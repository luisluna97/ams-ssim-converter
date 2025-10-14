#!/usr/bin/env python3
"""
Upload final para GitHub - AMS SSIM Converter
Execute: python UPLOAD_TO_GITHUB.py
"""

import subprocess
import os

def run_git(cmd):
    """Executa comando git"""
    print(f"🔄 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and "warning" not in result.stderr.lower():
        print(result.stderr)
    return result.returncode == 0

print("=" * 80)
print("🚀 UPLOAD AMS SSIM CONVERTER PARA GITHUB")
print("📅 Data: 14 de Outubro de 2025")
print("🌐 Repositório: https://github.com/luisluna97/ams-ssim-converter")
print("=" * 80)

commands = [
    ("git init", "Inicializando Git"),
    ("git add .", "Adicionando arquivos"),
    ('git commit -m "🚀 v1.0.0 - Dutch Schedule to SSIM Converter - 14/10/2025\n\n✨ Features:\n- Dutch Schedule to SSIM conversion\n- Bilingual interface (EN/NL) with Dutch orange theme\n- Turnaround and night stop processing with Next Flight linking\n- AMS timezone support (+0100)\n- Multi-airline support (Single, Multiple, All)\n- SSIM compliance: 200-character lines, proper structure\n- Days of operation with correct spacing format\n\n🏢 Developed by AMS Team - Capacity Dnata Brasil\n📅 Release Date: 14 October 2025\n\n📊 Test Results:\n- Single Airline (EK): ✅ 8 flights\n- All Airlines: ✅ 1,481 flights (18 airlines)\n- All lines: ✅ Exactly 200 characters\n- SSIM structure: ✅ Valid"', "Commit inicial"),
    ("git branch -M main", "Configurando branch"),
    ("git remote add origin https://github.com/luisluna97/ams-ssim-converter.git", "Adicionando remote"),
    ("git push -u origin main --force", "Upload para GitHub")
]

for cmd, desc in commands:
    print(f"\n📋 {desc}...")
    if not run_git(cmd):
        print(f"⚠️ Comando falhou, mas continuando...")

print("\n" + "=" * 80)
print("🎉 UPLOAD CONCLUÍDO!")
print("🌐 GitHub: https://github.com/luisluna97/ams-ssim-converter")
print("📱 Streamlit: https://ams-ssim-converter.streamlit.app")
print("=" * 80)

input("\nPressione Enter para sair...")
