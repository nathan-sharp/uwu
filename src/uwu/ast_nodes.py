from dataclasses import dataclass


class Node:
    pass


@dataclass
class Program(Node):
    statements: list[Node]


@dataclass
class LetStmt(Node):
    name: str
    expr: Node


@dataclass
class AssignStmt(Node):
    name: str
    expr: Node


@dataclass
class PrintStmt(Node):
    expr: Node


@dataclass
class IfStmt(Node):
    condition: Node
    then_body: list[Node]
    else_body: list[Node]


@dataclass
class WhileStmt(Node):
    condition: Node
    body: list[Node]


@dataclass
class Number(Node):
    value: float


@dataclass
class String(Node):
    value: str


@dataclass
class Name(Node):
    value: str


@dataclass
class Binary(Node):
    left: Node
    op: str
    right: Node
