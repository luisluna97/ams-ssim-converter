#!/usr/bin/env python3
"""
Verificar comprimento exato das linhas do arquivo oficial EK
"""

# Ler arquivo oficial
with open("../Downloads/EK 20250909 01DEC25-01JAN26.ssim", 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("ANÁLISE DO ARQUIVO OFICIAL EK")
print("=" * 80)

# Verificar comprimentos
comprimentos = {}
for i, line in enumerate(lines[:20], 1):
    line_clean = line.rstrip('\n\r')
    length = len(line_clean)
    comprimentos[length] = comprimentos.get(length, 0) + 1
    print(f"Linha {i:2d}: {length:3d} chars | {line_clean[:80]}...")

print()
print("RESUMO:")
for length, count in sorted(comprimentos.items()):
    print(f"  {length} caracteres: {count} linhas")

print()
print("=" * 80)
