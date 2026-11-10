use crate::{Arm, ArmContext, ArmError, ArmManifest, Artifact, GraphError, Workflow};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

#[derive(Clone, Debug)]
pub struct ExecutionPolicy {
    pub max_nodes: usize,
    pub max_artifact_bytes: usize,
    pub max_total_bytes: usize,
}

impl Default for ExecutionPolicy {
    fn default() -> Self {
        Self { max_nodes: 1_024, max_artifact_bytes: 16 * 1024 * 1024,
            max_total_bytes: 64 * 1024 * 1024 }
    }
}

#[derive(Clone, Default)]
pub struct CancellationToken(Arc<AtomicBool>);

impl CancellationToken {
    pub fn cancel(&self) { self.0.store(true, Ordering::Release); }
    pub fn is_cancelled(&self) -> bool { self.0.load(Ordering::Acquire) }
}

#[derive(Clone, Default)]
pub struct ExecutionContext {
    pub cancellation: CancellationToken,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NodeSummary {
    pub node_id: String,
    pub arm_id: String,
    pub input_count: usize,
    pub output_count: usize,
    pub output_bytes: usize,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExecutionReport {
    pub workflow_id: String,
    pub outputs: Vec<Artifact>,
    pub nodes: Vec<NodeSummary>,
    pub bytes_produced: usize,
}

pub struct Engine {
    arms: BTreeMap<String, Arc<dyn Arm>>,
    policy: ExecutionPolicy,
}

impl Default for Engine {
    fn default() -> Self { Self::new(ExecutionPolicy::default()) }
}

impl Engine {
    pub fn new(policy: ExecutionPolicy) -> Self {
        Self { arms: BTreeMap::new(), policy }
    }

    pub fn register<A: Arm + 'static>(&mut self, arm: A) -> Result<(), EngineError> {
        let manifest = arm.manifest();
        validate_manifest(&manifest)?;
        if self.arms.contains_key(&manifest.id) {
            return Err(EngineError::DuplicateArm(manifest.id));
        }
        self.arms.insert(manifest.id.clone(), Arc::new(arm));
        Ok(())
    }

    pub fn manifests(&self) -> Vec<ArmManifest> {
        self.arms.values().map(|arm| arm.manifest()).collect()
    }

    pub fn execute(&self, workflow: &Workflow, initial: Vec<Artifact>,
        context: &ExecutionContext) -> Result<ExecutionReport, EngineError> {
        if workflow.nodes.len() > self.policy.max_nodes {
            return Err(EngineError::NodeLimitExceeded {
                actual: workflow.nodes.len(), limit: self.policy.max_nodes,
            });
        }
        let order = workflow.execution_order()?;
        if initial.is_empty() { return Err(EngineError::NoInputArtifacts); }

        let mut total_bytes = 0usize;
        for artifact in &initial {
            validate_artifact(artifact)?;
            if artifact.data.len() > self.policy.max_artifact_bytes {
                return Err(EngineError::ArtifactTooLarge {
                    actual: artifact.data.len(), limit: self.policy.max_artifact_bytes,
                });
            }
            total_bytes = total_bytes.checked_add(artifact.data.len())
                .ok_or(EngineError::BudgetExceeded)?;
        }
        if total_bytes > self.policy.max_total_bytes {
            return Err(EngineError::BudgetExceeded);
        }

        let mut outputs_by_node = BTreeMap::<String, Vec<Artifact>>::new();
        let mut summaries = Vec::with_capacity(order.len());
        let mut produced_bytes = 0usize;

        for index in order {
            if context.cancellation.is_cancelled() { return Err(EngineError::Cancelled); }

            let node = &workflow.nodes[index];
            let arm = self.arms.get(&node.arm)
                .ok_or_else(|| EngineError::UnknownArm(node.arm.clone()))?;

            let mut inputs = Vec::new();
            if node.needs.is_empty() {
                inputs.extend(initial.iter().cloned());
            } else {
                for dependency in &node.needs {
                    let upstream = outputs_by_node.get(dependency)
                        .ok_or_else(|| EngineError::MissingRuntimeOutput(dependency.clone()))?;
                    inputs.extend(upstream.iter().cloned());
                }
            }

            let arm_context = ArmContext {
                workflow_id: workflow.id.clone(), node_id: node.id.clone(),
            };
            let outputs = arm.execute(&inputs, &arm_context)
                .map_err(|source| EngineError::ArmFailed {
                    node_id: node.id.clone(), source,
                })?;

            let mut node_bytes = 0usize;
            for artifact in &outputs {
                validate_artifact(artifact)?;
                if artifact.data.len() > self.policy.max_artifact_bytes {
                    return Err(EngineError::ArtifactTooLarge {
                        actual: artifact.data.len(), limit: self.policy.max_artifact_bytes,
                    });
                }
                node_bytes = node_bytes.checked_add(artifact.data.len())
                    .ok_or(EngineError::BudgetExceeded)?;
            }
            produced_bytes = produced_bytes.checked_add(node_bytes)
                .ok_or(EngineError::BudgetExceeded)?;
            if total_bytes.checked_add(produced_bytes).ok_or(EngineError::BudgetExceeded)?
                > self.policy.max_total_bytes {
                return Err(EngineError::BudgetExceeded);
            }

            summaries.push(NodeSummary {
                node_id: node.id.clone(), arm_id: node.arm.clone(),
                input_count: inputs.len(), output_count: outputs.len(),
                output_bytes: node_bytes,
            });
            outputs_by_node.insert(node.id.clone(), outputs);
        }

        let depended_on: BTreeSet<&str> = workflow.nodes.iter()
            .flat_map(|node| node.needs.iter().map(String::as_str)).collect();
        let mut final_outputs = Vec::new();
        for node in &workflow.nodes {
            if !depended_on.contains(node.id.as_str()) {
                if let Some(outputs) = outputs_by_node.get(&node.id) {
                    final_outputs.extend(outputs.iter().cloned());
                }
            }
        }

        Ok(ExecutionReport {
            workflow_id: workflow.id.clone(), outputs: final_outputs,
            nodes: summaries, bytes_produced: produced_bytes,
        })
    }
}

fn validate_manifest(manifest: &ArmManifest) -> Result<(), EngineError> {
    let valid_id = !manifest.id.is_empty() && manifest.id.len() <= 128
        && manifest.id.chars().all(|ch| ch.is_ascii_alphanumeric() || "-_.".contains(ch));
    if !valid_id || manifest.version.is_empty() || manifest.api_version == 0 {
        return Err(EngineError::InvalidManifest(manifest.id.clone()));
    }
    Ok(())
}

fn validate_artifact(artifact: &Artifact) -> Result<(), EngineError> {
    if artifact.media_type.trim().is_empty() {
        return Err(EngineError::InvalidArtifact("media_type must not be empty".into()));
    }
    Ok(())
}

#[derive(Debug)]
pub enum EngineError {
    Graph(GraphError),
    DuplicateArm(String),
    InvalidManifest(String),
    UnknownArm(String),
    MissingRuntimeOutput(String),
    NoInputArtifacts,
    InvalidArtifact(String),
    NodeLimitExceeded { actual: usize, limit: usize },
    ArtifactTooLarge { actual: usize, limit: usize },
    BudgetExceeded,
    Cancelled,
    ArmFailed { node_id: String, source: ArmError },
}

impl From<GraphError> for EngineError {
    fn from(value: GraphError) -> Self { Self::Graph(value) }
}

impl fmt::Display for EngineError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Graph(error) => write!(f, "invalid workflow: {error}"),
            Self::DuplicateArm(id) => write!(f, "arm already registered: {id}"),
            Self::InvalidManifest(id) => write!(f, "invalid manifest for arm: {id}"),
            Self::UnknownArm(id) => write!(f, "unknown arm: {id}"),
            Self::MissingRuntimeOutput(id) => write!(f, "dependency produced no runtime entry: {id}"),
            Self::NoInputArtifacts => f.write_str("execution requires at least one input artifact"),
            Self::InvalidArtifact(message) => write!(f, "invalid artifact: {message}"),
            Self::NodeLimitExceeded { actual, limit } =>
                write!(f, "workflow has {actual} nodes; policy limit is {limit}"),
            Self::ArtifactTooLarge { actual, limit } =>
                write!(f, "artifact has {actual} bytes; policy limit is {limit}"),
            Self::BudgetExceeded => f.write_str("execution byte budget exceeded"),
            Self::Cancelled => f.write_str("workflow execution was cancelled"),
            Self::ArmFailed { node_id, source } =>
                write!(f, "arm failed at node {node_id}: {source}"),
        }
    }
}

impl std::error::Error for EngineError {}
