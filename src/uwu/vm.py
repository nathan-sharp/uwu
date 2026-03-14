from uwu.bytecode import Chunk
from uwu.errors import RuntimeErrorM
from uwu.types import Operand


Value = Operand


class VM:
    def __init__(self) -> None:
        self.stack: list[Value] = []
        self.globals: dict[str, Value] = {}

    def run(self, chunk: Chunk) -> None:
        ip = 0
        while ip < len(chunk.code):
            ins = chunk.code[ip]
            ip += 1

            if ins.op == "LOAD_CONST":
                if ins.arg is None:
                    raise RuntimeErrorM("Invalid bytecode: LOAD_CONST missing operand")
                self.stack.append(ins.arg)
                continue
            if ins.op == "LOAD_NAME":
                name = str(ins.arg)
                if name not in self.globals:
                    raise RuntimeErrorM(f"Undefined variable '{name}'")
                self.stack.append(self.globals[name])
                continue
            if ins.op == "STORE_NAME":
                self.globals[str(ins.arg)] = self._pop()
                continue
            if ins.op == "BINARY_ADD":
                b = self._pop()
                a = self._pop()
                self.stack.append(self._add(a, b))
                continue
            if ins.op == "BINARY_SUB":
                b = self._pop()
                a = self._pop()
                self.stack.append(self._arith(a, b, "-"))
                continue
            if ins.op == "BINARY_MUL":
                b = self._pop()
                a = self._pop()
                self.stack.append(self._arith(a, b, "*"))
                continue
            if ins.op == "BINARY_DIV":
                b = self._pop()
                a = self._pop()
                self.stack.append(self._arith(a, b, "/"))
                continue
            if ins.op == "BINARY_MOD":
                b = self._pop()
                a = self._pop()
                self.stack.append(self._arith(a, b, "%"))
                continue
            if ins.op == "COMPARE_EQ":
                b = self._pop()
                a = self._pop()
                self.stack.append(1.0 if a == b else 0.0)
                continue
            if ins.op == "COMPARE_NE":
                b = self._pop()
                a = self._pop()
                self.stack.append(1.0 if a != b else 0.0)
                continue
            if ins.op == "COMPARE_LT":
                b = self._pop()
                a = self._pop()
                self.stack.append(1.0 if self._cmp(a, b, "<") else 0.0)
                continue
            if ins.op == "COMPARE_LTE":
                b = self._pop()
                a = self._pop()
                self.stack.append(1.0 if self._cmp(a, b, "<=") else 0.0)
                continue
            if ins.op == "COMPARE_GT":
                b = self._pop()
                a = self._pop()
                self.stack.append(1.0 if self._cmp(a, b, ">") else 0.0)
                continue
            if ins.op == "COMPARE_GTE":
                b = self._pop()
                a = self._pop()
                self.stack.append(1.0 if self._cmp(a, b, ">=") else 0.0)
                continue
            if ins.op == "POP_JUMP_IF_FALSE":
                target = int(ins.arg) if ins.arg is not None else -1
                if target < 0:
                    raise RuntimeErrorM("Invalid bytecode: POP_JUMP_IF_FALSE missing target")
                if not self._is_truthy(self._pop()):
                    ip = target
                continue
            if ins.op == "JUMP":
                target = int(ins.arg) if ins.arg is not None else -1
                if target < 0:
                    raise RuntimeErrorM("Invalid bytecode: JUMP missing target")
                ip = target
                continue
            if ins.op == "PRINT":
                print(self._display_value(self._pop()))
                continue
            if ins.op == "RETURN":
                return

            raise RuntimeErrorM(f"Unknown opcode: {ins.op}")

    def _pop(self) -> Value:
        if not self.stack:
            raise RuntimeErrorM("Stack underflow")
        return self.stack.pop()

    def _add(self, a: Value, b: Value) -> Value:
        if isinstance(a, str) and isinstance(b, str):
            return a + b
        if isinstance(a, float) and isinstance(b, float):
            return a + b
        raise RuntimeErrorM("Type error: '+' expects two numbers or two strings")

    def _arith(self, a: Value, b: Value, op: str) -> float:
        if not isinstance(a, float) or not isinstance(b, float):
            raise RuntimeErrorM(f"Type error: '{op}' expects two numbers")
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return a / b
        if op == "%":
            return a % b
        raise RuntimeErrorM(f"Unknown arithmetic operation: {op}")

    def _cmp(self, a: Value, b: Value, op: str) -> bool:
        if isinstance(a, float) and isinstance(b, float):
            if op == "<":
                return a < b
            if op == "<=":
                return a <= b
            if op == ">":
                return a > b
            if op == ">=":
                return a >= b
        if isinstance(a, str) and isinstance(b, str):
            if op == "<":
                return a < b
            if op == "<=":
                return a <= b
            if op == ">":
                return a > b
            if op == ">=":
                return a >= b
        raise RuntimeErrorM(f"Type error: '{op}' expects two numbers or two strings")

    def _is_truthy(self, value: Value) -> bool:
        if isinstance(value, float):
            return value != 0.0
        if isinstance(value, str):
            return value != ""
        return bool(value)

    def _display_value(self, value: Value) -> Value:
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
