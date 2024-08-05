pub mod key;
pub mod note;
pub mod scale;

use std::collections::HashMap;

use crate::core::CoreMT;

pub trait NoteName {}
impl NoteName for &str {}

pub trait PitchClass {}
impl PitchClass for u8 {}

pub struct NoteNames<T: NoteName> {
    names: Vec<T>,
}

pub struct PitchClasses<T: PitchClass> {
    classes: Vec<T>,
}

pub struct Symbols {}

pub trait TonalityMT: CoreMT {}
