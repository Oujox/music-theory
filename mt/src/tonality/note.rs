use super::{CoreMT, TonalityMT};

#[derive(Debug, Clone)]
pub struct Note {
    name: String,
}
impl Note {
    fn new(name: String) -> Self {
        Self { name }
    }
}
impl CoreMT for Note {}
impl TonalityMT for Note {}
