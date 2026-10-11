param([ValidateSet('local', 'dev')][string]$Env = 'local')
Set-Location (Join-Path $PSScriptRoot '..')
$env:APP_ENV = $Env
.\.venv\Scripts\python -m uvicorn src.main:app --reload --port 3000
exit $LASTEXITCODE
