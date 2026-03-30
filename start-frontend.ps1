# start-frontend.ps1
# Inicia servidor HTTP estático para frontend
Write-Host 'Iniciando servidor estático...' -ForegroundColor Green
Start-Process -NoNewWindow -FilePath 'python' -ArgumentList '-m http.server 8000' -WorkingDirectory $PWD
Write-Host 'Frontend estático em http://localhost:8000/frontend/public/dashboard.html' -ForegroundColor Green
