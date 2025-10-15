#!/usr/bin/env python3
"""
Verificar voos da companhia 6E na malha W25
"""

import pandas as pd
import re

def extrair_airline(flight_number):
    if pd.isna(flight_number) or flight_number == 'N/S':
        return None
    flight_str = str(flight_number).strip().upper()
    match = re.match(r'^([A-Z0-9]{1,3})', flight_str)
    if match:
        airline = match.group(1)
        return airline[:2] if len(airline) >= 2 else airline + "X"
    return None

def extrair_numero_voo(flight_number):
    if pd.isna(flight_number) or flight_number == 'N/S':
        return None
    flight_str = str(flight_number).strip().upper()
    match = re.search(r'([0-9]+)', flight_str)
    return match.group(1).zfill(4)[:4] if match else None

# Ler malha
df = pd.read_excel("../W25 COMBINED.xlsx")

print("=" * 80)
print("ANÁLISE DOS VOOS 6E NA MALHA W25")
print("=" * 80)

# Filtrar 6E
df_6e = df[df.apply(lambda row: 
    extrair_airline(row.get('A.FLT', '')) == '6E' or 
    extrair_airline(row.get('D.FLT', '')) == '6E', axis=1)].copy()

print(f"\nTotal de registros 6E: {len(df_6e)}")
print()

# Mostrar primeiras linhas
print("PRIMEIRAS LINHAS 6E:")
print("-" * 80)

for idx, row in df_6e.head(10).iterrows():
    a_flt = row.get('A.FLT')
    d_flt = row.get('D.FLT')
    
    a_num = extrair_numero_voo(a_flt) if not pd.isna(a_flt) else 'N/A'
    d_num = extrair_numero_voo(d_flt) if not pd.isna(d_flt) else 'N/A'
    
    print(f"\nLinha {idx}:")
    print(f"  A.FLT: {a_flt} → número: {a_num}")
    print(f"  D.FLT: {d_flt} → número: {d_num}")
    print(f"  STA: {row.get('STA')}, STD: {row.get('STD')}")
    print(f"  ORIG: {row.get('ORIG')}, DEST: {row.get('DEST')}")
    print(f"  FROM: {row.get('FROM')}, TILL: {row.get('TILL')}")

print()
print("=" * 80)
print("ANÁLISE:")
print("Esperado: 6E0021 e 6E0022")
print("Extraído: vamos verificar a função de extração...")
print()

# Testar extração
test_flights = ['6E0021', '6E0022', '6E0006']
for flight in test_flights:
    num = extrair_numero_voo(flight)
    print(f"  {flight} → {num}")

print("=" * 80)
