pub mod common;
pub mod harmony;
pub mod stracture;
pub mod stream;
pub mod timbre;
pub mod tonality;

use common::CommonConfig;
use harmony::HarmonyConfig;
use stracture::StractureConfig;
use stream::StreamConfig;
use timbre::TimbreConfig;
use tonality::TonalityConfig;

extern crate toml;

use serde::{Deserialize, Serialize};
use std::fs;
use std::ops::Deref;
use std::sync::{Arc, LazyLock, RwLock};

///
///
///
///
///
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct InnerConfig {
    #[serde(flatten)]
    pub common: CommonConfig,
    pub tonality: TonalityConfig,
    pub timbre: TimbreConfig,
    pub stracture: StractureConfig,
    pub harmony: HarmonyConfig,
    pub stream: StreamConfig,
}
impl InnerConfig {
    pub fn new(path: &str) -> Result<Self, toml::de::Error> {
        let s: String = fs::read_to_string(path).unwrap();
        return toml::from_str(&s);
    }
}

///
///
///
///
///
#[derive(Debug, Clone)]
pub struct MTConfig {
    pub path: String,
    pub config: InnerConfig,
}
impl MTConfig {
    pub fn new(path: &str) -> Self {
        Self {
            path: path.to_string(),
            config: InnerConfig::new(path).unwrap(),
        }
    }
    pub fn reload(&mut self) -> bool {
        match InnerConfig::new(&self.path) {
            Ok(c) => {
                self.config = c;
                true
            }
            Err(_) => false,
        }
    }
}
impl Deref for MTConfig {
    type Target = InnerConfig;
    fn deref(&self) -> &Self::Target {
        &self.config
    }
}

///
///
///
///
///
pub struct Config {
    inner: LazyLock<Arc<RwLock<MTConfig>>>,
}
impl Config {
    pub fn new() -> Self {
        Self {
            inner: LazyLock::new(|| Arc::new(RwLock::new(MTConfig::new("")))),
        }
    }

    pub fn reload(&mut self) -> bool {
        match self.inner.write() {
            Ok(mut w) => w.reload(),
            Err(_) => false,
        }
    }
}
impl Deref for Config {
    type Target = RwLock<MTConfig>;
    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

#[cfg(test)]
mod tests_config {
    #[test]
    fn test_confiog() {}
}
