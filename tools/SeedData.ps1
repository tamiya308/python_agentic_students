Set-Location (Join-Path $PSScriptRoot '..')
.\.venv\Scripts\python -m src.seeds.seed_StudentEnrolments
exit $LASTEXITCODE
