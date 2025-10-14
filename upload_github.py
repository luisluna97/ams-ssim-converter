#!/usr/bin/env python3
"""
Upload AMS SSIM Converter para GitHub
Execute: python upload_github.py
Data: 14/10/2025
"""

import subprocess
import os
import sys

def run_command(cmd):
    """Executa comando e mostra resultado"""
    print(f"🔄 Executando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 UPLOAD AMS SSIM CONVERTER PARA GITHUB")
    print("📅 Data: 14/10/2025")
    print("🌐 Repositório: https://github.com/luisluna97/ams-ssim-converter")
    print("=" * 60)
    
    # Verificar se Git está disponível
    if not run_command("git --version"):
        print("❌ Git não encontrado. Instale o Git primeiro.")
        return
    
    print("\n1. 🔧 Inicializando repositório Git...")
    run_command("git init")
    
    print("\n2. 📁 Adicionando todos os arquivos...")
    run_command("git add .")
    
    print("\n3. 💾 Fazendo commit inicial...")
    commit_msg = """🚀 Initial release v1.0.0 - AMS SSIM Converter - 14/10/2025

✨ Features:
- W25 Amsterdam to SSIM conversion
- Bilingual interface (EN/NL) 
- Dutch orange theme
- Turnaround and night stop processing
- AMS timezone support (+0100)
- Multi-airline support

🏢 Developed by AMS Team - Capacity Dnata Brasil
📅 Release Date: 14 October 2025"""
    
    run_command(f'git commit -m "{commit_msg}"')
    
    print("\n4. 🌿 Configurando branch main...")
    run_command("git branch -M main")
    
    print("\n5. 🔗 Adicionando remote origin...")
    run_command("git remote add origin https://github.com/luisluna97/ams-ssim-converter.git")
    
    print("\n6. 🚀 Fazendo push para GitHub...")
    success = run_command("git push -u origin main --force")
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 UPLOAD CONCLUÍDO COM SUCESSO!")
        print("🌐 GitHub: https://github.com/luisluna97/ams-ssim-converter")
        print("📱 Streamlit: https://ams-ssim-converter.streamlit.app")
    else:
        print("⚠️ Alguns comandos falharam. Verifique as mensagens acima.")
    print("=" * 60)

if __name__ == "__main__":
    main()
    input("\nPressione Enter para sair...")
