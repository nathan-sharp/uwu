#[derive(Debug, Clone)]
pub enum Stmt {
    Let(String, Expr),
    Assign(String, Expr),
    Print(Expr),
}

#[derive(Debug, Clone)]
pub enum Expr {
    Number(f64),
    String(String),
    Name(String),
    Binary(Box<Expr>, BinOp, Box<Expr>),
}

#[derive(Debug, Clone, Copy)]
pub enum BinOp {
    Add,
    Sub,
    Mul,
    Div,
}
