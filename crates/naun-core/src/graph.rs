use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NodeSpec {
    pub id: String,
    pub arm: String,
    pub needs: Vec<String>,
}

impl NodeSpec {
    pub fn new(
        id: impl Into<String>,
        arm: impl Into<String>,
        needs: Vec<String>,
    ) -> Self {
        Self { id: id.into(), arm: arm.into(), needs }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Workflow {
    pub id: String,
    pub nodes: Vec<NodeSpec>,
}

impl Workflow {
    pub fn new(id: impl Into<String>, nodes: Vec<NodeSpec>) -> Self {
        Self { id: id.into(), nodes }
    }

    /// Validate the graph and return stable, topological node indexes.
    /// Independent nodes are ordered lexicographically by node ID.
    pub fn execution_order(&self) -> Result<Vec<usize>, GraphError> {
        if !valid_identifier(&self.id) {
            return Err(GraphError::InvalidWorkflowId(self.id.clone()));
        }
        if self.nodes.is_empty() {
            return Err(GraphError::EmptyWorkflow);
        }

        let mut indexes = BTreeMap::<String, usize>::new();
        for (index, node) in self.nodes.iter().enumerate() {
            if !valid_identifier(&node.id) {
                return Err(GraphError::InvalidNodeId(node.id.clone()));
            }
            if !valid_identifier(&node.arm) {
                return Err(GraphError::InvalidArmId(node.arm.clone()));
            }
            if indexes.insert(node.id.clone(), index).is_some() {
                return Err(GraphError::DuplicateNode(node.id.clone()));
            }
        }

        let mut indegree = vec![0usize; self.nodes.len()];
        let mut successors = vec![Vec::<usize>::new(); self.nodes.len()];

        for (index, node) in self.nodes.iter().enumerate() {
            let mut seen = BTreeSet::new();
            for dependency in &node.needs {
                if !seen.insert(dependency) {
                    return Err(GraphError::DuplicateDependency {
                        node: node.id.clone(),
                        dependency: dependency.clone(),
                    });
                }
                if dependency == &node.id {
                    return Err(GraphError::SelfDependency(node.id.clone()));
                }
                let Some(&parent_index) = indexes.get(dependency) else {
                    return Err(GraphError::MissingDependency {
                        node: node.id.clone(),
                        dependency: dependency.clone(),
                    });
                };
                indegree[index] += 1;
                successors[parent_index].push(index);
            }
        }

        let mut ready = BTreeSet::<(String, usize)>::new();
        for (index, degree) in indegree.iter().enumerate() {
            if *degree == 0 {
                ready.insert((self.nodes[index].id.clone(), index));
            }
        }

        let mut order = Vec::with_capacity(self.nodes.len());
        while let Some(next) = ready.iter().next().cloned() {
            ready.remove(&next);
            let index = next.1;
            order.push(index);
            for &child in &successors[index] {
                indegree[child] -= 1;
                if indegree[child] == 0 {
                    ready.insert((self.nodes[child].id.clone(), child));
                }
            }
        }

        if order.len() != self.nodes.len() {
            return Err(GraphError::CycleDetected);
        }
        Ok(order)
    }
}

fn valid_identifier(value: &str) -> bool {
    !value.is_empty()
        && value.len() <= 128
        && value.chars().all(|ch| ch.is_ascii_alphanumeric() || "-_.".contains(ch))
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum GraphError {
    EmptyWorkflow,
    InvalidWorkflowId(String),
    InvalidNodeId(String),
    InvalidArmId(String),
    DuplicateNode(String),
    DuplicateDependency { node: String, dependency: String },
    MissingDependency { node: String, dependency: String },
    SelfDependency(String),
    CycleDetected,
}

impl fmt::Display for GraphError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyWorkflow => f.write_str("workflow contains no nodes"),
            Self::InvalidWorkflowId(id) => write!(f, "invalid workflow id: {id}"),
            Self::InvalidNodeId(id) => write!(f, "invalid node id: {id}"),
            Self::InvalidArmId(id) => write!(f, "invalid arm id: {id}"),
            Self::DuplicateNode(id) => write!(f, "duplicate node id: {id}"),
            Self::DuplicateDependency { node, dependency } =>
                write!(f, "node {node} repeats dependency {dependency}"),
            Self::MissingDependency { node, dependency } =>
                write!(f, "node {node} depends on missing node {dependency}"),
            Self::SelfDependency(id) => write!(f, "node {id} depends on itself"),
            Self::CycleDetected => f.write_str("workflow contains a dependency cycle"),
        }
    }
}

impl std::error::Error for GraphError {}
