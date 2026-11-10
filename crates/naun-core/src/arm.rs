use crate::Artifact;
use std::fmt;

/// The contract version implemented by this core.
pub const ARM_API_VERSION: u16 = 1;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ArmManifest {
    pub api_version: u16,
    pub id: String,
    pub version: String,
    pub description: String,
    pub capabilities: Vec<String>,
}

impl ArmManifest {
    pub fn new(
        id: impl Into<String>,
        version: impl Into<String>,
        description: impl Into<String>,
        capabilities: Vec<String>,
    ) -> Self {
        Self {
            api_version: ARM_API_VERSION,
            id: id.into(),
            version: version.into(),
            description: description.into(),
            capabilities,
        }
    }
}

/// Per-node metadata passed to an executing arm.
#[derive(Clone, Debug)]
pub struct ArmContext {
    pub workflow_id: String,
    pub node_id: String,
}

/// A module failure is explicit and attributed to the node by the engine.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ArmError {
    pub message: String,
}

impl ArmError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl fmt::Display for ArmError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.message)
    }
}

impl std::error::Error for ArmError {}

/// An independently registerable unit of work.
///
/// Implementations should be deterministic where possible, avoid hidden global
/// state, and treat inputs as read-only. A registered arm is trusted in-process
/// code; this trait is an extension contract, not a sandbox.
pub trait Arm: Send + Sync {
    fn manifest(&self) -> ArmManifest;

    fn execute(
        &self,
        inputs: &[Artifact],
        context: &ArmContext,
    ) -> Result<Vec<Artifact>, ArmError>;
}
