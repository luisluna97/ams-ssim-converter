#!/usr/bin/env python3
"""
Análise do arquivo oficial EK para entender formato exato
"""

# Ler arquivo oficial
with open("../EK 20250909 01DEC25-01JAN26.ssim", 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("ANÁLISE DO ARQUIVO OFICIAL EK")
print("=" * 100)

# Pegar linha 11 (primeira linha de voo)
linha11 = lines[10].rstrip('\n\r')
print(f"\nLinha 11 (primeiro voo):")
print(f"Comprimento: {len(linha11)} caracteres")
print(f"Conteúdo: '{linha11}'")
print()

# Analisar byte a byte
print("ANÁLISE POSICIONAL:")
print("-" * 100)

# Campos principais
campos = [
    (0, 2, "Record Type"),
    (2, 5, "Airline"),
    (5, 9, "Flight Number"),
    (9, 11, "Itinerary Var"),
    (11, 13, "Leg Sequence"),
    (13, 14, "Service Type"),
    (14, 21, "Period From"),
    (21, 28, "Period To"),
    (28, 35, "Days of Operation"),
    (35, 36, "Frequency Rate"),
    (36, 39, "Dep Station"),
    (39, 43, "STD Passenger"),
    (43, 47, "STD Aircraft"),
    (47, 52, "Timezone Dep"),
    (52, 54, "Terminal Dep"),
    (54, 57, "Arr Station"),
    (57, 61, "STA Passenger"),
    (61, 65, "STA Aircraft"),
    (65, 70, "Timezone Arr"),
    (70, 72, "Terminal Arr"),
    (72, 75, "Aircraft Type"),
    (75, 128, "Onward/Designator"),
    (128, 130, "Next Airline 1"),
    (130, 137, "Spacing"),
    (137, 139, "Next Airline 2"),
    (139, 141, "Spacing"),
    (141, 144, "Next Flight"),
    (144, 200, "Remaining")
]

for start, end, nome in campos:
    if end <= len(linha11):
        valor = linha11[start:end]
        print(f"Pos {start:3d}-{end:3d} ({end-start:2d}) | {nome:25s} | '{valor}'")
    else:
        print(f"Pos {start:3d}-{end:3d} ({end-start:2d}) | {nome:25s} | [FORA DO RANGE]")

# Analisar especificamente pos 144-200
print()
print("=" * 100)
print("ANÁLISE DETALHADA POS 144-200 (56 caracteres restantes):")
print("-" * 100)

if len(linha11) >= 144:
    resto = linha11[144:]
    print(f"Conteúdo: '{resto}'")
    print(f"Comprimento: {len(resto)} caracteres")
    print()
    
    # Tentar identificar padrões
    for i, char in enumerate(resto, 144):
        if char != ' ':
            print(f"Pos {i}: '{char}'")

print()
print("=" * 100)
