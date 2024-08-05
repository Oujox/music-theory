use crate::config::{Config, MTConfig};

pub trait CoreMT {
    fn config() -> MTConfig {
        Config::new().read().expect("").clone()
    }
}
