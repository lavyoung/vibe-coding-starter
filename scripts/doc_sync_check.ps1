Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "doc_sync_check.py"

$runtimes = @(
    @{ command = "python"; args = @() },
    @{ command = "py"; args = @("-3") },
    @{ command = "python3"; args = @() }
)

foreach ($runtime in $runtimes) {
    if (Get-Command $runtime.command -ErrorAction SilentlyContinue) {
        & $runtime.command @($runtime.args + @($pythonScript) + $args)
        exit $LASTEXITCODE
    }
}

Write-Error "No supported Python runtime found. Install python, py, or python3 and try again."
exit 1
