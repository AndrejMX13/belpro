# Loads variables from .env in the project root into the current PowerShell session.
# Run from any directory: . .\scripts\load_env.ps1
# Skips blank lines and comments. Strips surrounding quotes from values.

$envFile = Join-Path $PSScriptRoot "..\\.env"

if (-not (Test-Path $envFile)) {
    Write-Error ".env file not found at $envFile"
    exit 1
}

[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1")

$count = 0
foreach ($line in Get-Content $envFile) {
    if ($line -match '^\s*([^#][^=]*)=(.*)') {
        $key = $Matches[1].Trim()
        $value = $Matches[2].Trim().Trim('"').Trim("'")
        [System.Environment]::SetEnvironmentVariable($key, $value)
        $count++
    }
}

Write-Host "Loaded $count variables from .env"
