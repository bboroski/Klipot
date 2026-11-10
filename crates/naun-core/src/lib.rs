//! NAUN's deterministic, in-process composition runtime.

mod adapter;
mod arm;
mod artifact;
mod builtins;
mod engine;
mod graph;
mod protocol;

pub use adapter::{AdapterArm, SystemAdapter};
pub use arm::{Arm, ArmContext, ArmError, ArmManifest, ARM_API_VERSION};
pub use artifact::Artifact;
pub use builtins::{
    Fnv1a64Arm, IdentityArm, MergeArm, PrefixArm, Utf8UppercaseArm,
};
pub use engine::{
    CancellationToken, Engine, EngineError, ExecutionContext, ExecutionPolicy,
    ExecutionReport, NodeSummary,
};
pub use graph::{GraphError, NodeSpec, Workflow};
pub use protocol::{decode_bundle, encode_bundle, ProtocolError, BUNDLE_MAGIC};
