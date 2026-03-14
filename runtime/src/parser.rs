use crate::ast::{BinOp, Expr, Stmt};
use crate::token::{Token, TokenKind};

pub fn parse(tokens: &[Token]) -> Result<Vec<Stmt>, String> {
    let mut p = Parser { tokens, i: 0 };
    p.parse_program()
}

struct Parser<'a> {
    tokens: &'a [Token],
    i: usize,
}

impl<'a> Parser<'a> {
    fn parse_program(&mut self) -> Result<Vec<Stmt>, String> {
        let mut statements = Vec::new();
        while !self.check_eof() {
            self.skip_newlines();
            if self.check_eof() {
                break;
            }
            statements.push(self.statement()?);
            self.skip_newlines();
        }
        Ok(statements)
    }

    fn statement(&mut self) -> Result<Stmt, String> {
        if self.match_token(|k| matches!(k, TokenKind::Let)) {
            let name = self.consume_ident("Expected identifier after 'let'")?;
            self.consume_equal("Expected '=' after variable name")?;
            let expr = self.expression()?;
            return Ok(Stmt::Let(name, expr));
        }

        if self.match_token(|k| matches!(k, TokenKind::Print)) {
            let expr = self.expression()?;
            return Ok(Stmt::Print(expr));
        }

        if let Some(name) = self.peek_ident_owned() {
            if self.peek_next_is_equal() {
                self.advance();
                self.advance();
                let expr = self.expression()?;
                return Ok(Stmt::Assign(name, expr));
            }
        }

        let tok = self.peek();
        Err(format!("Unexpected token at {}:{}", tok.line, tok.col))
    }

    fn expression(&mut self) -> Result<Expr, String> {
        self.term()
    }

    fn term(&mut self) -> Result<Expr, String> {
        let mut expr = self.factor()?;
        loop {
            if self.match_token(|k| matches!(k, TokenKind::Plus)) {
                let right = self.factor()?;
                expr = Expr::Binary(Box::new(expr), BinOp::Add, Box::new(right));
                continue;
            }
            if self.match_token(|k| matches!(k, TokenKind::Minus)) {
                let right = self.factor()?;
                expr = Expr::Binary(Box::new(expr), BinOp::Sub, Box::new(right));
                continue;
            }
            break;
        }
        Ok(expr)
    }

    fn factor(&mut self) -> Result<Expr, String> {
        let mut expr = self.primary()?;
        loop {
            if self.match_token(|k| matches!(k, TokenKind::Star)) {
                let right = self.primary()?;
                expr = Expr::Binary(Box::new(expr), BinOp::Mul, Box::new(right));
                continue;
            }
            if self.match_token(|k| matches!(k, TokenKind::Slash)) {
                let right = self.primary()?;
                expr = Expr::Binary(Box::new(expr), BinOp::Div, Box::new(right));
                continue;
            }
            break;
        }
        Ok(expr)
    }

    fn primary(&mut self) -> Result<Expr, String> {
        if let Some(n) = self.match_number() {
            return Ok(Expr::Number(n));
        }
        if let Some(s) = self.match_string_owned() {
            return Ok(Expr::String(s));
        }
        if let Some(name) = self.match_ident_owned() {
            return Ok(Expr::Name(name));
        }
        if self.match_token(|k| matches!(k, TokenKind::LParen)) {
            let expr = self.expression()?;
            if !self.match_token(|k| matches!(k, TokenKind::RParen)) {
                let tok = self.peek();
                return Err(format!("Expected ')' at {}:{}", tok.line, tok.col));
            }
            return Ok(expr);
        }

        let tok = self.peek();
        Err(format!("Expected expression at {}:{}", tok.line, tok.col))
    }

    fn skip_newlines(&mut self) {
        while self.match_token(|k| matches!(k, TokenKind::Newline)) {}
    }

    fn check_eof(&self) -> bool {
        matches!(self.peek().kind, TokenKind::Eof)
    }

    fn consume_ident(&mut self, msg: &str) -> Result<String, String> {
        if let Some(name) = self.match_ident_owned() {
            return Ok(name);
        }
        let tok = self.peek();
        Err(format!("{} at {}:{}", msg, tok.line, tok.col))
    }

    fn consume_equal(&mut self, msg: &str) -> Result<(), String> {
        if self.match_token(|k| matches!(k, TokenKind::Equal)) {
            return Ok(());
        }
        let tok = self.peek();
        Err(format!("{} at {}:{}", msg, tok.line, tok.col))
    }

    fn peek_ident_owned(&self) -> Option<String> {
        match &self.peek().kind {
            TokenKind::Ident(name) => Some(name.clone()),
            _ => None,
        }
    }

    fn peek_next_is_equal(&self) -> bool {
        if self.i + 1 >= self.tokens.len() {
            return false;
        }
        matches!(self.tokens[self.i + 1].kind, TokenKind::Equal)
    }

    fn match_ident_owned(&mut self) -> Option<String> {
        match &self.peek().kind {
            TokenKind::Ident(name) => {
                let name = name.clone();
                self.advance();
                Some(name)
            }
            _ => None,
        }
    }

    fn match_string_owned(&mut self) -> Option<String> {
        match &self.peek().kind {
            TokenKind::String(s) => {
                let s = s.clone();
                self.advance();
                Some(s)
            }
            _ => None,
        }
    }

    fn match_number(&mut self) -> Option<f64> {
        match self.peek().kind {
            TokenKind::Number(n) => {
                self.advance();
                Some(n)
            }
            _ => None,
        }
    }

    fn match_token<F>(&mut self, f: F) -> bool
    where
        F: Fn(&TokenKind) -> bool,
    {
        if f(&self.peek().kind) {
            self.advance();
            return true;
        }
        false
    }

    fn peek(&self) -> &Token {
        &self.tokens[self.i]
    }

    fn advance(&mut self) {
        if self.i + 1 < self.tokens.len() {
            self.i += 1;
        }
    }
}
