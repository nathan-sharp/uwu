#!/bin/sh
# PAWS Runtime Installer — Linux & macOS
# Usage: curl -fsSL https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.sh | sh
set -e

REPO="nathan-sharp/uwu"
BIN_DIR="$HOME/.local/bin"
BIN_NAME="paws"

# ── detect OS ────────────────────────────────────────────────────────────────
OS="$(uname -s)"
case "$OS" in
  Linux*)  OS_KEY="linux"  ;;
  Darwin*) OS_KEY="macos"  ;;
  *)
    echo "Error: unsupported operating system: $OS" >&2
    exit 1
    ;;
esac

# ── detect architecture ──────────────────────────────────────────────────────
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64)        ARCH_KEY="x86_64"  ;;
  aarch64|arm64) ARCH_KEY="aarch64" ;;
  *)
    echo "Error: unsupported architecture: $ARCH" >&2
    exit 1
    ;;
esac

ASSET="paws-${OS_KEY}-${ARCH_KEY}"
URL="https://github.com/${REPO}/releases/latest/download/${ASSET}"

# ── download ─────────────────────────────────────────────────────────────────
echo "PAWS Runtime Installer"
echo "Platform : ${OS_KEY}/${ARCH_KEY}"
echo "Downloading from ${URL} ..."

mkdir -p "$BIN_DIR"

if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$URL" -o "$BIN_DIR/$BIN_NAME"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$BIN_DIR/$BIN_NAME" "$URL"
else
  echo "Error: curl or wget is required to download PAWS." >&2
  exit 1
fi

chmod +x "$BIN_DIR/$BIN_NAME"

# macOS: remove the quarantine flag that Gatekeeper sets on downloaded files
if [ "$OS_KEY" = "macos" ]; then
  xattr -d com.apple.quarantine "$BIN_DIR/$BIN_NAME" 2>/dev/null || true
fi

echo "Installed  : $BIN_DIR/$BIN_NAME"

# ── PATH instructions (only if needed) ───────────────────────────────────────
case ":${PATH}:" in
  *":${BIN_DIR}:"*) ;;
  *)
    echo ""
    echo "NOTE: $BIN_DIR is not on your PATH."
    echo "Run the following, then restart your shell:"
    echo ""

    if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
      RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
      RC="$HOME/.bashrc"
    else
      RC="$HOME/.profile"
    fi

    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> $RC"
    echo "  source $RC"
    echo ""
    ;;
esac

echo "Done. To verify: paws run <file.uwu>"
