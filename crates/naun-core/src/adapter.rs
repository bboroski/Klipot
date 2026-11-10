use crate::{Arm, ArmContext, ArmError, ArmManifest, Artifact};

/// Boundary for a real external system: database, service, device gateway,
/// compiler, message bus, MES connector, or another application.
pub trait SystemAdapter: Send + Sync {
    fn system_id(&self) -> &str;
    fn version(&self) -> &str;
    fn capabilities(&self) -> Vec<String>;

    fn exchange(
        &self,
        request: &Artifact,
        context: &ArmContext,
    ) -> Result<Artifact, ArmError>;
}

/// Turns one request/response adapter into a regular NAUN arm.
/// One adapter invocation is performed for each input artifact.
pub struct AdapterArm<A> {
    adapter: A,
    arm_id: String,
}

impl<A> AdapterArm<A> {
    pub fn new(arm_id: impl Into<String>, adapter: A) -> Self {
        Self {
            adapter,
            arm_id: arm_id.into(),
        }
    }

    pub fn adapter(&self) -> &A {
        &self.adapter
    }
}

impl<A: SystemAdapter> Arm for AdapterArm<A> {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new(
            self.arm_id.clone(),
            self.adapter.version(),
            format!("Adapter for {}", self.adapter.system_id()),
            self.adapter.capabilities(),
        )
    }

    fn execute(
        &self,
        inputs: &[Artifact],
        context: &ArmContext,
    ) -> Result<Vec<Artifact>, ArmError> {
        inputs
            .iter()
            .map(|input| self.adapter.exchange(input, context))
            .collect()
    }
}
