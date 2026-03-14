# .uwu Language (Prototype)

This is an early prototype of a portable language runtime centered on `.uwu` source files.

Primary runtime: **PAWS Runtime**

- PAWS expansion: **Platform Agnostic Wrapper Service**
- Public meaning: a stable cross-platform execution utility

Current prototype supports:
- Variables (`let x = 10`)
- Reassignment (`x = x + 1`)
- Arithmetic (`+`, `-`, `*`, `/`)
- String and number literals
- `print` statements

## File extension
- Primary extension in this prototype: `.uwu`
- Formal expansion: **Universal Workload Unit**

## Quick start (standalone for end users, no Python required)

```bash
paws.exe run hello.uwu
```

## Build standalone runtime artifact (maintainer flow)

Build this once, then distribute `dist/paws.exe` to end users.

On Windows PowerShell:

```powershell
Set-Location .
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install pyinstaller
python -m PyInstaller --onefile --name paws --paths src src/uwu/cli.py
.\dist\paws.exe run .\examples\hello.uwu
```

## Optional: native Rust runtime track

An experimental native implementation also exists in `runtime/` and can be built with Rust tooling.

## Quick start (dev-only Python path)

```bash
python -m pip install -e .
python -m uwu.cli run examples/hello.uwu
```

## Example

```txt
let x = 2
let y = 3
print x + y * 10
print "uwu online"
```

## Status

This is phase-1 bootstrap code to start implementation. It is intentionally small and readable.

Current architecture includes two implementations:
- Native standalone runtime (`runtime/`) for end users
- Python implementation (`src/uwu/`) used to build/distribute `paws.exe`
