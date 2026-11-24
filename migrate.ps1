$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$alembic = Join-Path $projectRoot '.venv\Scripts\alembic.exe'

if (-not (Test-Path -LiteralPath $alembic)) {
    throw "No se encontró Alembic en $alembic. Instala las dependencias con .\.venv\Scripts\pip.exe install -r requirements-dev.txt"
}

Push-Location $projectRoot
try {
    & $alembic upgrade head
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
