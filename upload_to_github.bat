@echo off
echo ========================================
echo 🚀 UPLOAD AMS SSIM CONVERTER PARA GITHUB
echo Data: 14/10/2025
echo ========================================

echo.
echo 1. Inicializando repositório Git...
git init

echo.
echo 2. Adicionando todos os arquivos...
git add .

echo.
echo 3. Fazendo commit inicial...
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

echo.
echo 4. Configurando branch main...
git branch -M main

echo.
echo 5. Adicionando remote origin...
git remote add origin https://github.com/luisluna97/ams-ssim-converter.git

echo.
echo 6. Fazendo push para GitHub (forçado)...
git push -u origin main --force

echo.
echo ========================================
echo 🎉 UPLOAD CONCLUÍDO!
echo 🌐 GitHub: https://github.com/luisluna97/ams-ssim-converter
echo 📱 Streamlit: https://ams-ssim-converter.streamlit.app
echo ========================================
pause
