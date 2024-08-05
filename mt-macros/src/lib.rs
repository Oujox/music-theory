// extern crate mt_macros_internals as mtmi;
// use proc_macro::TokenStream;
// use syn::parse_macro_input;

// #[proc_macro]
// pub fn generate_dynamic_enum(item: TokenStream) -> TokenStream {
//     let input = parse_macro_input!(item as mtmi::DynamicEnum);
//     mtmi::generate_dynamic_enum(input).into()
// }
