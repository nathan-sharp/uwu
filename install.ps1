# PAWS Runtime Installer — Windows (PowerShell)
# Usage: irm https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.ps1 | iex
#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

# Enforce TLS 1.2 for older PowerShell / .NET versions
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Repo   = "nathan-sharp/uwu"
$BinDir = Join-Path $HOME ".local\bin"
$BinName = "paws.exe"

# ── detect architecture ───────────────────────────────────────────────────────
$RuntimeArch = [System.Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture
$ArchKey = "x86_64"

if ($RuntimeArch -eq [System.Runtime.InteropServices.Architecture]::Arm64) {
    Write-Host "Windows ARM64 detected; using the x86_64 PAWS build via Windows emulation."
}

$Asset = "paws-windows-${ArchKey}.exe"
$Url   = "https://github.com/$Repo/releases/latest/download/$Asset"

# ── download ──────────────────────────────────────────────────────────────────
Write-Host "PAWS Runtime Installer"
Write-Host "Platform : windows/$ArchKey"
Write-Host "Downloading from $Url ..."

New-Item -ItemType Directory -Force -Path $BinDir | Out-Null

$Dest = Join-Path $BinDir $BinName
Invoke-WebRequest -Uri $Url -OutFile $Dest -UseBasicParsing

$LegacyDir = Join-Path $HOME ".paws"
$LegacyWrapper = Join-Path $BinDir "paws.bat"
if (Test-Path $LegacyWrapper) {
    Remove-Item -Force $LegacyWrapper
}
if (Test-Path $LegacyDir) {
    Remove-Item -Recurse -Force $LegacyDir
}

Write-Host "Installed  : $Dest"

# ── add to user PATH (persistent) ────────────────────────────────────────────
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$BinDir*") {
    $NewPath = $UserPath.TrimEnd(';') + ";$BinDir"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    # Also update the current session so the user can run paws immediately
    $env:Path = $env:Path.TrimEnd(';') + ";$BinDir"
    Write-Host ""
    Write-Host "Added $BinDir to your user PATH."
    Write-Host "(Restart any other open terminals to pick up the change.)"
}

Write-Host ""
Write-Host "Done. To verify: paws run <file.uwu>"
