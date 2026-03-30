# start-backend.ps1
# Ativa o virtualenv e inicia o backend FastAPI
$venv = Join-Path $PWD '.venv\Scripts\python.exe'
if (-not (Test-Path $venv)) {
    Write-Error 'Virtualenv não encontrado em .venv. Execute primeiro `python -m venv .venv` e `pip install -r requirements.txt`.'
    exit 1
}

Write-Host 'Iniciando backend...' -ForegroundColor Green
Start-Process -NoNewWindow -FilePath $venv -ArgumentList '-m uvicorn backend.api:app --host 0.0.0.0 --port 5000 --reload' -WorkingDirectory $PWD
Write-Host 'Backend iniciado em http://localhost:5000' -ForegroundColor Green
