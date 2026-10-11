Set-Location (Join-Path $PSScriptRoot '..')
.\.venv\Scripts\python -m uvicorn src.main:app --reload --port 3000 --log-level debug
exit $LASTEXITCODE
