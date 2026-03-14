use std::collections::HashMap;

use crate::ast::{BinOp, Expr, Stmt};

#[derive(Debug, Clone)]
enum Value {
    Number(f64),
    String(String),
}

pub struct Runtime {
    globals: HashMap<String, Value>,
}

impl Runtime {
    pub fn new() -> Self {
        Self {
            globals: HashMap::new(),
        }
    }

    pub fn run(&mut self, program: &[Stmt]) -> Result<(), String> {
        for stmt in program {
            self.exec_stmt(stmt)?;
        }
        Ok(())
    }

    fn exec_stmt(&mut self, stmt: &Stmt) -> Result<(), String> {
        match stmt {
            Stmt::Let(name, expr) | Stmt::Assign(name, expr) => {
                let value = self.eval_expr(expr)?;
                self.globals.insert(name.clone(), value);
                Ok(())
            }
            Stmt::Print(expr) => {
                let value = self.eval_expr(expr)?;
                match value {
                    Value::Number(n) => println!("{}", n),
                    Value::String(s) => println!("{}", s),
                }
                Ok(())
            }
        }
    }

    fn eval_expr(&self, expr: &Expr) -> Result<Value, String> {
        match expr {
            Expr::Number(n) => Ok(Value::Number(*n)),
            Expr::String(s) => Ok(Value::String(s.clone())),
            Expr::Name(name) => self
                .globals
                .get(name)
                .cloned()
                .ok_or_else(|| format!("Undefined variable '{}'", name)),
            Expr::Binary(left, op, right) => {
                let a = self.eval_expr(left)?;
                let b = self.eval_expr(right)?;
                self.apply_binary(*op, a, b)
            }
        }
    }

    fn apply_binary(&self, op: BinOp, a: Value, b: Value) -> Result<Value, String> {
        match (op, a, b) {
            (BinOp::Add, Value::Number(x), Value::Number(y)) => Ok(Value::Number(x + y)),
            (BinOp::Add, Value::String(x), Value::String(y)) => Ok(Value::String(x + &y)),
            (BinOp::Sub, Value::Number(x), Value::Number(y)) => Ok(Value::Number(x - y)),
            (BinOp::Mul, Value::Number(x), Value::Number(y)) => Ok(Value::Number(x * y)),
            (BinOp::Div, Value::Number(x), Value::Number(y)) => Ok(Value::Number(x / y)),
            (BinOp::Add, _, _) => Err("Type error: '+' expects two numbers or two strings".to_string()),
            (BinOp::Sub, _, _) => Err("Type error: '-' expects two numbers".to_string()),
            (BinOp::Mul, _, _) => Err("Type error: '*' expects two numbers".to_string()),
            (BinOp::Div, _, _) => Err("Type error: '/' expects two numbers".to_string()),
        }
    }
}
