#!/usr/bin/env python3
"""
Análise exata de uma linha SSIM para entender cada posição
"""

# Linha exemplo do SSIM correto
linha = "3 TS 01220101J01SEP2501SEP251       YYZ22452245-0500  LGW10451045+0000  332                                                     TS       TS  122                     TS  123           00000011         "

print("ANÁLISE BYTE A BYTE DA LINHA SSIM")
print("=" * 100)
print(f"Comprimento: {len(linha)} caracteres")
print()

# Analisar cada seção
sections = [
    (0, 2, "Record Type", "3 "),
    (2, 5, "Airline", "TS "),
    (5, 9, "Flight Number", "0122"),
    (9, 11, "Itin Var", "01"),
    (11, 13, "Leg Seq", "01"),
    (13, 14, "Service", "J"),
    (14, 21, "From Date", "01SEP25"),
    (21, 28, "To Date", "01SEP25"),
    (28, 35, "Days", "1       "),  # 7 chars
    (35, 36, "Freq", " "),
    (36, 39, "Dep Stn", "YYZ"),
    (39, 43, "STD Pass", "2245"),
    (43, 47, "STD Airc", "2245"),
    (47, 52, "TZ Dep", "-0500"),
    (52, 54, "Term Dep", "  "),
    (54, 57, "Arr Stn", "LGW"),
    (57, 61, "STA Pass", "1045"),
    (61, 65, "STA Airc", "1045"),
    (65, 70, "TZ Arr", "+0000"),
    (70, 72, "Term Arr", "  "),
    (72, 75, "Aircraft", "332"),
    (75, 128, "Onward/Designator", " " * 53),  # 53 espaços
    (128, 130, "Next Airline 1", "TS"),
    (130, 137, "Spacing", " " * 7),
    (137, 139, "Next Airline 2", "TS"),
    (139, 141, "Spacing", "  "),
    (141, 144, "Next Flight", "122"),
    (144, 165, "Spacing", " " * 21),
    (165, 167, "Operational Suffix Airline 1", "TS"),
    (167, 169, "Spacing", "  "),
    (169, 172, "Operational Suffix Flight", "123"),
    (172, 183, "Spacing", " " * 11),
    (183, 191, "Line Number", "00000011"),
    (191, 200, "Final Spacing", " " * 9)
]

print("ESTRUTURA DETALHADA:")
print("-" * 100)
for start, end, nome, exemplo in sections:
    valor_real = linha[start:end]
    tamanho = end - start
    match = "✅" if valor_real == exemplo else "❌"
    print(f"{start:3d}-{end:3d} ({tamanho:2d}) | {nome:30s} | '{valor_real}' {match}")

print()
print("=" * 100)
print("CAMPOS NEXT FLIGHT (MAIS IMPORTANTES):")
print("Pos 128-130: Next Airline 1 (2 chars)")
print("Pos 137-139: Next Airline 2 (2 chars)")
print("Pos 141-144: Next Flight Number (3 chars, right-aligned)")
print()
print("Pos 165-167: Operational Suffix Airline (2 chars)")
print("Pos 169-172: Operational Suffix Flight (3 chars)")
print("=" * 100)
