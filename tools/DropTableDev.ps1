# Drops the StudentEnrolments table from the AWS dev account (.env.dev, via AWS_PROFILE).
# This permanently deletes every record. Pass -Force to skip the confirmation prompt.
# Recreate and seed it afterwards with .\tools\SeedData.ps1 -Env dev
param([switch]$Force)
Set-Location (Join-Path $PSScriptRoot '..')
if (-not $Force) {
    $answer = Read-Host 'This permanently deletes the StudentEnrolments table and all its data on AWS (dev). Type StudentEnrolments to confirm'
    if ($answer -cne 'StudentEnrolments') {
        Write-Host 'Cancelled; nothing dropped.'
        exit 1
    }
}
$env:APP_ENV = 'dev'
.\.venv\Scripts\python -m src.drop_StudentEnrolments
exit $LASTEXITCODE
