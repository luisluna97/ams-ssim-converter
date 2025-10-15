#!/usr/bin/env python3
"""
Debug da extração de número de voo
"""

import re

def extrair_numero_voo_OLD(flight_number):
    """Função atual"""
    flight_str = str(flight_number).strip().upper()
    match = re.search(r'([0-9]+)', flight_str)
    return match.group(1).zfill(4)[:4] if match else None

def extrair_numero_voo_NEW(flight_number):
    """Função corrigida"""
    flight_str = str(flight_number).strip().upper()
    match = re.search(r'([0-9]+)', flight_str)
    if match:
        numero = match.group(1)
        # NÃO truncar! Manter todos os dígitos
        return numero.zfill(4)  # Apenas preencher com zeros à esquerda
    return None

# Testar
test_cases = ['6E0021', '6E0022', '6E0006', 'AI155', 'LH1002', 'EK145']

print("TESTE DE EXTRAÇÃO DE NÚMERO DE VOO")
print("=" * 80)
print(f"{'Voo':15s} | {'OLD (errado)':15s} | {'NEW (correto)':15s}")
print("-" * 80)

for flight in test_cases:
    old_result = extrair_numero_voo_OLD(flight)
    new_result = extrair_numero_voo_NEW(flight)
    print(f"{flight:15s} | {old_result:15s} | {new_result:15s}")

print()
print("=" * 80)
print("PROBLEMA IDENTIFICADO:")
print("zfill(4)[:4] está TRUNCANDO números maiores que 4 dígitos!")
print("Exemplo: '0021'.zfill(4)[:4] = '0021' ✅")
print("Mas: '21'.zfill(4) = '0021', [:4] = '0021' ✅")
print()
print("Vou testar com o valor real...")

# Testar com valor real
import pandas as pd
df = pd.read_excel("../W25 COMBINED.xlsx")
linha_0 = df.iloc[0]

a_flt_raw = linha_0.get('A.FLT')
print(f"\nValor RAW da linha 0, coluna A.FLT: {a_flt_raw}")
print(f"Tipo: {type(a_flt_raw)}")

# Se for inteiro
if isinstance(a_flt_raw, (int, float)):
    print(f"É número! Valor: {a_flt_raw}")
    # Converter para string primeiro
    flight_str = str(int(a_flt_raw))
    print(f"Como string: '{flight_str}'")
    
    # Extrair letras e números separadamente
    match_letter = re.match(r'^([A-Z0-9]{1,2})', flight_str)
    match_number = re.search(r'([0-9]+)$', flight_str)
    
    print(f"Match letras: {match_letter.group(1) if match_letter else 'NENHUM'}")
    print(f"Match números: {match_number.group(1) if match_number else 'NENHUM'}")

print()
print("=" * 80)
