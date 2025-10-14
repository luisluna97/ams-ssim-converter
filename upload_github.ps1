Write-Host "========================================" -ForegroundColor Green
Write-Host "🚀 UPLOAD AMS SSIM CONVERTER PARA GITHUB" -ForegroundColor Green
Write-Host "Data: 14/10/2025" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

Write-Host ""
Write-Host "1. Inicializando repositório Git..." -ForegroundColor Cyan
git init

Write-Host ""
Write-Host "2. Adicionando todos os arquivos..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "3. Fazendo commit inicial..." -ForegroundColor Cyan
git commit -m "🚀 Initial release v1.0.0 - AMS SSIM Converter - 14/10/2025

✨ Features:
- W25 Amsterdam to SSIM conversion
- Bilingual interface (EN/NL) 
- Dutch orange theme
- Turnaround and night stop processing
- AMS timezone support (+0100)
- Multi-airline support

🏢 Developed by AMS Team - Capacity Dnata Brasil
📅 Release Date: 14 October 2025"

Write-Host ""
Write-Host "4. Configurando branch main..." -ForegroundColor Cyan
git branch -M main

Write-Host ""
Write-Host "5. Adicionando remote origin..." -ForegroundColor Cyan
git remote add origin https://github.com/luisluna97/ams-ssim-converter.git

Write-Host ""
Write-Host "6. Fazendo push para GitHub..." -ForegroundColor Cyan
git push -u origin main --force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 UPLOAD CONCLUÍDO!" -ForegroundColor Green
Write-Host "🌐 GitHub: https://github.com/luisluna97/ams-ssim-converter" -ForegroundColor Yellow
Write-Host "📱 Streamlit: https://ams-ssim-converter.streamlit.app" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

Read-Host "Pressione Enter para continuar"
