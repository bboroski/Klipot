use crate::{encode_bundle, Arm, ArmContext, ArmError, ArmManifest, Artifact};

pub struct IdentityArm;

impl Arm for IdentityArm {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new("identity", "1.0.0", "Passes input artifacts through unchanged",
            vec!["transform.identity".into()])
    }
    fn execute(&self, inputs: &[Artifact], _context: &ArmContext)
        -> Result<Vec<Artifact>, ArmError> {
        Ok(inputs.to_vec())
    }
}

pub struct PrefixArm { prefix: Vec<u8> }

impl PrefixArm {
    pub fn new(prefix: impl Into<Vec<u8>>) -> Self {
        Self { prefix: prefix.into() }
    }
}

impl Arm for PrefixArm {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new("prefix", "1.0.0", "Prepends a fixed byte prefix to every input",
            vec!["transform.bytes".into()])
    }
    fn execute(&self, inputs: &[Artifact], _context: &ArmContext)
        -> Result<Vec<Artifact>, ArmError> {
        inputs.iter().map(|input| {
            let mut data = Vec::with_capacity(self.prefix.len() + input.data.len());
            data.extend_from_slice(&self.prefix);
            data.extend_from_slice(&input.data);
            Ok(Artifact::new(input.media_type.clone(), data))
        }).collect()
    }
}

pub struct Utf8UppercaseArm;

impl Arm for Utf8UppercaseArm {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new("utf8-uppercase", "1.0.0",
            "Uppercases UTF-8 text without changing non-text payloads",
            vec!["transform.text.utf8".into()])
    }
    fn execute(&self, inputs: &[Artifact], _context: &ArmContext)
        -> Result<Vec<Artifact>, ArmError> {
        inputs.iter().map(|input| {
            let text = std::str::from_utf8(&input.data)
                .map_err(|error| ArmError::new(format!("input is not UTF-8: {error}")))?;
            Ok(Artifact::new(input.media_type.clone(), text.to_uppercase().into_bytes()))
        }).collect()
    }
}

pub struct MergeArm;

impl Arm for MergeArm {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new("merge", "1.0.0",
            "Packs multiple input artifacts into a reversible KLP1 bundle",
            vec!["compose.bundle.klp1".into()])
    }
    fn execute(&self, inputs: &[Artifact], _context: &ArmContext)
        -> Result<Vec<Artifact>, ArmError> {
        let bundle = encode_bundle(inputs)
            .map_err(|error| ArmError::new(format!("cannot encode bundle: {error}")))?;
        Ok(vec![bundle])
    }
}

pub struct Fnv1a64Arm;

impl Arm for Fnv1a64Arm {
    fn manifest(&self) -> ArmManifest {
        ArmManifest::new("fnv1a64", "1.0.0",
            "Computes a non-cryptographic FNV-1a 64-bit diagnostic hash",
            vec!["inspect.hash.fnv1a64".into()])
    }
    fn execute(&self, inputs: &[Artifact], _context: &ArmContext)
        -> Result<Vec<Artifact>, ArmError> {
        let mut outputs = Vec::with_capacity(inputs.len());
        for input in inputs {
            let mut hash = 0xcbf29ce484222325u64;
            for byte in &input.data {
                hash ^= u64::from(*byte);
                hash = hash.wrapping_mul(0x100000001b3);
            }
            outputs.push(Artifact::text(format!("{hash:016x}"))
                .with_label("algorithm", "fnv1a-64")
                .with_label("security", "non-cryptographic"));
        }
        Ok(outputs)
    }
}
