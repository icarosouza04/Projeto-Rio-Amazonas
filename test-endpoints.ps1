# test-endpoints.ps1
# Verifica se os endpoints e o dashboard retornam OK
$urls = @(
    'http://localhost:5000/api/estacoes',
    'http://localhost:5000/api/dados',
    'http://localhost:8000/frontend/public/dashboard.html'
)

Write-Host 'Testando endpoints...' -ForegroundColor Cyan
foreach ($u in $urls) {
    try {
        $res = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 5
        Write-Host "$u -> $($res.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "$u -> ERRO: $($_.Exception.Message)" -ForegroundColor Red
    }
}
