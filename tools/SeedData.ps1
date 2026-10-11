param([ValidateSet('local', 'dev')][string]$Env = 'local')
Set-Location (Join-Path $PSScriptRoot '..')
$env:APP_ENV = $Env
.\.venv\Scripts\python -m "src.seeds.seed_StudentEnrolments_$($Env.ToUpper())"
exit $LASTEXITCODE
