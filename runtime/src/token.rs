#[derive(Debug, Clone, PartialEq)]
pub enum TokenKind {
    Let,
    Print,
    Ident(String),
    Number(f64),
    String(String),
    Plus,
    Minus,
    Star,
    Slash,
    Equal,
    LParen,
    RParen,
    Newline,
    Eof,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub kind: TokenKind,
    pub line: usize,
    pub col: usize,
}

impl Token {
    pub fn new(kind: TokenKind, line: usize, col: usize) -> Self {
        Self { kind, line, col }
    }
}
