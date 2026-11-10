use naun_core::{
    decode_bundle, Engine, Fnv1a64Arm, IdentityArm, MergeArm, NodeSpec,
    PrefixArm, Utf8UppercaseArm, Workflow, Artifact, ExecutionContext,
};
use std::error::Error;

fn main() {
    if let Err(error) = run() {
        eprintln!("klipot: {error}");
        std::process::exit(1);
    }
}

fn run() -> Result<(), Box<dyn Error>> {
    let command = std::env::args().nth(1).unwrap_or_else(|| "help".into());
    match command.as_str() {
        "demo" => run_demo()?,
        "self-check" => {
            run_demo()?;
            println!("NAUN self-check: OK");
        }
        "arms" => list_arms()?,
        "help" | "--help" | "-h" => print_help(),
        other => {
            eprintln!("unknown command: {other}");
            print_help();
            std::process::exit(2);
        }
    }
    Ok(())
}

fn build_engine() -> Result<Engine, Box<dyn Error>> {
    let mut engine = Engine::default();
    engine.register(Utf8UppercaseArm)?;
    engine.register(PrefixArm::new("Klipot/NAUN: "))?;
    engine.register(MergeArm)?;
    engine.register(IdentityArm)?;
    engine.register(Fnv1a64Arm)?;
    Ok(engine)
}

fn run_demo() -> Result<(), Box<dyn Error>> {
    let engine = build_engine()?;
    let workflow = Workflow::new(
        "naun-octopus-demo",
        vec![
            NodeSpec::new("arm-cortex", "utf8-uppercase", vec![]),
            NodeSpec::new("arm-prefix", "prefix", vec![]),
            NodeSpec::new(
                "central-mantle",
                "merge",
                vec!["arm-cortex".into(), "arm-prefix".into()],
            ),
        ],
    );

    let report = engine.execute(
        &workflow,
        vec![Artifact::text("one system becomes a stronger system")],
        &ExecutionContext::default(),
    )?;

    println!("NAUN / KLIPOT — octopus composition runtime");
    println!("workflow: {}", report.workflow_id);
    for node in &report.nodes {
        println!(
            "  {:<18} arm={:<16} inputs={} outputs={} bytes={}",
            node.node_id, node.arm_id, node.input_count, node.output_count, node.output_bytes
        );
    }

    let bundle = report.outputs.first().ok_or_else(|| std::io::Error::new(
        std::io::ErrorKind::NotFound,
        "workflow produced no terminal artifact",
    ))?;
    let parts = decode_bundle(&bundle.data)?;
    println!("result: {} ({} bytes)", bundle.media_type, bundle.data.len());
    for (index, part) in parts.iter().enumerate() {
        println!(
            "  tentacle[{}] {} => {}",
            index,
            part.media_type,
            String::from_utf8_lossy(&part.data)
        );
    }
    println!("bytes produced across nodes: {}", report.bytes_produced);
    Ok(())
}

fn list_arms() -> Result<(), Box<dyn Error>> {
    let engine = build_engine()?;
    for manifest in engine.manifests() {
        println!("{:<16} v{:<8} {}", manifest.id, manifest.version, manifest.description);
        for capability in manifest.capabilities {
            println!("  - {capability}");
        }
    }
    Ok(())
}

fn print_help() {
    println!(
        "Klipot / NAUN — modular system composition runtime\n\n         Usage:\n           klipot demo        Run a two-arm composition and decode the KLP1 bundle\n           klipot arms        List built-in arms and capabilities\n           klipot self-check  Run the composition smoke test\n           klipot help        Show this help\n"
    );
}
