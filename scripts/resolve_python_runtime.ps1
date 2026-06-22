function Resolve-PythonRuntime {
    $py = Get-Command "py" -ErrorAction SilentlyContinue
    if ($py) {
        return @{
            command = $py.Source
            args = @("-3")
        }
    }

    foreach ($candidate in @("python", "python3")) {
        $paths = @(
            & where.exe $candidate 2>$null |
                Where-Object { $_ -and $_ -notmatch '\\WindowsApps\\' }
        )
        if ($paths.Count -gt 0) {
            return @{
                command = $paths[0]
                args = @()
            }
        }

        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command -and $command.Source -and $command.Source -notmatch '\\WindowsApps\\') {
            return @{
                command = $command.Source
                args = @()
            }
        }
    }

    return $null
}
