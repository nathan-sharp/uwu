import argparse
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

from uwu import __version__
from uwu.compiler import Compiler
from uwu.errors import UwuError
from uwu.lexer import Lexer
from uwu.parser import Parser
from uwu.vm import VM

RUNTIME_NAME = "PAWS Runtime"
RUNTIME_EXPANSION = "Platform Agnostic Wrapper Service"
PROJECT_URL = "https://github.com/nathan-sharp/uwu"
LATEST_RELEASE_API = f"{PROJECT_URL}/releases/latest"
LATEST_RELEASE_JSON = "https://api.github.com/repos/nathan-sharp/uwu/releases/latest"
LEGACY_INSTALL_DIR = pathlib.Path.home() / ".paws"


def run_file(path: pathlib.Path) -> int:
    source = path.read_text(encoding="utf-8")
    tokens = Lexer(source).lex()
    program = Parser(tokens).parse()
    chunk = Compiler().compile(program)
    VM().run(chunk)
    return 0


def print_runtime_help(parser: argparse.ArgumentParser) -> int:
    parser.print_help()
    print()
    print("Commands:")
    print("  run <file.uwu>  Run a .uwu source file")
    print("  help            Show all PAWS commands and project links")
    print("  version         Show the current PAWS version")
    print("  update          Update PAWS from the latest GitHub release")
    print("  uninstall       Remove PAWS and all PAWS-managed local files")
    print()
    print(f"GitHub: {PROJECT_URL}")
    return 0


def print_version() -> int:
    print(f"paws {__version__}")
    return 0


def detect_release_asset() -> str:
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Linux":
        os_key = "linux"
    elif system == "Darwin":
        os_key = "macos"
    elif system == "Windows":
        os_key = "windows"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")

    if machine in {"x86_64", "amd64"}:
        arch_key = "x86_64"
    elif machine in {"aarch64", "arm64"}:
        arch_key = "x86_64" if os_key == "windows" else "aarch64"
    else:
        raise RuntimeError(f"Unsupported architecture: {machine}")

    suffix = ".exe" if os_key == "windows" else ""
    return f"paws-{os_key}-{arch_key}{suffix}"


def resolve_install_path() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys.executable).resolve()

    paws_on_path = shutil.which("paws")
    if paws_on_path:
        return pathlib.Path(paws_on_path).resolve()

    raise RuntimeError(
        "Could not locate the installed PAWS binary. Install PAWS first, then run 'paws update'."
    )


def cleanup_legacy_install(current_binary: pathlib.Path) -> None:
    legacy_paths = [
        LEGACY_INSTALL_DIR,
        pathlib.Path.home() / ".local" / "bin" / "paws.bat",
    ]

    current_text = str(current_binary.resolve())

    for path in legacy_paths:
        if not path.exists():
            continue
        if str(path.resolve()) == current_text:
            continue
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)


def discover_uninstall_targets(current_path: pathlib.Path | None) -> tuple[list[pathlib.Path], list[pathlib.Path]]:
    file_targets: set[pathlib.Path] = set()
    dir_targets: set[pathlib.Path] = {LEGACY_INSTALL_DIR}

    if os.name == "nt":
        basenames = ("paws.exe", "paws.bat", "paws.cmd", "paws")
    else:
        basenames = ("paws",)

    if current_path is not None:
        file_targets.add(current_path.resolve())

    # Common install locations that may not be on PATH in the current process.
    common_dirs = [
        pathlib.Path.home() / ".local" / "bin",
        pathlib.Path.home() / "bin",
    ]

    for directory in common_dirs:
        for base in basenames:
            candidate = (directory / base).expanduser()
            if candidate.exists() and candidate.is_file():
                file_targets.add(candidate.resolve())

    for raw_dir in os.environ.get("PATH", "").split(os.pathsep):
        if not raw_dir:
            continue
        path_dir = pathlib.Path(raw_dir).expanduser()
        for base in basenames:
            candidate = path_dir / base
            if candidate.exists() and candidate.is_file():
                file_targets.add(candidate.resolve())

    return sorted(file_targets), sorted(dir_targets)


def fetch_latest_release() -> tuple[str, str]:
    asset_name = detect_release_asset()
    request = urllib.request.Request(
        LATEST_RELEASE_JSON,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"paws/{__version__}",
        },
    )

    with urllib.request.urlopen(request) as response:
        payload = json.load(response)

    latest_version = str(payload["tag_name"]).lstrip("v")
    for asset in payload.get("assets", []):
        if asset.get("name") == asset_name:
            return latest_version, asset["browser_download_url"]

    raise RuntimeError(
        f"No release asset named '{asset_name}' was found in the latest GitHub release."
    )


def download_binary(download_url: str, target: pathlib.Path) -> pathlib.Path:
    request = urllib.request.Request(
        download_url,
        headers={"User-Agent": f"paws/{__version__}"},
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=target.suffix) as temp_file:
        temp_path = pathlib.Path(temp_file.name)

    try:
        with urllib.request.urlopen(request) as response, temp_path.open("wb") as dst:
            shutil.copyfileobj(response, dst)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise

    if os.name != "nt":
        temp_path.chmod(0o755)
    return temp_path


def quote_powershell(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def stage_windows_update(temp_path: pathlib.Path, target_path: pathlib.Path) -> None:
    script_path = pathlib.Path(tempfile.mkstemp(suffix=".ps1")[1])
    legacy_dir = quote_powershell(str(LEGACY_INSTALL_DIR))
    legacy_wrapper = quote_powershell(str(pathlib.Path.home() / ".local" / "bin" / "paws.bat"))
    temp_literal = quote_powershell(str(temp_path))
    target_literal = quote_powershell(str(target_path))
    script_literal = quote_powershell(str(script_path))

    script = f"""$ErrorActionPreference = 'Stop'
Start-Sleep -Milliseconds 750
for ($i = 0; $i -lt 120; $i++) {{
    try {{
        Move-Item -Force {temp_literal} {target_literal}
        break
    }} catch {{
        Start-Sleep -Milliseconds 500
    }}
}}
if (Test-Path {legacy_wrapper}) {{
    Remove-Item -Force {legacy_wrapper}
}}
if (Test-Path {legacy_dir}) {{
    Remove-Item -Recurse -Force {legacy_dir}
}}
Remove-Item -Force {script_literal} -ErrorAction SilentlyContinue
"""
    script_path.write_text(script, encoding="utf-8")

    creationflags = 0
    creationflags |= getattr(subprocess, "DETACHED_PROCESS", 0)
    creationflags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

    subprocess.Popen(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
        close_fds=True,
    )


def stage_windows_uninstall(file_targets: list[pathlib.Path], dir_targets: list[pathlib.Path]) -> None:
    script_path = pathlib.Path(tempfile.mkstemp(suffix=".ps1")[1])
    script_literal = quote_powershell(str(script_path))
    files_literal = "\n".join(f"    {quote_powershell(str(path))}" for path in file_targets)
    dirs_literal = "\n".join(f"    {quote_powershell(str(path))}" for path in dir_targets)

    if not files_literal:
        files_literal = "    ''"
    if not dirs_literal:
        dirs_literal = "    ''"

    script = f"""$ErrorActionPreference = 'Stop'
Start-Sleep -Milliseconds 750
$files = @(
{files_literal}
)
$dirs = @(
{dirs_literal}
)
foreach ($dir in $dirs) {{
    if ($dir -and (Test-Path $dir)) {{
        Remove-Item -Recurse -Force $dir
    }}
}}
foreach ($file in $files) {{
    if (-not $file) {{
        continue
    }}
    for ($i = 0; $i -lt 120; $i++) {{
        try {{
            if (Test-Path $file) {{
                Remove-Item -Force $file
            }}
            break
        }} catch {{
            Start-Sleep -Milliseconds 500
        }}
    }}
}}
Remove-Item -Force {script_literal} -ErrorAction SilentlyContinue
"""
    script_path.write_text(script, encoding="utf-8")

    creationflags = 0
    creationflags |= getattr(subprocess, "DETACHED_PROCESS", 0)
    creationflags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

    subprocess.Popen(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
        close_fds=True,
    )


def uninstall_runtime() -> int:
    try:
        current_path = resolve_install_path()
    except RuntimeError:
        current_path = None

    file_targets, dir_targets = discover_uninstall_targets(current_path)

    if os.name == "nt":
        stage_windows_uninstall(file_targets, dir_targets)
        print("PAWS uninstall staged.")
        print("Close this process and open a new shell to verify 'paws' is gone.")
        return 0

    removed_files = 0
    removed_dirs = 0

    for path in file_targets:
        if path.exists() and path.is_file():
            path.unlink(missing_ok=True)
            removed_files += 1

    for path in dir_targets:
        if path.exists() and path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
            removed_dirs += 1

    print(f"PAWS uninstalled. Removed {removed_files} file(s) and {removed_dirs} directory(ies).")
    return 0


def update_runtime() -> int:
    current_path = resolve_install_path()
    current_version = __version__
    latest_version, download_url = fetch_latest_release()

    print(f"Current version : {current_version}")
    print(f"Latest version  : {latest_version}")

    if latest_version == current_version:
        cleanup_legacy_install(current_path)
        print("PAWS is already up to date.")
        return 0

    print(f"Downloading update from {LATEST_RELEASE_API} ...")
    temp_path = download_binary(download_url, current_path)

    if os.name == "nt":
        stage_windows_update(temp_path, current_path)
        print("Update staged. PAWS will replace itself after this process exits.")
        print("Run 'paws version' again in a fresh shell to confirm the new version.")
        return 0

    os.replace(temp_path, current_path)
    cleanup_legacy_install(current_path)
    print(f"Updated PAWS to version {latest_version}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="paws",
        description=f"{RUNTIME_NAME} ({RUNTIME_EXPANSION})",
    )
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="Run a .uwu source file")
    run_parser.add_argument("file", type=pathlib.Path)
    sub.add_parser("help", help="Show all PAWS commands and project links")
    sub.add_parser("version", help="Show the current PAWS version")
    sub.add_parser("update", help="Update PAWS from the latest GitHub release")
    sub.add_parser("uninstall", help="Remove PAWS and all PAWS-managed local files")

    args = parser.parse_args()

    try:
        if args.command in {None, "help"}:
            return print_runtime_help(parser)
        if args.command == "version":
            return print_version()
        if args.command == "update":
            return update_runtime()
        if args.command == "uninstall":
            return uninstall_runtime()
        if args.command == "run":
            return run_file(args.file)
        return print_runtime_help(parser)
    except FileNotFoundError:
        print(f"{RUNTIME_NAME} error: File not found: {args.file}", file=sys.stderr)
        return 2
    except UwuError as exc:
        print(f"{RUNTIME_NAME} error: {exc}", file=sys.stderr)
        return 3
    except (OSError, RuntimeError, urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        print(f"{RUNTIME_NAME} error: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
