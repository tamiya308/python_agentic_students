Set-Location (Join-Path $PSScriptRoot '..')
.\.venv\Scripts\python -m pytest
exit $LASTEXITCODE
