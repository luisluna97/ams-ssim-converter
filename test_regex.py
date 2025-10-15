#!/usr/bin/env python3
"""
Testar regex de extração
"""

import re

def extrair_numero_voo_ATUAL(flight_number):
    """Função atual com problema"""
    flight_str = str(flight_number).strip().upper()
    print(f"  Input: '{flight_number}' → String: '{flight_str}'")
    
    match = re.search(r'([0-9]+)', flight_str)
    if match:
        numero = match.group(1)
        print(f"  Regex encontrou: '{numero}'")
        resultado = numero.zfill(4)[:4]
        print(f"  Após zfill(4)[:4]: '{resultado}'")
        return resultado
    return None

print("TESTE DA FUNÇÃO ATUAL:")
print("=" * 80)

test_cases = ['6E0021', '6E0022', 'AI155', 'LH1002', 'EK0145']

for flight in test_cases:
    print(f"\n{flight}:")
    result = extrair_numero_voo_ATUAL(flight)
    print(f"  RESULTADO FINAL: '{result}'")

print()
print("=" * 80)
print("PROBLEMA:")
print("A regex r'([0-9]+)' pega TODOS os dígitos consecutivos")
print("Em '6E0021': pega '0021' (4 dígitos)")
print("Mas zfill(4)[:4] trunca em 4 caracteres")
print("'0021'.zfill(4) = '0021'")
print("'0021'[:4] = '0021'")
print()
print("Isso está CORRETO!")
print()
print("O problema deve estar em outro lugar...")
print("Vou verificar se '6E0021' está sendo lido como 60021 (número)")
print("=" * 80)
