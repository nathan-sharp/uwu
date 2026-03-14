# UWU Language — Wiki Home

Welcome to the **UWU language** wiki. UWU is a small, portable scripting language whose programs are stored in `.uwu` source files and executed by the **PAWS Runtime** (**P**latform **A**gnostic **W**rapper **S**ervice).

## Pages

| Page | Description |
|------|-------------|
| [Installation](Installation) | Install the PAWS runtime on Linux, macOS, or Windows |
| [Getting Started](Getting-Started) | Write and run your first `.uwu` program |
| [Language Reference](Language-Reference) | Complete syntax and semantics guide |
| [Examples](Examples) | Annotated example programs |

## Quick links

- **Repository:** <https://github.com/nathan-sharp/uwu>
- **Latest release:** <https://github.com/nathan-sharp/uwu/releases/latest>

## What is UWU?

UWU is a phase-1 prototype of a portable language runtime. It intentionally stays small and readable so the implementation is easy to follow and extend. The current feature set covers:

- Number and string values
- Variable declaration (`let`) and reassignment
- Arithmetic and string concatenation (`+`, `-`, `*`, `/`, `%`)
- Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`)
- `print` for output
- `if` / `else` / `end` branching
- `while` / `end` loops

## Architecture

UWU ships two parallel implementations:

| Track | Location | Purpose |
|-------|----------|---------|
| Python | `src/uwu/` | Reference implementation; also used to build the distributable `paws` binary via PyInstaller |
| Rust (experimental) | `runtime/` | Native runtime track for end users |

The Python pipeline is: **source → Lexer → Parser → AST → Compiler → Bytecode → VM**.
