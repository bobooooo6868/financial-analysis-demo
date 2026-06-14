# One-command setup for Windows (PowerShell)
# Usage: .\setup.ps1 [-RunDemo]

param(
    [switch]$RunDemo
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "==> Creating virtual environment (.venv) ..."
if (-not (Test-Path .venv)) {
    py -3.12 -m venv .venv
}

Write-Host "==> Installing dependencies ..."
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\pip.exe install -r requirements.txt
if (Test-Path requirements-dev.txt) {
    .\.venv\Scripts\pip.exe install -r requirements-dev.txt
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "  Activate:  .\.venv\Scripts\Activate.ps1"
Write-Host "  Demo run:  .\.venv\Scripts\python.exe main.py --demo"
Write-Host "  Tests:     .\.venv\Scripts\pytest.exe tests/"

if ($RunDemo) {
    Write-Host ""
    Write-Host "==> Running demo pipeline ..."
    .\.venv\Scripts\python.exe main.py --demo
}
