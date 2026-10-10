Set-Location (Join-Path $PSScriptRoot '..')
.\.venv\Scripts\python -m src.seeds.seed_StudentEnrolements
exit $LASTEXITCODE
