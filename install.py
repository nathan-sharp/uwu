#!/usr/bin/env python3
"""
PAWS Runtime Installer
======================
Compiles and installs the PAWS (Platform Agnostic Wrapper Service) runtime as a
fully standalone, self-contained native executable.

After installation Python is NOT required to run .uwu programs — only the
'paws' binary itself is needed.

Supports : Linux, macOS, Windows
Bootstrap : Python 3.10+  (used once to compile the binary, not at runtime)

Usage:
    python install.py
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ── constants ────────────────────────────────────────────────────────────────

MIN_PYTHON: tuple[int, int] = (3, 10)

_WIN = platform.system() == "Windows"
BINARY_NAME: str = "paws.exe" if _WIN else "paws"

# Where the standalone binary lands — one directory, one file.
INSTALL_DIR: Path = Path.home() / ".local" / "bin"


# ── helpers ──────────────────────────────────────────────────────────────────

def _scripts(venv: Path) -> Path:
    return venv / ("Scripts" if _WIN else "bin")


def _exe(venv: Path, name: str) -> Path:
    return _scripts(venv) / (f"{name}.exe" if _WIN else name)


def _run(*cmd, **kwargs) -> None:
    subprocess.run([str(c) for c in cmd], check=True, **kwargs)


def _die(msg: str) -> None:
    print(f"\nError: {msg}", file=sys.stderr)
    sys.exit(1)


# ── steps ────────────────────────────────────────────────────────────────────

def check_python() -> None:
    if sys.version_info < MIN_PYTHON:
        _die(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required "
            f"(found {sys.version_info.major}.{sys.version_info.minor})."
        )


def build_standalone(source_dir: Path, build_dir: Path) -> Path:
    """
    Creates a throw-away venv, installs PyInstaller + the uwu-lang package into
    it, compiles a --onefile binary, and returns the path to that binary.
    The venv and all intermediate build artefacts live inside build_dir and are
    deleted automatically when the caller's TemporaryDirectory context exits.
    """
    venv = build_dir / "venv"
    pip = _exe(venv, "pip")
    python = _exe(venv, "python")
    dist = build_dir / "dist"

    print("  Setting up build environment ...")
    _run(sys.executable, "-m", "venv", venv)

    print("  Installing build tools (PyInstaller) ...")
    _run(pip, "install", "--quiet", "pyinstaller")

    print("  Installing PAWS package ...")
    _run(pip, "install", "--quiet", source_dir)

    print("  Compiling standalone binary (this may take a minute) ...")
    _run(
        python, "-m", "PyInstaller",
        "--onefile",
        "--name", "paws",
        "--distpath", dist,
        "--workpath", build_dir / "work",
        "--specpath", build_dir,
        "--paths", source_dir / "src",
        "--noconfirm",
        "--log-level", "WARN",
        source_dir / "src" / "uwu" / "cli.py",
    )

    binary = dist / BINARY_NAME
    if not binary.exists():
        _die(f"Compilation succeeded but binary not found at: {binary}")
    return binary


def install_binary(binary: Path) -> Path:
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    dest = INSTALL_DIR / BINARY_NAME
    shutil.copy2(binary, dest)
    if not _WIN:
        dest.chmod(0o755)
    print(f"  Installed : {dest}")
    return dest


def print_path_instructions() -> None:
    on_path = str(INSTALL_DIR) in os.environ.get("PATH", "").split(os.pathsep)
    if on_path:
        return

    print()
    print("  Add the install directory to your PATH:")
    print()
    if _WIN:
        print("  PowerShell — run once, then restart your shell:")
        print(
            f'    [Environment]::SetEnvironmentVariable('
            f'"Path", $env:Path + ";{INSTALL_DIR}", "User")'
        )
        print()
        print("  Or: Settings → System → Advanced system settings →")
        print(f"      Environment Variables → append  {INSTALL_DIR}  to user PATH")
    else:
        home = Path.home()
        if (home / ".zshrc").exists():
            rc = "~/.zshrc"
        elif (home / ".bashrc").exists():
            rc = "~/.bashrc"
        else:
            rc = "~/.profile"
        print(f"  Run once, then restart your shell:")
        print(f'    echo \'export PATH="$HOME/.local/bin:$PATH"\' >> {rc}')
        print(f"    source {rc}")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("PAWS Runtime Installer")
    print("======================")
    print(f"Platform : {platform.system()} {platform.machine()}")
    print(f"Python   : {sys.version.split()[0]}  (bootstrap only — not needed after install)")
    print()

    check_python()

    source_dir = Path(__file__).resolve().parent

    # All build artefacts (venv, PyInstaller work dir, spec file) go into a
    # temporary directory that is removed automatically on exit.
    with tempfile.TemporaryDirectory(prefix="paws_build_") as _tmp:
        build_dir = Path(_tmp)

        print("[1/2] Building standalone binary ...")
        binary = build_standalone(source_dir, build_dir)

        print("\n[2/2] Installing binary ...")
        install_binary(binary)

    # TemporaryDirectory cleaned up here; Python venv is gone.

    print()
    print("=" * 42)
    print("PAWS Runtime installed successfully.")
    print("=" * 42)
    print()
    print("'paws' is now a fully standalone executable.")
    print("Python is no longer required to run .uwu programs.")
    print_path_instructions()
    print()
    print("Verify:")
    print("  paws run examples/hello.uwu")
    print()


if __name__ == "__main__":
    main()
