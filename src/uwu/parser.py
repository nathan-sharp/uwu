from uwu.ast_nodes import AssignStmt, Binary, IfStmt, LetStmt, Name, Number, PrintStmt, Program, String, WhileStmt
from uwu.errors import ParseError
from uwu.tokens import Token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def parse(self) -> Program:
        return Program(self._block("EOF"))

    def _block(self, *end_tokens: str):
        statements = []
        while not self._check("EOF", *end_tokens):
            self._skip_newlines()
            if self._check("EOF", *end_tokens):
                break
            statements.append(self._statement())
            self._skip_newlines()
        return statements

    def _statement(self):
        if self._match("LET"):
            name = self._consume("IDENT", "Expected identifier after 'let'")
            self._consume("EQUAL", "Expected '=' after variable name")
            expr = self._expression()
            return LetStmt(name.value, expr)

        if self._match("PRINT"):
            expr = self._expression()
            return PrintStmt(expr)

        if self._match("IF"):
            condition = self._expression()
            self._skip_newlines()
            then_body = self._block("ELSE", "END")
            else_body = []
            if self._match("ELSE"):
                self._skip_newlines()
                else_body = self._block("END")
            self._consume("END", "Expected 'end' to close if statement")
            return IfStmt(condition, then_body, else_body)

        if self._match("WHILE"):
            condition = self._expression()
            self._skip_newlines()
            body = self._block("END")
            self._consume("END", "Expected 'end' to close while statement")
            return WhileStmt(condition, body)

        if self._check("IDENT") and self._peek_next().kind == "EQUAL":
            name = self._advance()
            self._advance()  # equal token
            expr = self._expression()
            return AssignStmt(name.value, expr)

        tok = self._peek()
        raise ParseError(f"Unexpected token '{tok.kind}' at {tok.line}:{tok.col}")

    def _expression(self):
        return self._equality()

    def _equality(self):
        expr = self._comparison()
        while self._match("EQEQ", "NOTEQ"):
            op = self._prev().kind
            right = self._comparison()
            expr = Binary(expr, op, right)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match("LT", "LTE", "GT", "GTE"):
            op = self._prev().kind
            right = self._term()
            expr = Binary(expr, op, right)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match("PLUS", "MINUS"):
            op = self._prev().kind
            right = self._factor()
            expr = Binary(expr, op, right)
        return expr

    def _factor(self):
        expr = self._primary()
        while self._match("STAR", "SLASH", "PERCENT"):
            op = self._prev().kind
            right = self._primary()
            expr = Binary(expr, op, right)
        return expr

    def _primary(self):
        if self._match("NUMBER"):
            return Number(float(self._prev().value))
        if self._match("STRING"):
            return String(self._prev().value)
        if self._match("IDENT"):
            return Name(self._prev().value)
        if self._match("LPAREN"):
            expr = self._expression()
            self._consume("RPAREN", "Expected ')' after expression")
            return expr

        tok = self._peek()
        raise ParseError(f"Expected expression at {tok.line}:{tok.col}")

    def _skip_newlines(self) -> None:
        while self._match("NEWLINE"):
            pass

    def _match(self, *kinds: str) -> bool:
        if self._check(*kinds):
            self._advance()
            return True
        return False

    def _consume(self, kind: str, message: str) -> Token:
        if self._check(kind):
            return self._advance()
        tok = self._peek()
        raise ParseError(f"{message} at {tok.line}:{tok.col}")

    def _check(self, *kinds: str) -> bool:
        if self._is_at_end():
            return "EOF" in kinds
        return self._peek().kind in kinds

    def _peek(self) -> Token:
        return self.tokens[self.i]

    def _peek_next(self) -> Token:
        if self.i + 1 >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.i + 1]

    def _prev(self) -> Token:
        return self.tokens[self.i - 1]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.i += 1
        return self.tokens[self.i - 1]

    def _is_at_end(self) -> bool:
        return self._peek().kind == "EOF"
