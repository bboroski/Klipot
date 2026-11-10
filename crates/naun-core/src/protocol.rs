use crate::Artifact;
use std::fmt;

/// KLP1: magic, u32 item count, then (u32 media-type length, u64 data length,
/// UTF-8 media type bytes, payload bytes) for each item.
pub const BUNDLE_MAGIC: &[u8; 4] = b"KLP1";
const MAX_BUNDLE_ITEMS: usize = 65_536;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ProtocolError {
    BadMagic,
    Truncated,
    TooManyItems,
    InvalidMediaType,
    LengthOverflow,
    TrailingBytes,
}

impl fmt::Display for ProtocolError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::BadMagic => f.write_str("invalid KLP1 bundle magic"),
            Self::Truncated => f.write_str("truncated KLP1 bundle"),
            Self::TooManyItems => f.write_str("KLP1 item count exceeds limit"),
            Self::InvalidMediaType => f.write_str("bundle media type is not valid UTF-8"),
            Self::LengthOverflow => f.write_str("bundle length cannot be represented"),
            Self::TrailingBytes => f.write_str("unexpected trailing bytes in bundle"),
        }
    }
}

impl std::error::Error for ProtocolError {}

pub fn encode_bundle(items: &[Artifact]) -> Result<Artifact, ProtocolError> {
    if items.len() > MAX_BUNDLE_ITEMS {
        return Err(ProtocolError::TooManyItems);
    }
    let count = u32::try_from(items.len()).map_err(|_| ProtocolError::LengthOverflow)?;
    let mut out = Vec::new();
    out.extend_from_slice(BUNDLE_MAGIC);
    out.extend_from_slice(&count.to_le_bytes());

    for item in items {
        let media = item.media_type.as_bytes();
        let media_len = u32::try_from(media.len()).map_err(|_| ProtocolError::LengthOverflow)?;
        let data_len = u64::try_from(item.data.len()).map_err(|_| ProtocolError::LengthOverflow)?;
        out.extend_from_slice(&media_len.to_le_bytes());
        out.extend_from_slice(&data_len.to_le_bytes());
        out.extend_from_slice(media);
        out.extend_from_slice(&item.data);
    }

    Ok(Artifact::new("application/vnd.klipot.bundle; version=1", out))
}

pub fn decode_bundle(data: &[u8]) -> Result<Vec<Artifact>, ProtocolError> {
    let mut cursor = Cursor::new(data);
    if cursor.take(4)? != BUNDLE_MAGIC.as_slice() {
        return Err(ProtocolError::BadMagic);
    }
    let count = usize::try_from(cursor.u32()?).map_err(|_| ProtocolError::LengthOverflow)?;
    if count > MAX_BUNDLE_ITEMS {
        return Err(ProtocolError::TooManyItems);
    }

    let mut items = Vec::with_capacity(count);
    for _ in 0..count {
        let media_len = cursor.u32()? as usize;
        let data_len = usize::try_from(cursor.u64()?)
            .map_err(|_| ProtocolError::LengthOverflow)?;
        let media = std::str::from_utf8(cursor.take(media_len)?)
            .map_err(|_| ProtocolError::InvalidMediaType)?
            .to_owned();
        let payload = cursor.take(data_len)?.to_vec();
        items.push(Artifact::new(media, payload));
    }

    if cursor.remaining() != 0 {
        return Err(ProtocolError::TrailingBytes);
    }
    Ok(items)
}

struct Cursor<'a> {
    data: &'a [u8],
    offset: usize,
}

impl<'a> Cursor<'a> {
    fn new(data: &'a [u8]) -> Self {
        Self { data, offset: 0 }
    }

    fn remaining(&self) -> usize {
        self.data.len().saturating_sub(self.offset)
    }

    fn take(&mut self, length: usize) -> Result<&'a [u8], ProtocolError> {
        let end = self.offset.checked_add(length).ok_or(ProtocolError::LengthOverflow)?;
        if end > self.data.len() {
            return Err(ProtocolError::Truncated);
        }
        let part = &self.data[self.offset..end];
        self.offset = end;
        Ok(part)
    }

    fn u32(&mut self) -> Result<u32, ProtocolError> {
        let bytes: [u8; 4] = self.take(4)?.try_into().map_err(|_| ProtocolError::Truncated)?;
        Ok(u32::from_le_bytes(bytes))
    }

    fn u64(&mut self) -> Result<u64, ProtocolError> {
        let bytes: [u8; 8] = self.take(8)?.try_into().map_err(|_| ProtocolError::Truncated)?;
        Ok(u64::from_le_bytes(bytes))
    }
}
