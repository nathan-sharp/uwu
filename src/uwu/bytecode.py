from dataclasses import dataclass, field

from uwu.types import Operand


@dataclass
class Instruction:
    op: str
    arg: Operand | None = None


@dataclass
class Chunk:
    code: list[Instruction] = field(default_factory=list)

    def emit(self, op: str, arg: Operand | None = None) -> None:
        self.code.append(Instruction(op, arg))
