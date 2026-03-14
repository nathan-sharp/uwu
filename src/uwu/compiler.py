from uwu.ast_nodes import AssignStmt, Binary, LetStmt, Name, Number, PrintStmt, Program, String
from uwu.bytecode import Chunk
from uwu.errors import UwuError


class CompileError(UwuError):
    pass


class Compiler:
    def compile(self, program: Program) -> Chunk:
        chunk = Chunk()
        for stmt in program.statements:
            self._emit_stmt(chunk, stmt)
        chunk.emit("RETURN")
        return chunk

    def _emit_stmt(self, chunk: Chunk, stmt) -> None:
        if isinstance(stmt, LetStmt):
            self._emit_expr(chunk, stmt.expr)
            chunk.emit("STORE_NAME", stmt.name)
            return
        if isinstance(stmt, AssignStmt):
            self._emit_expr(chunk, stmt.expr)
            chunk.emit("STORE_NAME", stmt.name)
            return
        if isinstance(stmt, PrintStmt):
            self._emit_expr(chunk, stmt.expr)
            chunk.emit("PRINT")
            return
        raise CompileError(f"Unsupported statement: {type(stmt).__name__}")

    def _emit_expr(self, chunk: Chunk, expr) -> None:
        if isinstance(expr, Number):
            chunk.emit("LOAD_CONST", expr.value)
            return
        if isinstance(expr, String):
            chunk.emit("LOAD_CONST", expr.value)
            return
        if isinstance(expr, Name):
            chunk.emit("LOAD_NAME", expr.value)
            return
        if isinstance(expr, Binary):
            self._emit_expr(chunk, expr.left)
            self._emit_expr(chunk, expr.right)
            op_map = {
                "PLUS": "BINARY_ADD",
                "MINUS": "BINARY_SUB",
                "STAR": "BINARY_MUL",
                "SLASH": "BINARY_DIV",
            }
            op = op_map.get(expr.op)
            if op is None:
                raise CompileError(f"Unsupported binary operator: {expr.op}")
            chunk.emit(op)
            return
        raise CompileError(f"Unsupported expression: {type(expr).__name__}")
