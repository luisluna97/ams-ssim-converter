#!/usr/bin/env python3
"""
Comparação detalhada entre linha correta e gerada
"""

# Linha CORRETA do arquivo EK oficial
linha_correta = "3 EK 02470101J01DEC2501DEC251       DXB08050805+0400  GIG15551555-0300  77W                                                     EK       EK  247                                                00000011"

# Linha GERADA pelo nosso conversor
linha_gerada = "3 EK 01450101J26OCT2528MAR261 34567 DXB10351035+0000  AMS07500750+0100  77W                                                     EK       EK  146                     EK  145           00000007"

print("COMPARAÇÃO LINHA A LINHA")
print("=" * 120)
print(f"Correta: {len(linha_correta)} chars")
print(f"Gerada:  {len(linha_gerada)} chars")
print()

# Comparar posição por posição
print("POS | CORRETO | GERADO | MATCH")
print("-" * 120)

for i in range(max(len(linha_correta), len(linha_gerada))):
    c_char = linha_correta[i] if i < len(linha_correta) else '?'
    g_char = linha_gerada[i] if i < len(linha_gerada) else '?'
    match = "✅" if c_char == g_char else "❌"
    
    if c_char != g_char:
        print(f"{i:3d} | '{c_char}'     | '{g_char}'    | {match}")

print()
print("=" * 120)
print("ANÁLISE DOS CAMPOS:")
print()

# Analisar campo por campo
campos = [
    (0, 2, "Record"),
    (2, 5, "Airline"),
    (5, 9, "Flight"),
    (9, 11, "Itin"),
    (11, 13, "Leg"),
    (13, 14, "Type"),
    (14, 21, "From"),
    (21, 28, "To"),
    (28, 35, "Days"),
    (35, 36, "Freq"),
    (36, 39, "DepStn"),
    (39, 43, "STD1"),
    (43, 47, "STD2"),
    (47, 52, "TZDep"),
    (52, 54, "TermD"),
    (54, 57, "ArrStn"),
    (57, 61, "STA1"),
    (61, 65, "STA2"),
    (65, 70, "TZArr"),
    (70, 72, "TermA"),
    (72, 75, "Aircraft"),
    (75, 128, "Onward"),
    (128, 130, "NextAir1"),
    (130, 137, "Space1"),
    (137, 139, "NextAir2"),
    (139, 141, "Space2"),
    (141, 144, "NextFlt"),
    (144, 165, "Space3"),
    (165, 167, "OpAir"),
    (167, 169, "Space4"),
    (169, 172, "OpFlt"),
    (172, 183, "Space5"),
    (183, 191, "LineNum"),
    (191, 200, "Final")
]

for start, end, nome in campos:
    c_val = linha_correta[start:end] if end <= len(linha_correta) else "???"
    g_val = linha_gerada[start:end] if end <= len(linha_gerada) else "???"
    match = "✅" if c_val == g_val else "❌"
    print(f"{start:3d}-{end:3d} {nome:12s} | C:'{c_val}' | G:'{g_val}' | {match}")

print()
print("=" * 120)
