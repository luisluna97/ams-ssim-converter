#!/usr/bin/env python3
"""
Teste da lógica de casamento de Night Stop
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

def gerar_dias_set(row):
    """Retorna set de dias operacionais"""
    dias = set()
    for i in range(1, 8):
        col_name = f"OP.D.{i}" if i < 7 else "OP/D/7"
        if col_name in row and not pd.isna(row[col_name]) and str(row[col_name]).strip() != "":
            dias.add(i)
    return dias if dias else {1,2,3,4,5,6,7}

# Ler malha
df = pd.read_excel("../W25 COMBINED.xlsx")

print("=" * 80)
print("ANÁLISE DE NIGHT STOP - LÓGICA DE CASAMENTO")
print("=" * 80)

# Focar em uma companhia para exemplo
companhia = "LH"
df_lh = df[df.apply(lambda row: 
    extrair_airline(row.get('A.FLT', '')) == companhia or 
    extrair_airline(row.get('D.FLT', '')) == companhia, axis=1)].copy()

print(f"\n🔍 Analisando companhia: {companhia}")
print(f"Total de registros: {len(df_lh)}")

# Separar ARRIVALs com N/S
arrivals_ns = []
for idx, row in df_lh.iterrows():
    a_flt = row.get('A.FLT')
    dest = str(row.get('DEST', '')).upper()
    
    if not pd.isna(a_flt) and a_flt != 'N/S' and dest == 'N/S':
        airline = extrair_airline(a_flt)
        if airline == companhia:
            flight_num = extrair_numero_voo(a_flt)
            dias = gerar_dias_set(row)
            arrivals_ns.append({
                'idx': idx,
                'flight_num': flight_num,
                'sta': row.get('STA'),
                'orig': row.get('ORIG'),
                'aty': row.get('ATY'),
                'dias': dias,
                'from': row.get('FROM'),
                'till': row.get('TILL')
            })

print(f"\n📥 ARRIVALS com Night Stop: {len(arrivals_ns)}")
for arr in arrivals_ns[:3]:
    print(f"  Voo {arr['flight_num']}: {arr['orig']}→AMS {arr['sta']}, dias {sorted(arr['dias'])}")

# Separar DEPARTUREs após N/S
departures_ns = []
for idx, row in df_lh.iterrows():
    d_flt = row.get('D.FLT')
    orig = str(row.get('ORIG', '')).upper()
    dest = str(row.get('DEST', '')).upper()
    
    # Departure após N/S: ORIG = N/S ou A.FLT vazio/N/S
    if not pd.isna(d_flt) and d_flt != 'N/S' and dest != 'N/S':
        if orig == 'N/S' or pd.isna(row.get('A.FLT')) or row.get('A.FLT') == 'N/S':
            airline = extrair_airline(d_flt)
            if airline == companhia:
                flight_num = extrair_numero_voo(d_flt)
                dias = gerar_dias_set(row)
                departures_ns.append({
                    'idx': idx,
                    'flight_num': flight_num,
                    'std': row.get('STD'),
                    'dest': dest,
                    'aty': row.get('ATY'),
                    'dias': dias,
                    'from': row.get('FROM'),
                    'till': row.get('TILL')
                })

print(f"\n📤 DEPARTURES após Night Stop: {len(departures_ns)}")
for dep in departures_ns[:3]:
    print(f"  Voo {dep['flight_num']}: AMS→{dep['dest']} {dep['std']}, dias {sorted(dep['dias'])}")

# Tentar casar
print(f"\n🔗 CASAMENTO DE NIGHT STOPS:")
print("-" * 80)

casamentos = []
for arr in arrivals_ns[:5]:  # Testar primeiros 5
    print(f"\n📥 Arrival: Voo {arr['flight_num']}, dias {sorted(arr['dias'])}")
    
    # Procurar departure correspondente
    candidatos = []
    for dep in departures_ns:
        # Mesmo número de voo
        if dep['flight_num'] == arr['flight_num']:
            # Dias compatíveis (dia seguinte)
            # Se chega no dia X, sai no dia X+1
            # Mas na malha pode estar marcado como mesmo dia ou dia seguinte
            dias_compativeis = len(arr['dias'].intersection(dep['dias'])) > 0
            
            if dias_compativeis:
                candidatos.append(dep)
    
    if candidatos:
        print(f"  ✅ Encontrados {len(candidatos)} candidatos:")
        for cand in candidatos[:2]:
            print(f"     → Departure: {cand['flight_num']}, dias {sorted(cand['dias'])}, STD {cand['std']}")
            casamentos.append((arr, cand))
    else:
        print(f"  ❌ Nenhum departure correspondente encontrado")

print(f"\n📊 RESUMO:")
print(f"  Arrivals N/S: {len(arrivals_ns)}")
print(f"  Departures N/S: {len(departures_ns)}")
print(f"  Casamentos encontrados: {len(casamentos)}")
print("=" * 80)
