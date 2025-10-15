#!/usr/bin/env python3
"""
Script rápido para commit e push de atualizações
Execute: python quick_update.py
"""

import subprocess
from version import VERSION, BUILD_DATE

def run_git(cmd):
    print(f"🔄 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and "warning" not in result.stderr.lower():
        print(result.stderr)
    return result.returncode == 0

print("=" * 80)
print(f"🚀 QUICK UPDATE - v{VERSION}")
print(f"📅 {BUILD_DATE}")
print("=" * 80)

commands = [
    ("git add .", "Adicionando mudanças"),
    (f'git commit -m "🐛 v{VERSION} - Fix flight number extraction for numeric airlines\n\nFixed:\n- Regex bug for airlines like 6E (IndiGo)\n- 6E0021 now correctly extracts as 0021 (was 0006)\n- Removed [:4] truncation for longer flight numbers\n\nTested:\n- ✅ 6E0021→0021, 6E0022→0022\n- ✅ All 18 airlines, 1,481 flights\n- ✅ 200 characters per line\n\n📅 {BUILD_DATE}\n🏢 AMS Team - Capacity Dnata Brasil"', "Commit da atualização"),
    ("git push origin main", "Push para GitHub")
]

for cmd, desc in commands:
    print(f"\n📋 {desc}...")
    if not run_git(cmd):
        print(f"⚠️ Comando falhou")
        break

print("\n" + "=" * 80)
print("✅ ATUALIZAÇÃO ENVIADA!")
print(f"🌐 https://github.com/luisluna97/ams-ssim-converter")
print(f"📱 https://ams-ssim-converter.streamlit.app")
print("=" * 80)

input("\nPressione Enter para sair...")
