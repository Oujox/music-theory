use std::cell::LazyCell;

pub struct B {
    a: String,
}
impl B {
    fn new(a: String) -> Self {
        Self { a }
    }
}

pub struct A {
    pub b: LazyCell<B>,
}
impl A {
    fn new() -> Self {
        Self {
            b: LazyCell::new(|| return B::new("a".to_string())),
        }
    }
}

fn main() {
    let a = A::new();
    println!("{}", a.b.a);
}
