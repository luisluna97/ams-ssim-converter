#!/usr/bin/env python3
"""
Análise detalhada do formato SSIM para entender posições exatas
"""

# Exemplo de linha 3 do SSIM correto
linha = "3 TS 01220101J01SEP2501SEP251       YYZ22452245-0500  LGW10451045+0000  332                                                     TS       TS  122                     TS  123           00000011         "

print("ANÁLISE DETALHADA DA LINHA 3 DO SSIM")
print("=" * 100)
print(f"Comprimento total: {len(linha)} caracteres")
print()

# Quebrar a linha em campos
print("POSIÇÕES E CAMPOS:")
print("-" * 100)

campos = [
    (1, 2, "Record Type", linha[0:2]),
    (3, 5, "Airline", linha[2:5]),
    (6, 9, "Flight Number", linha[5:9]),
    (10, 11, "Itinerary Variation", linha[9:11]),
    (12, 13, "Leg Sequence", linha[11:13]),
    (14, 14, "Service Type", linha[13:14]),
    (15, 21, "Period of Operation (From)", linha[14:21]),
    (22, 28, "Period of Operation (To)", linha[21:28]),
    (29, 35, "Days of Operation", linha[28:35]),
    (36, 36, "Frequency Rate", linha[35:36]),
    (37, 39, "Dep Station", linha[36:39]),
    (40, 43, "Passenger STD", linha[39:43]),
    (44, 47, "Aircraft STD", linha[43:47]),
    (48, 52, "Time Variation Dep", linha[47:52]),
    (53, 54, "Dep Terminal", linha[52:54]),
    (55, 57, "Arr Station", linha[54:57]),
    (58, 61, "Passenger STA", linha[57:61]),
    (62, 65, "Aircraft STA", linha[61:65]),
    (66, 70, "Time Variation Arr", linha[65:70]),
    (71, 72, "Arr Terminal", linha[70:72]),
    (73, 75, "Aircraft Type", linha[72:75]),
    (76, 95, "Onward Airline/Flight", linha[75:95]),
    (96, 115, "Airline Designator", linha[95:115]),
    (116, 135, "Next Flight Data", linha[115:135]),
    (136, 155, "Airline Code/Number", linha[135:155]),
    (156, 175, "Reserved/Operational Suffix", linha[155:175]),
    (176, 184, "Record Serial Number", linha[175:184]),
    (185, 200, "Spacing/Reserved", linha[184:200])
]

for start, end, nome, valor in campos:
    print(f"{start:3d}-{end:3d} | {nome:35s} | '{valor}'")

print()
print("=" * 100)
print("OBSERVAÇÕES IMPORTANTES:")
print("- Posição 29-35: Dias operacionais com ESPAÇOS nas posições dos dias não operacionais")
print("  Exemplo: '1    67' = Opera nos dias 1, 6 e 7")
print("- Posição 116-135: Next Flight Data - campo para ligar voos conectados")
print("- Linha tem EXATAMENTE 200 caracteres")
print("=" * 100)
