# Drops the StudentEnrolments table from the DynamoDB Local container (.env.local).
# Recreate and seed it afterwards with .\tools\SeedData.ps1
Set-Location (Join-Path $PSScriptRoot '..')
$env:APP_ENV = 'local'
.\.venv\Scripts\python -m src.drop_StudentEnrolments
exit $LASTEXITCODE
