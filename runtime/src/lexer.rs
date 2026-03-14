use crate::token::{Token, TokenKind};

pub fn lex(source: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let chars: Vec<char> = source.chars().collect();
    let mut i = 0usize;
    let mut line = 1usize;
    let mut col = 1usize;

    while i < chars.len() {
        let ch = chars[i];

        if ch == ' ' || ch == '\t' || ch == '\r' {
            i += 1;
            col += 1;
            continue;
        }

        if ch == '\n' {
            tokens.push(Token::new(TokenKind::Newline, line, col));
            i += 1;
            line += 1;
            col = 1;
            continue;
        }

        if ch.is_ascii_alphabetic() || ch == '_' {
            let start = i;
            let start_col = col;
            while i < chars.len() && (chars[i].is_ascii_alphanumeric() || chars[i] == '_') {
                i += 1;
                col += 1;
            }
            let value: String = chars[start..i].iter().collect();
            let kind = match value.as_str() {
                "let" => TokenKind::Let,
                "print" => TokenKind::Print,
                _ => TokenKind::Ident(value),
            };
            tokens.push(Token::new(kind, line, start_col));
            continue;
        }

        if ch.is_ascii_digit() {
            let start = i;
            let start_col = col;
            let mut saw_dot = false;
            while i < chars.len() {
                let c = chars[i];
                if c == '.' && !saw_dot {
                    saw_dot = true;
                    i += 1;
                    col += 1;
                    continue;
                }
                if !c.is_ascii_digit() {
                    break;
                }
                i += 1;
                col += 1;
            }
            let num_text: String = chars[start..i].iter().collect();
            let number = num_text
                .parse::<f64>()
                .map_err(|_| format!("Invalid number '{}' at {}:{}", num_text, line, start_col))?;
            tokens.push(Token::new(TokenKind::Number(number), line, start_col));
            continue;
        }

        if ch == '"' {
            let start_col = col;
            i += 1;
            col += 1;
            let mut out = String::new();
            while i < chars.len() && chars[i] != '"' {
                let c = chars[i];
                if c == '\\' {
                    i += 1;
                    col += 1;
                    if i >= chars.len() {
                        return Err(format!("Unterminated string at {}:{}", line, start_col));
                    }
                    let esc = chars[i];
                    match esc {
                        'n' => out.push('\n'),
                        't' => out.push('\t'),
                        '"' => out.push('"'),
                        '\\' => out.push('\\'),
                        _ => out.push(esc),
                    }
                    i += 1;
                    col += 1;
                    continue;
                }
                if c == '\n' {
                    return Err(format!("Unterminated string at {}:{}", line, start_col));
                }
                out.push(c);
                i += 1;
                col += 1;
            }
            if i >= chars.len() || chars[i] != '"' {
                return Err(format!("Unterminated string at {}:{}", line, start_col));
            }
            i += 1;
            col += 1;
            tokens.push(Token::new(TokenKind::String(out), line, start_col));
            continue;
        }

        let kind = match ch {
            '+' => TokenKind::Plus,
            '-' => TokenKind::Minus,
            '*' => TokenKind::Star,
            '/' => TokenKind::Slash,
            '=' => TokenKind::Equal,
            '(' => TokenKind::LParen,
            ')' => TokenKind::RParen,
            ';' => TokenKind::Newline,
            _ => return Err(format!("Unexpected character '{}' at {}:{}", ch, line, col)),
        };
        tokens.push(Token::new(kind, line, col));
        i += 1;
        col += 1;
    }

    tokens.push(Token::new(TokenKind::Eof, line, col));
    Ok(tokens)
}
