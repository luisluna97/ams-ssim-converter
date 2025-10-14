#!/usr/bin/env python3
"""
Análise da lógica W25 para entender casamento de voos
"""

import pandas as pd

df = pd.read_excel("../W25 COMBINED.xlsx")

print("=" * 80)
print("ANÁLISE DA MALHA W25 - ESCALA HOLANDESA")
print("=" * 80)

# Mostrar primeiras 10 linhas com colunas principais
colunas_principais = ['A.FLT', 'STA', 'ORIG', 'D.FLT', 'STD', 'DEST', 'ATY', 'FLT.TYPE', 'FROM', 'TILL']

print("\nPRIMEIRAS 10 LINHAS:")
print("-" * 80)
for idx, row in df.head(10).iterrows():
    print(f"\nLinha {idx}:")
    for col in colunas_principais:
        if col in row:
            print(f"  {col:10s}: {row[col]}")

print("\n" + "=" * 80)
print("LÓGICA DE CASAMENTO:")
print("=" * 80)

print("\n1. TURNAROUND (mesma linha com A.FLT e D.FLT):")
print("   - Se linha tem A.FLT e D.FLT válidos")
print("   - São 2 voos conectados (next flight)")
print("   - Exemplo: Linha 0 tem 6E0021 chegando e 6E0022 saindo")

print("\n2. NIGHT STOP (N/S):")
print("   - Quando DEST = 'N/S', voo pernoita em AMS")
print("   - Voo de saída correspondente está na LINHA SEGUINTE")
print("   - Deve usar 'next flight' para conectar")

print("\n3. DIAS OPERACIONAIS:")
print("   - OP.D.1 a OP/D/7 indicam dias de operação")
print("   - No SSIM: posições específicas (não concatenar números)")
print("   - Exemplo SSIM: '1    67' = dias 1, 6 e 7")

# Encontrar exemplos de Night Stop
print("\n" + "=" * 80)
print("EXEMPLOS DE NIGHT STOP NA MALHA:")
print("=" * 80)

ns_examples = df[df['DEST'] == 'N/S'].head(3)
for idx, row in ns_examples.iterrows():
    print(f"\nLinha {idx} (Night Stop):")
    print(f"  A.FLT: {row.get('A.FLT')}")
    print(f"  STA: {row.get('STA')}")
    print(f"  ORIG: {row.get('ORIG')}")
    print(f"  D.FLT: {row.get('D.FLT')}")
    print(f"  DEST: {row.get('DEST')}")
    
    if idx + 1 < len(df):
        next_row = df.iloc[idx + 1]
        print(f"\nLinha {idx+1} (Próxima - deve ser saída do N/S):")
        print(f"  A.FLT: {next_row.get('A.FLT')}")
        print(f"  D.FLT: {next_row.get('D.FLT')}")
        print(f"  STD: {next_row.get('STD')}")
        print(f"  DEST: {next_row.get('DEST')}")

print("\n" + "=" * 80)
