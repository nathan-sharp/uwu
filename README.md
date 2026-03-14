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

## Installing the PAWS Runtime

Open your terminal, paste **one command**, and you're done.  
No repo cloning, no Python, no package managers — just a single native binary.

**Linux / macOS**
```sh
curl -fsSL https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.sh | sh
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.ps1 | iex
```

The script will:
1. Detect your OS and architecture automatically
2. Download the pre-built `paws` binary from the [latest GitHub Release](https://github.com/nathan-sharp/uwu/releases/latest)
3. Place it in `~/.local/bin` (Linux/macOS) or `%USERPROFILE%\.local\bin` (Windows)
4. Add that directory to your PATH — on Windows this happens automatically; on Linux/macOS the script prints the one-line command to do it

**Verify the install:**
```sh
paws run examples/hello.uwu
```

After installation `paws` is a fully standalone executable. Python is not required to run `.uwu` programs.

---

## Quick start

```sh
paws run hello.uwu
```

## For contributors — building from source

Requires Python 3.10+. Builds the standalone binary from the local source tree:

```sh
python install.py
```

To build and test inside the Python dev path without compiling a binary:

```sh
python -m pip install -e .
python -m uwu.cli run examples/hello.uwu
```

## Optional: native Rust runtime track

An experimental native implementation also exists in `runtime/` and can be built with Rust tooling.

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
