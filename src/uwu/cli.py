import argparse
import pathlib
import sys

from uwu.compiler import Compiler
from uwu.errors import UwuError
from uwu.lexer import Lexer
from uwu.parser import Parser
from uwu.vm import VM

RUNTIME_NAME = "PAWS Runtime"
RUNTIME_EXPANSION = "Platform Agnostic Wrapper Service"


def run_file(path: pathlib.Path) -> int:
    source = path.read_text(encoding="utf-8")
    tokens = Lexer(source).lex()
    program = Parser(tokens).parse()
    chunk = Compiler().compile(program)
    VM().run(chunk)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="paws",
        description=f"{RUNTIME_NAME} ({RUNTIME_EXPANSION})",
    )
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="Run a .uwu source file")
    run_parser.add_argument("file", type=pathlib.Path)

    args = parser.parse_args()

    if args.command != "run":
        parser.print_help()
        return 1

    try:
        return run_file(args.file)
    except FileNotFoundError:
        print(f"{RUNTIME_NAME} error: File not found: {args.file}", file=sys.stderr)
        return 2
    except UwuError as exc:
        print(f"{RUNTIME_NAME} error: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
