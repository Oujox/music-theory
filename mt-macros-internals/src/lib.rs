// use proc_macro2::TokenStream;
// use quote::quote;
// use syn::parse::{Parse, ParseStream};
// use syn::Result;
// use syn::{Expr, ExprArray, Ident, Token};

// struct DynamicEnum {
//     inner1: Ident,
//     inner2: ExprArray,
// }
// impl Parse for DynamicEnum {
//     fn parse(input: ParseStream) -> Result<Self> {
//         let ident_enum: Ident = input.parse()?;
//         input.parse::<Token![,]>()?;

//         let expr_vec = input.parse()?;
//         let expr_vec = match expr_vec {
//             Expr::Array(expr_vec) => expr_vec,
//             _ => panic!(""),
//         };

//         Ok(DynamicEnum {
//             inner1: ident_enum,
//             inner2: expr_vec,
//         })
//     }
// }

// pub fn generate_dynamic_enum(array: DynamicEnum) -> TokenStream {
//     TokenStream::from(expanded)
// }
