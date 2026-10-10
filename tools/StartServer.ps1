Set-Location (Join-Path $PSScriptRoot '..')
.\.venv\Scripts\python -m uvicorn src.main:app --reload --port 3000
exit $LASTEXITCODE
