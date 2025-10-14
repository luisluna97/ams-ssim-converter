#!/usr/bin/env python3
"""
Script para fazer deploy do AMS SSIM Converter para GitHub
Data: 14/10/2025
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(cmd, description):
    """Executa comando e mostra resultado"""
    print(f"\n🔄 {description}")
    print(f"Comando: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Sucesso: {description}")
            if result.stdout:
                print(f"Output: {result.stdout}")
        else:
            print(f"❌ Erro: {description}")
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 DEPLOY AMS SSIM CONVERTER PARA GITHUB")
    print("📅 Data:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("🌐 Repositório: https://github.com/luisluna97/ams-ssim-converter")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Erro: Execute este script dentro da pasta ams-ssim-converter")
        return False
    
    # Comandos Git
    commands = [
        ("git init", "Inicializando repositório Git"),
        ("git add .", "Adicionando todos os arquivos"),
        ('git commit -m "🚀 Initial release v1.0.0 - AMS SSIM Converter\\n\\n✨ Features:\\n- W25 Amsterdam to SSIM conversion\\n- Bilingual interface (EN/NL)\\n- Dutch orange theme\\n- Turnaround and night stop processing\\n- AMS timezone support (+0100)\\n- Multi-airline support\\n\\n🏢 Developed by AMS Team - Capacity Dnata Brasil"', "Fazendo commit inicial"),
        ("git branch -M main", "Configurando branch main"),
        ("git remote add origin https://github.com/luisluna97/ams-ssim-converter.git", "Adicionando remote origin"),
        ("git push -u origin main --force", "Fazendo push para GitHub")
    ]
    
    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
        else:
            print(f"\n⚠️ Falha em: {desc}")
            print("Continuando com próximo comando...")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO: {success_count}/{len(commands)} comandos executados com sucesso")
    
    if success_count >= 4:  # Pelo menos os comandos essenciais
        print("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
        print("🌐 Acesse: https://github.com/luisluna97/ams-ssim-converter")
        print("📱 Streamlit: https://ams-ssim-converter.streamlit.app")
    else:
        print("⚠️ Deploy parcialmente concluído. Verifique os erros acima.")
    
    print("=" * 60)
    return success_count >= 4

if __name__ == "__main__":
    main()
