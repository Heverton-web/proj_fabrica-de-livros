# Script PowerShell para execução do resolvedor da obra oh-my
Write-Host "Iniciando processo de resolução de oh-my..." -ForegroundColor Green
python scripts/resolver_oh_my.py
python scripts/validar-artefatos.py --todos --estrito
Write-Host "Processo concluído com sucesso!" -ForegroundColor Green
