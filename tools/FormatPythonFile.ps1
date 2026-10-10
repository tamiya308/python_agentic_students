Set-Location (Join-Path $PSScriptRoot '..')
.\.venv\Scripts\ruff format src tests
exit $LASTEXITCODE