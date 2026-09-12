param([string]$Python = 'python')
$env:PYTHONPATH = Join-Path $PSScriptRoot '../../src'
$env:PYTHONUTF8 = '1'
& $Python -B (Join-Path $PSScriptRoot 'run_reference_checks.py')
if ($LASTEXITCODE -ne 0) { throw 'Experiment or acceptance check failed' }
