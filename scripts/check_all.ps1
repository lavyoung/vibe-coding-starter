Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "check_all.py"
. (Join-Path $scriptDir "resolve_python_runtime.ps1")

$runtime = Resolve-PythonRuntime
if ($runtime) {
    & $runtime.command @($runtime.args + @($pythonScript) + $args)
    exit $LASTEXITCODE
}

Write-Error "No supported Python runtime found. Install python, py, or python3 and try again."
exit 1
