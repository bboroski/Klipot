use std::collections::BTreeMap;

/// Immutable-by-convention payload passed between modules.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Artifact {
    pub media_type: String,
    pub data: Vec<u8>,
    pub labels: BTreeMap<String, String>,
}

impl Artifact {
    pub fn new(media_type: impl Into<String>, data: impl Into<Vec<u8>>) -> Self {
        Self {
            media_type: media_type.into(),
            data: data.into(),
            labels: BTreeMap::new(),
        }
    }

    pub fn text(value: impl Into<String>) -> Self {
        Self::new("text/plain; charset=utf-8", value.into().into_bytes())
    }

    pub fn with_label(
        mut self,
        key: impl Into<String>,
        value: impl Into<String>,
    ) -> Self {
        self.labels.insert(key.into(), value.into());
        self
    }
}
