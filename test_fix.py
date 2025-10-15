#!/usr/bin/env python3
"""
Testar se a correção funcionou
"""

import re

# Nova função
def extrair_numero_voo(flight_number):
    """Extrai número do voo - CORRIGIDO"""
    if flight_number == 'N/S' or not flight_number:
        return None
    flight_str = str(flight_number).strip().upper()
    # Pular letras iniciais e pegar números (ex: 6E0021 → 0021)
    match = re.search(r'^[A-Z]*([0-9]+)', flight_str)
    if match:
        numero = match.group(1)
        print(f"  '{flight_str}' → regex capturou: '{numero}' → zfill(4): '{numero.zfill(4)}'")
        return numero.zfill(4)
    return None

print("TESTE DA FUNÇÃO CORRIGIDA:")
print("=" * 80)

test_cases = ['6E0021', '6E0022', 'AI155', 'LH1002', 'EK0145']

for flight in test_cases:
    result = extrair_numero_voo(flight)
    print(f"{flight:10s} → {result}")

print()
print("=" * 80)
print("Esperado:")
print("6E0021 → 0021")
print("6E0022 → 0022")
print("=" * 80)

# Importar do módulo e testar
print("\nTestando função do módulo:")
from w25_to_ssim_converter import extrair_numero_voo as extrair_modulo

for flight in ['6E0021', '6E0022']:
    result = extrair_modulo(flight)
    print(f"{flight} → {result}")
