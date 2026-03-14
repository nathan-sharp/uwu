from uwu.errors import LexError
from uwu.tokens import KEYWORDS, Token


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.i = 0
        self.line = 1
        self.col = 1

    def lex(self) -> list[Token]:
        tokens: list[Token] = []
        while not self._eof():
            ch = self._peek()
            if ch in " \t\r":
                self._advance()
                continue
            if ch == "\n":
                tokens.append(self._token("NEWLINE", "\\n"))
                self._advance_line()
                continue
            if ch.isalpha() or ch == "_":
                tokens.append(self._identifier())
                continue
            if ch.isdigit():
                tokens.append(self._number())
                continue
            if ch == '"':
                tokens.append(self._string())
                continue

            start_line, start_col = self.line, self.col
            double = {
                "==": "EQEQ",
                "!=": "NOTEQ",
                "<=": "LTE",
                ">=": "GTE",
            }
            pair = self.source[self.i:self.i + 2]
            if pair in double:
                tokens.append(Token(double[pair], pair, start_line, start_col))
                self._advance()
                self._advance()
                continue

            single = {
                "(": "LPAREN",
                ")": "RPAREN",
                "+": "PLUS",
                "-": "MINUS",
                "*": "STAR",
                "/": "SLASH",
                "%": "PERCENT",
                "=": "EQUAL",
                "<": "LT",
                ">": "GT",
                ";": "NEWLINE",
            }
            kind = single.get(ch)
            if kind is None:
                raise LexError(f"Unexpected character '{ch}' at {start_line}:{start_col}")
            tokens.append(Token(kind, ch, start_line, start_col))
            self._advance()

        tokens.append(Token("EOF", "", self.line, self.col))
        return tokens

    def _identifier(self) -> Token:
        start_i = self.i
        line, col = self.line, self.col
        while not self._eof() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        value = self.source[start_i:self.i]
        kind = KEYWORDS.get(value, "IDENT")
        return Token(kind, value, line, col)

    def _number(self) -> Token:
        start_i = self.i
        line, col = self.line, self.col
        saw_dot = False
        while not self._eof():
            ch = self._peek()
            if ch == "." and not saw_dot:
                saw_dot = True
                self._advance()
                continue
            if not ch.isdigit():
                break
            self._advance()
        value = self.source[start_i:self.i]
        return Token("NUMBER", value, line, col)

    def _string(self) -> Token:
        line, col = self.line, self.col
        self._advance()  # opening quote
        chars: list[str] = []
        while not self._eof() and self._peek() != '"':
            ch = self._peek()
            if ch == "\\":
                self._advance()
                if self._eof():
                    break
                esc = self._peek()
                mapping = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
                chars.append(mapping.get(esc, esc))
                self._advance()
                continue
            if ch == "\n":
                raise LexError(f"Unterminated string at {line}:{col}")
            chars.append(ch)
            self._advance()
        if self._eof() or self._peek() != '"':
            raise LexError(f"Unterminated string at {line}:{col}")
        self._advance()  # closing quote
        return Token("STRING", "".join(chars), line, col)

    def _peek(self) -> str:
        return self.source[self.i]

    def _advance(self) -> None:
        self.i += 1
        self.col += 1

    def _advance_line(self) -> None:
        self.i += 1
        self.line += 1
        self.col = 1

    def _token(self, kind: str, value: str) -> Token:
        return Token(kind, value, self.line, self.col)

    def _eof(self) -> bool:
        return self.i >= len(self.source)
