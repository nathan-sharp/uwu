mod ast;
mod lexer;
mod parser;
mod runtime;
mod token;

use std::env;
use std::fs;
use std::path::Path;

use lexer::lex;
use parser::parse;
use runtime::Runtime;

const RUNTIME_NAME: &str = "PAWS Runtime";
const RUNTIME_EXPANSION: &str = "Platform Agnostic Wrapper Service";

fn print_usage() {
    eprintln!("{} ({})", RUNTIME_NAME, RUNTIME_EXPANSION);
    eprintln!("Usage: paws run <file.uwu>");
}

fn run_file(path: &Path) -> Result<(), String> {
    let source = fs::read_to_string(path)
        .map_err(|e| format!("Could not read '{}': {}", path.display(), e))?;
    let tokens = lex(&source)?;
    let program = parse(&tokens)?;
    let mut rt = Runtime::new();
    rt.run(&program)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 || args[1] != "run" {
        print_usage();
        std::process::exit(1);
    }

    let path = Path::new(&args[2]);
    if let Err(err) = run_file(path) {
        eprintln!("{} error: {}", RUNTIME_NAME, err);
        std::process::exit(2);
    }
}
