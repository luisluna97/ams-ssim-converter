#!/usr/bin/env python3
"""
Teste da lógica de casamento de Night Stop - VERSÃO CORRIGIDA
Lógica: Arrival N/S aponta para DEPARTURE (não necessariamente mesmo número)
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
    if match:
        return match.group(1).zfill(4)[:4]
    return None

# Ler malha
df = pd.read_excel("../W25 COMBINED.xlsx")

print("=" * 80)
print("ANÁLISE DE NIGHT STOP - LÓGICA CORRIGIDA")
print("=" * 80)

# Focar em LH
companhia = "LH"
df_lh = df[df.apply(lambda row: 
    extrair_airline(row.get('A.FLT', '')) == companhia or 
    extrair_airline(row.get('D.FLT', '')) == companhia, axis=1)].copy()

print(f"\n🔍 Analisando companhia: {companhia}")

# Analisar linhas com N/S
print(f"\n📋 LINHAS COM NIGHT STOP:")
print("-" * 80)

for idx, row in df_lh.head(20).iterrows():
    a_flt = row.get('A.FLT')
    d_flt = row.get('D.FLT')
    dest = str(row.get('DEST', '')).upper()
    orig = str(row.get('ORIG', '')).upper()
    
    if dest == 'N/S' or orig == 'N/S':
        a_num = extrair_numero_voo(a_flt) if not pd.isna(a_flt) else 'N/A'
        d_num = extrair_numero_voo(d_flt) if not pd.isna(d_flt) else 'N/A'
        
        print(f"\nLinha {idx}:")
        print(f"  A.FLT: {a_flt} (num: {a_num}), ORIG: {orig}")
        print(f"  D.FLT: {d_flt} (num: {d_num}), DEST: {dest}")
        print(f"  STA: {row.get('STA')}, STD: {row.get('STD')}")

print(f"\n" + "=" * 80)
print("OBSERVAÇÕES:")
print("=" * 80)

print("""
PADRÃO IDENTIFICADO:

1. Linha com ARRIVAL N/S:
   - A.FLT: LH1002 (chega)
   - D.FLT: LH1003 (campo já mostra qual voo sai!)
   - DEST: N/S
   
2. Linha com DEPARTURE após N/S:
   - A.FLT: LH1002 (vazio ou N/S)
   - D.FLT: LH1003 (sai)
   - ORIG: N/S

SOLUÇÃO:
- Quando linha tem A.FLT válido + DEST=N/S:
  → Next Flight = D.FLT da MESMA LINHA!
  → O campo D.FLT já indica qual voo sai após o pernoite

- Quando linha tem D.FLT válido + ORIG=N/S:
  → É o departure correspondente
  → Pode ter ou não next flight para próximo segmento
""")

print("\n" + "=" * 80)
print("TESTE DA LÓGICA:")
print("=" * 80)

# Testar lógica corrigida
ns_pairs = []
for idx, row in df_lh.iterrows():
    a_flt = row.get('A.FLT')
    d_flt = row.get('D.FLT')
    dest = str(row.get('DEST', '')).upper()
    
    # Arrival com N/S - D.FLT já mostra o departure!
    if not pd.isna(a_flt) and a_flt != 'N/S' and dest == 'N/S':
        a_num = extrair_numero_voo(a_flt)
        d_num = extrair_numero_voo(d_flt) if not pd.isna(d_flt) and d_flt != 'N/S' else None
        
        if d_num:
            ns_pairs.append({
                'arrival': a_num,
                'departure': d_num,
                'sta': row.get('STA'),
                'linha': idx
            })

print(f"\n✅ Pares Night Stop identificados: {len(ns_pairs)}")
for pair in ns_pairs[:10]:
    print(f"  Arrival {pair['arrival']} (STA {pair['sta']}) → Departure {pair['departure']}")

print("\n" + "=" * 80)
