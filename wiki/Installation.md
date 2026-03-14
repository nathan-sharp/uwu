# Installation

The PAWS runtime is distributed as a single self-contained binary. No separate Python installation is required to run `.uwu` programs.

## One-line install

Open a terminal and paste the command for your platform.

### Linux / macOS

```sh
curl -fsSL https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.sh | sh
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.ps1 | iex
```

The installer will:

1. Detect your OS and CPU architecture automatically.
2. Download the correct pre-built `paws` binary from the [latest GitHub release](https://github.com/nathan-sharp/uwu/releases/latest).
3. Place the binary in `~/.local/bin` (Linux/macOS) or `%USERPROFILE%\.local\bin` (Windows).
4. On Windows the install directory is added to your `PATH` automatically. On Linux/macOS the script prints the one-liner needed to add it.

### Verify the install

```sh
paws version
paws run examples/hello.uwu
```

## Updating

```sh
paws update
```

`paws update` compares the installed version against the latest GitHub release and replaces the binary in-place if a newer version is available. It also removes any files left over from an older install layout.

## Uninstalling

```sh
paws uninstall
```

This removes the `paws` binary and any PAWS-managed local files. After uninstalling, delete the `~/.local/bin` entry from your `PATH` if no other tools use that directory.

## Building from source

Requires **Python 3.10+**.

### Build the standalone binary

```sh
python install.py
```

### Dev / editable install (no binary compilation)

```sh
python -m pip install -e .
python -m uwu.cli run examples/hello.uwu
```

### Experimental Rust runtime

An alternative native implementation lives in `runtime/` and can be built with standard Rust tooling:

```sh
cd runtime
cargo build --release
```
