use naun_core::{
    decode_bundle, Arm, ArmContext, ArmError, ArmManifest, Artifact, Engine,
    EngineError, ExecutionContext, ExecutionPolicy, MergeArm, NodeSpec, PrefixArm,
    Utf8UppercaseArm, Workflow,
};

fn demo_workflow() -> Workflow {
    Workflow::new("integration-test", vec![
        NodeSpec::new("upper", "utf8-uppercase", vec![]),
        NodeSpec::new("prefix", "prefix", vec![]),
        NodeSpec::new("bundle", "merge", vec!["upper".into(), "prefix".into()]),
    ])
}

#[test]
fn independent_arms_compose_into_reversible_bundle() {
    let mut engine = Engine::default();
    engine.register(Utf8UppercaseArm).unwrap();
    engine.register(PrefixArm::new("tag: ")).unwrap();
    engine.register(MergeArm).unwrap();

    let report = engine.execute(&demo_workflow(), vec![Artifact::text("naun")],
        &ExecutionContext::default()).unwrap();

    assert_eq!(report.nodes.len(), 3);
    assert_eq!(report.outputs.len(), 1);
    let unpacked = decode_bundle(&report.outputs[0].data).unwrap();
    assert_eq!(unpacked.len(), 2);
    assert_eq!(unpacked[0].data, b"NAUN");
    assert_eq!(unpacked[1].data, b"tag: naun");
}

#[test]
fn cycle_is_rejected_before_execution() {
    let workflow = Workflow::new("cycle", vec![
        NodeSpec::new("a", "identity", vec!["b".into()]),
        NodeSpec::new("b", "identity", vec!["a".into()]),
    ]);
    assert!(workflow.execution_order().is_err());
}

#[test]
fn byte_budget_is_enforced() {
    let mut engine = Engine::new(ExecutionPolicy {
        max_nodes: 8, max_artifact_bytes: 128, max_total_bytes: 4,
    });
    engine.register(PrefixArm::new("x")).unwrap();
    let workflow = Workflow::new("budget",
        vec![NodeSpec::new("prefix", "prefix", vec![])]);
    let error = engine.execute(&workflow, vec![Artifact::text("abc")],
        &ExecutionContext::default()).unwrap_err();
    assert!(matches!(error, EngineError::BudgetExceeded));
}

struct FailingArm;

impl Arm for FailingArm {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new("fail", "1.0.0", "test failure", vec![])
    }
    fn execute(&self, _inputs: &[Artifact], _context: &ArmContext)
        -> Result<Vec<Artifact>, ArmError> {
        Err(ArmError::new("intentional test error"))
    }
}

#[test]
fn arm_failure_is_reported_in_context() {
    let mut engine = Engine::default();
    engine.register(FailingArm).unwrap();
    let workflow = Workflow::new("failure",
        vec![NodeSpec::new("fragile", "fail", vec![])]);
    let error = engine.execute(&workflow, vec![Artifact::text("input")],
        &ExecutionContext::default()).unwrap_err();
    assert!(error.to_string().contains("fragile"));
}
