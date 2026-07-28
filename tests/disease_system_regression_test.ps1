$ErrorActionPreference = 'Stop'

$testPath = Join-Path $PSScriptRoot 'disease_system_regression_test.py'
$env:PYTHONDONTWRITEBYTECODE = '1'
& py -3 $testPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
