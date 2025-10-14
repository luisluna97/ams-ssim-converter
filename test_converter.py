#!/usr/bin/env python3
"""
Teste do conversor W25 para SSIM - AMS Team
Execute: python test_converter.py
"""

from w25_to_ssim_converter import gerar_ssim_w25_single_airline, gerar_ssim_w25_todas_companias

def test_single_airline():
    """Testa conversão de uma única companhia"""
    print("\n" + "="*60)
    print("TESTE: SINGLE AIRLINE (EK - Emirates)")
    print("="*60)
    
    # Usar arquivo W25 COMBINED.xlsx
    result = gerar_ssim_w25_single_airline(
        excel_path="../W25 COMBINED.xlsx",
        codigo_iata="EK",
        output_file="TEST_EK_W25_AMS.ssim"
    )
    
    if result:
        print(f"\n✅ Arquivo gerado: {result}")
        
        # Ler e validar
        with open(result, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📊 Total de linhas: {len(lines)}")
        
        # Validar tamanho das linhas
        invalid_lines = []
        for i, line in enumerate(lines, 1):
            line_clean = line.rstrip('\n')
            if line_clean and len(line_clean) != 200:
                invalid_lines.append((i, len(line_clean)))
        
        if invalid_lines:
            print(f"❌ Linhas inválidas (não têm 200 caracteres):")
            for line_num, length in invalid_lines[:5]:  # Mostrar apenas primeiras 5
                print(f"   Linha {line_num}: {length} caracteres")
        else:
            print("✅ Todas as linhas têm exatamente 200 caracteres")
        
        # Mostrar primeiras linhas
        print("\n📄 Primeiras 10 linhas:")
        for i, line in enumerate(lines[:10], 1):
            print(f"{i:2d}: {line.rstrip()}")
        
        print("\n" + "="*60)
        return True
    else:
        print("❌ Erro na conversão")
        return False

def test_all_airlines():
    """Testa conversão de todas as companhias"""
    print("\n" + "="*60)
    print("TESTE: ALL AIRLINES")
    print("="*60)
    
    result = gerar_ssim_w25_todas_companias(
        excel_path="../W25 COMBINED.xlsx",
        output_file="TEST_ALL_W25_AMS.ssim"
    )
    
    if result:
        print(f"\n✅ Arquivo gerado: {result}")
        
        # Ler e validar
        with open(result, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📊 Total de linhas: {len(lines)}")
        
        # Validar tamanho
        invalid_lines = []
        for i, line in enumerate(lines, 1):
            line_clean = line.rstrip('\n')
            if line_clean and len(line_clean) != 200:
                invalid_lines.append((i, len(line_clean)))
        
        if invalid_lines:
            print(f"❌ Linhas inválidas:")
            for line_num, length in invalid_lines[:5]:
                print(f"   Linha {line_num}: {length} caracteres")
        else:
            print("✅ Todas as linhas têm exatamente 200 caracteres")
        
        print("\n" + "="*60)
        return True
    else:
        print("❌ Erro na conversão")
        return False

if __name__ == "__main__":
    print("\n🧪 INICIANDO TESTES DO CONVERSOR W25→SSIM")
    print("AMS Team - Capacity Dnata Brasil")
    print("Data: 14/10/2025")
    
    # Teste 1: Single airline
    test1 = test_single_airline()
    
    # Teste 2: All airlines
    test2 = test_all_airlines()
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print(f"Single Airline (EK): {'✅ PASSOU' if test1 else '❌ FALHOU'}")
    print(f"All Airlines: {'✅ PASSOU' if test2 else '❌ FALHOU'}")
    print("="*60)
    
    if test1 and test2:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
    
    input("\nPressione Enter para sair...")
