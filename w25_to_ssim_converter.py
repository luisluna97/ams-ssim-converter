#!/usr/bin/env python3
"""
Conversor Escala Holandesa (Amsterdam Schedule) para SSIM - AMS Team
Desenvolvido por Capacity Dnata Brasil - 14/10/2025
Baseado no padrão SIRIUM com adaptações para formato holandês
"""

import pandas as pd
from datetime import datetime, timedelta
import os
import re

def ajustar_linha(line, comprimento=200):
    """Ajusta uma linha para ter exatamente o comprimento especificado"""
    return line.ljust(comprimento)[:comprimento]

def extrair_airline_w25(flight_number):
    """
    Extrai código da companhia aérea do número do voo
    Exemplo: '6E0021' → '6E', 'AI155' → 'AI'
    """
    if pd.isna(flight_number) or flight_number == 'N/S':
        return "XX"
    
    flight_str = str(flight_number).strip().upper()
    
    # Usar regex para extrair letras/números no início
    match = re.match(r'^([A-Z0-9]{1,3})', flight_str)
    if match:
        airline = match.group(1)
        # Garantir que tem pelo menos 2 caracteres
        if len(airline) == 1:
            airline = airline + "X"
        return airline[:2]
    
    return "XX"

def extrair_numero_voo_w25(flight_number):
    """
    Extrai número do voo do flight number
    Exemplo: '6E0021' → '0021', 'AI155' → '155'
    """
    if pd.isna(flight_number) or flight_number == 'N/S':
        return "001"
    
    flight_str = str(flight_number).strip().upper()
    
    # Usar regex para extrair números
    match = re.search(r'([0-9]+)', flight_str)
    if match:
        numero = match.group(1)
        return numero.zfill(4)[:4]
    
    return "001"

def processar_aty_w25(aty_value):
    """
    Processa código ATY, removendo barra se existir
    Exemplo: '320/321' → '320'
    """
    if pd.isna(aty_value):
        return "320"
    
    aty_str = str(aty_value).strip().upper()
    
    if '/' in aty_str:
        aty_str = aty_str.split('/')[0].strip()
    
    aty_clean = re.sub(r'[^A-Z0-9]', '', aty_str)
    
    return aty_clean[:3] if aty_clean else "320"

def converter_horario_w25(time_value):
    """
    Converte horário para formato SSIM HHMM
    """
    if pd.isna(time_value):
        return "0000"
    
    try:
        if isinstance(time_value, str):
            for fmt in ['%H:%M:%S', '%H:%M', '%H%M', '%H.%M']:
                try:
                    time_obj = datetime.strptime(time_value.strip(), fmt)
                    return time_obj.strftime('%H%M')
                except:
                    continue
        elif hasattr(time_value, 'hour'):
            return f"{time_value.hour:02d}{time_value.minute:02d}"
        else:
            time_str = str(time_value).strip()
            if ':' in time_str:
                parts = time_str.split(':')
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
                return f"{hour:02d}{minute:02d}"
    except:
        pass
    
    return "0000"

def gerar_operating_days_w25(row):
    """
    Gera string de dias operacionais baseado nas colunas OP.D.1 a OP/D/7
    """
    days = ""
    for i in range(1, 8):
        col_name = f"OP.D.{i}" if i < 7 else "OP/D/7"
        if col_name in row and not pd.isna(row[col_name]) and str(row[col_name]).strip() != "":
            days += str(i)
    
    # Se não tem dias, usar todos
    if not days:
        days = "1234567"
    
    # Completar com espaços até 7 caracteres
    return days.ljust(7)[:7]

def processar_periodo_w25(from_date, till_date):
    """
    Processa período FROM/TILL para formato SSIM
    """
    try:
        if pd.isna(from_date):
            from_date = datetime.now()
        if pd.isna(till_date):
            till_date = datetime.now() + timedelta(days=365)
        
        if isinstance(from_date, str):
            from_date = pd.to_datetime(from_date)
        if isinstance(till_date, str):
            till_date = pd.to_datetime(till_date)
        
        return from_date.strftime('%d%b%y').upper(), till_date.strftime('%d%b%y').upper()
    except:
        data_atual = datetime.now()
        return data_atual.strftime('%d%b%y').upper(), (data_atual + timedelta(days=365)).strftime('%d%b%y').upper()

def processar_flt_type_w25(flt_type):
    """
    Processa FLT.TYPE para determinar tipo de serviço
    J/J = Passenger/Passenger, F/F = Cargo/Cargo
    """
    if pd.isna(flt_type):
        return "J", "J"
    
    flt_str = str(flt_type).strip().upper()
    
    if '/' in flt_str:
        parts = flt_str.split('/')
        arrive_type = parts[0].strip() if len(parts) > 0 else "J"
        depart_type = parts[1].strip() if len(parts) > 1 else "J"
        return arrive_type, depart_type
    
    return flt_str, flt_str

def gerar_ssim_w25_single_airline(excel_path, codigo_iata, output_file=None):
    """
    Gera arquivo SSIM para uma companhia específica a partir da Escala Holandesa
    """
    try:
        print(f"🔄 GERANDO SSIM PARA {codigo_iata}")
        print("=" * 60)
        
        # Ler arquivo Excel
        df = pd.read_excel(excel_path)
        print(f"✅ Arquivo lido: {len(df)} linhas")
        
        # Filtrar por companhia aérea
        df_filtered = df[df.apply(lambda row: 
            extrair_airline_w25(row.get('A.FLT', '')) == codigo_iata or 
            extrair_airline_w25(row.get('D.FLT', '')) == codigo_iata, axis=1)]
        
        if df_filtered.empty:
            return None
        
        print(f"📊 Voos encontrados: {len(df_filtered)}")
        
        df_filtered = df_filtered.reset_index(drop=True)
        
        # Preparar arquivo de saída
        if output_file is None:
            data_atual = datetime.now()
            output_file = f"{codigo_iata}_{data_atual.strftime('%Y%m%d')}_AMS.ssim"
        
        with open(output_file, 'w', encoding='utf-8') as file:
            numero_linha = 1
            data_emissao = datetime.now().strftime('%d%b%y').upper()
            
            # Header (Linha 1)
            header_content = "1AIRLINE STANDARD SCHEDULE DATA SET"
            numero_linha_str = f"{numero_linha:08}"
            espacos_header = 200 - len(header_content) - len(numero_linha_str)
            linha_1 = header_content + (' ' * espacos_header) + numero_linha_str
            file.write(linha_1 + "\n")
            numero_linha += 1
            
            # 4 linhas de zeros
            for _ in range(4):
                zeros_line = "0" * 200
                file.write(zeros_line + "\n")
                numero_linha += 1
            
            # Carrier Info (Linha 2U)
            numero_linha_str = f"{numero_linha:08}"
            linha_2_content = f"2U{codigo_iata}  0008    {data_emissao}{data_emissao}{data_emissao}Created by AMS Team Dnata Brasil    P"
            espacos_necessarios = 200 - len(linha_2_content) - 4 - len(numero_linha_str)
            linha_2 = linha_2_content + (' ' * espacos_necessarios) + "EN08" + numero_linha_str
            file.write(linha_2 + "\n")
            numero_linha += 1
            
            # 4 linhas de zeros
            for _ in range(4):
                zeros_line = "0" * 200
                file.write(zeros_line + "\n")
                numero_linha += 1
            
            # Flight Records (Linha 3)
            processed_indices = set()
            flight_date_counter = {}
            
            for idx, row in df_filtered.iterrows():
                if idx in processed_indices:
                    continue
                
                from_date, till_date = processar_periodo_w25(row.get('FROM'), row.get('TILL'))
                arrive_type, depart_type = processar_flt_type_w25(row.get('FLT.TYPE'))
                frequencia = gerar_operating_days_w25(row)
                equipamento = processar_aty_w25(row.get('ATY', '320'))
                
                # Processar voo de chegada (A.FLT)
                if not pd.isna(row.get('A.FLT')) and row.get('A.FLT') != 'N/S':
                    airline_code = extrair_airline_w25(row['A.FLT'])
                    if airline_code == codigo_iata:
                        numero_voo = extrair_numero_voo_w25(row['A.FLT'])
                        sta = converter_horario_w25(row.get('STA', ''))
                        orig = str(row.get('ORIG', 'XXX'))[:3].upper()
                        
                        # Calcular STD (2h antes)
                        try:
                            sta_time = datetime.strptime(sta, '%H%M')
                            std_time = sta_time - timedelta(hours=2)
                            std = std_time.strftime('%H%M')
                        except:
                            std = "0600"
                        
                        # Date counter
                        voo_key = f"{codigo_iata}_{numero_voo}_ARR"
                        if voo_key not in flight_date_counter:
                            flight_date_counter[voo_key] = 0
                        flight_date_counter[voo_key] += 1
                        date_counter = flight_date_counter[voo_key]
                        
                        # Construir linha 3
                        numero_voo_padded = numero_voo.zfill(4)
                        etapa = "01"
                        eight_char_field = f"{numero_voo_padded}{str(date_counter).zfill(2)}{etapa}"
                        numero_voo_display = numero_voo.rjust(5)
                        numero_linha_str = f"{numero_linha:08}"
                        
                        linha_3 = (
                            f"3 "
                            f"{codigo_iata:<2} "
                            f"{eight_char_field}"
                            f"{arrive_type}"
                            f"{from_date}"
                            f"{till_date}"
                            f"{frequencia}"
                            f" "
                            f"{orig:<3}"
                            f"{std}"
                            f"{std}"
                            f"+0000"
                            f"  "
                            f"AMS"
                            f"{sta}"
                            f"{sta}"
                            f"+0100"
                            f"  "
                            f"{equipamento:<3}"
                            f"{' ':53}"
                            f"{codigo_iata:<2}"
                            f"{' ':7}"
                            f"{codigo_iata:<2}"
                            f"{numero_voo_display}"
                            f"{' ':28}"
                            f"{' ':6}"
                            f"{' ':5}"
                            f"{' ':9}"
                            f"{numero_linha_str}"
                        )
                        
                        linha_3 = linha_3.ljust(200)
                        file.write(linha_3 + "\n")
                        numero_linha += 1
                
                # Processar voo de saída (D.FLT)
                if not pd.isna(row.get('D.FLT')) and row.get('D.FLT') != 'N/S':
                    airline_code = extrair_airline_w25(row['D.FLT'])
                    if airline_code == codigo_iata:
                        numero_voo = extrair_numero_voo_w25(row['D.FLT'])
                        std = converter_horario_w25(row.get('STD', ''))
                        dest = str(row.get('DEST', 'XXX'))[:3].upper()
                        
                        # Calcular STA (2h depois)
                        try:
                            std_time = datetime.strptime(std, '%H%M')
                            sta_time = std_time + timedelta(hours=2)
                            sta = sta_time.strftime('%H%M')
                        except:
                            sta = "1400"
                        
                        # Date counter
                        voo_key = f"{codigo_iata}_{numero_voo}_DEP"
                        if voo_key not in flight_date_counter:
                            flight_date_counter[voo_key] = 0
                        flight_date_counter[voo_key] += 1
                        date_counter = flight_date_counter[voo_key]
                        
                        # Construir linha 3
                        numero_voo_padded = numero_voo.zfill(4)
                        etapa = "01"
                        eight_char_field = f"{numero_voo_padded}{str(date_counter).zfill(2)}{etapa}"
                        numero_voo_display = numero_voo.rjust(5)
                        numero_linha_str = f"{numero_linha:08}"
                        
                        linha_3 = (
                            f"3 "
                            f"{codigo_iata:<2} "
                            f"{eight_char_field}"
                            f"{depart_type}"
                            f"{from_date}"
                            f"{till_date}"
                            f"{frequencia}"
                            f" "
                            f"AMS"
                            f"{std}"
                            f"{std}"
                            f"+0100"
                            f"  "
                            f"{dest:<3}"
                            f"{sta}"
                            f"{sta}"
                            f"+0000"
                            f"  "
                            f"{equipamento:<3}"
                            f"{' ':53}"
                            f"{codigo_iata:<2}"
                            f"{' ':7}"
                            f"{codigo_iata:<2}"
                            f"{numero_voo_display}"
                            f"{' ':28}"
                            f"{' ':6}"
                            f"{' ':5}"
                            f"{' ':9}"
                            f"{numero_linha_str}"
                        )
                        
                        linha_3 = linha_3.ljust(200)
                        file.write(linha_3 + "\n")
                        numero_linha += 1
            
            # 4 linhas de zeros finais
            for _ in range(4):
                zeros_line = "0" * 200
                file.write(zeros_line + "\n")
                numero_linha += 1
            
            # Footer (Linha 5)
            numero_linha_str = f"{numero_linha + 1:06}"
            linha_5_content = f"5 {codigo_iata} {data_emissao}"
            numero_linha_str2 = f"{numero_linha:06}E"
            espacos_necessarios = 200 - len(linha_5_content) - len(numero_linha_str) - len(numero_linha_str2)
            linha_5 = linha_5_content + (' ' * espacos_necessarios) + numero_linha_str2 + numero_linha_str
            file.write(linha_5 + "\n")
        
        print(f"✅ Arquivo SSIM gerado: {output_file}")
        print(f"📊 Total de linhas: {numero_linha}")
        print("=" * 60)
        
        return output_file
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def gerar_ssim_w25_multiplas_companias(excel_path, companias_list, output_file=None):
    """
    Gera arquivo SSIM para múltiplas companhias selecionadas
    """
    try:
        print(f"🔄 GERANDO SSIM PARA COMPANHIAS: {', '.join(companias_list)}")
        print("=" * 60)
        
        # Ler arquivo Excel
        df = pd.read_excel(excel_path)
        print(f"✅ Arquivo lido: {len(df)} linhas")
        
        # Preparar arquivo de saída
        if output_file is None:
            data_atual = datetime.now()
            companias_str = '_'.join(companias_list)
            output_file = f"{companias_str}_{data_atual.strftime('%Y%m%d')}_AMS.ssim"
        
        with open(output_file, 'w', encoding='utf-8') as file:
            numero_linha = 1
            data_emissao = datetime.now().strftime('%d%b%y').upper()
            
            # Header (Linha 1)
            header_content = "1AIRLINE STANDARD SCHEDULE DATA SET"
            numero_linha_str = f"{numero_linha:08}"
            espacos_header = 200 - len(header_content) - len(numero_linha_str)
            linha_1 = header_content + (' ' * espacos_header) + numero_linha_str
            file.write(linha_1 + "\n")
            numero_linha += 1
            
            # 4 linhas de zeros
            for _ in range(4):
                zeros_line = "0" * 200
                file.write(zeros_line + "\n")
                numero_linha += 1
            
            # Processar cada companhia
            flight_date_counter = {}
            
            for companhia in companias_list:
                print(f"🔄 Processando {companhia}...")
                
                # Filtrar por companhia
                df_filtered = df[df.apply(lambda row: 
                    extrair_airline_w25(row.get('A.FLT', '')) == companhia or 
                    extrair_airline_w25(row.get('D.FLT', '')) == companhia, axis=1)]
                
                if df_filtered.empty:
                    continue
                
                df_filtered = df_filtered.reset_index(drop=True)
                
                # Carrier Info para esta companhia
                numero_linha_str = f"{numero_linha:08}"
                linha_2_content = f"2U{companhia}  0008    {data_emissao}{data_emissao}{data_emissao}Created by AMS Team Dnata Brasil    P"
                espacos_necessarios = 200 - len(linha_2_content) - 4 - len(numero_linha_str)
                linha_2 = linha_2_content + (' ' * espacos_necessarios) + "EN08" + numero_linha_str
                file.write(linha_2 + "\n")
                numero_linha += 1
                
                # 4 linhas de zeros
                for _ in range(4):
                    zeros_line = "0" * 200
                    file.write(zeros_line + "\n")
                    numero_linha += 1
                
                # Flight Records (usar mesma lógica do single airline)
                for idx, row in df_filtered.iterrows():
                    from_date, till_date = processar_periodo_w25(row.get('FROM'), row.get('TILL'))
                    arrive_type, depart_type = processar_flt_type_w25(row.get('FLT.TYPE'))
                    frequencia = gerar_operating_days_w25(row)
                    equipamento = processar_aty_w25(row.get('ATY', '320'))
                    
                    # Voo de chegada
                    if not pd.isna(row.get('A.FLT')) and row.get('A.FLT') != 'N/S':
                        airline_code = extrair_airline_w25(row['A.FLT'])
                        if airline_code == companhia:
                            numero_voo = extrair_numero_voo_w25(row['A.FLT'])
                            sta = converter_horario_w25(row.get('STA', ''))
                            orig = str(row.get('ORIG', 'XXX'))[:3].upper()
                            
                            try:
                                sta_time = datetime.strptime(sta, '%H%M')
                                std_time = sta_time - timedelta(hours=2)
                                std = std_time.strftime('%H%M')
                            except:
                                std = "0600"
                            
                            voo_key = f"{companhia}_{numero_voo}_ARR"
                            if voo_key not in flight_date_counter:
                                flight_date_counter[voo_key] = 0
                            flight_date_counter[voo_key] += 1
                            date_counter = flight_date_counter[voo_key]
                            
                            numero_voo_padded = numero_voo.zfill(4)
                            etapa = "01"
                            eight_char_field = f"{numero_voo_padded}{str(date_counter).zfill(2)}{etapa}"
                            numero_voo_display = numero_voo.rjust(5)
                            numero_linha_str = f"{numero_linha:08}"
                            
                            linha_3 = (
                                f"3 "
                                f"{companhia:<2} "
                                f"{eight_char_field}"
                                f"{arrive_type}"
                                f"{from_date}"
                                f"{till_date}"
                                f"{frequencia}"
                                f" "
                                f"{orig:<3}"
                                f"{std}"
                                f"{std}"
                                f"+0000"
                                f"  "
                                f"AMS"
                                f"{sta}"
                                f"{sta}"
                                f"+0100"
                                f"  "
                                f"{equipamento:<3}"
                                f"{' ':53}"
                                f"{companhia:<2}"
                                f"{' ':7}"
                                f"{companhia:<2}"
                                f"{numero_voo_display}"
                                f"{' ':28}"
                                f"{' ':6}"
                                f"{' ':5}"
                                f"{' ':9}"
                                f"{numero_linha_str}"
                            )
                            
                            linha_3 = linha_3.ljust(200)
                            file.write(linha_3 + "\n")
                            numero_linha += 1
                    
                    # Voo de saída
                    if not pd.isna(row.get('D.FLT')) and row.get('D.FLT') != 'N/S':
                        airline_code = extrair_airline_w25(row['D.FLT'])
                        if airline_code == companhia:
                            numero_voo = extrair_numero_voo_w25(row['D.FLT'])
                            std = converter_horario_w25(row.get('STD', ''))
                            dest = str(row.get('DEST', 'XXX'))[:3].upper()
                            
                            try:
                                std_time = datetime.strptime(std, '%H%M')
                                sta_time = std_time + timedelta(hours=2)
                                sta = sta_time.strftime('%H%M')
                            except:
                                sta = "1400"
                            
                            voo_key = f"{companhia}_{numero_voo}_DEP"
                            if voo_key not in flight_date_counter:
                                flight_date_counter[voo_key] = 0
                            flight_date_counter[voo_key] += 1
                            date_counter = flight_date_counter[voo_key]
                            
                            numero_voo_padded = numero_voo.zfill(4)
                            etapa = "01"
                            eight_char_field = f"{numero_voo_padded}{str(date_counter).zfill(2)}{etapa}"
                            numero_voo_display = numero_voo.rjust(5)
                            numero_linha_str = f"{numero_linha:08}"
                            
                            linha_3 = (
                                f"3 "
                                f"{companhia:<2} "
                                f"{eight_char_field}"
                                f"{depart_type}"
                                f"{from_date}"
                                f"{till_date}"
                                f"{frequencia}"
                                f" "
                                f"AMS"
                                f"{std}"
                                f"{std}"
                                f"+0100"
                                f"  "
                                f"{dest:<3}"
                                f"{sta}"
                                f"{sta}"
                                f"+0000"
                                f"  "
                                f"{equipamento:<3}"
                                f"{' ':53}"
                                f"{companhia:<2}"
                                f"{' ':7}"
                                f"{companhia:<2}"
                                f"{numero_voo_display}"
                                f"{' ':28}"
                                f"{' ':6}"
                                f"{' ':5}"
                                f"{' ':9}"
                                f"{numero_linha_str}"
                            )
                            
                            linha_3 = linha_3.ljust(200)
                            file.write(linha_3 + "\n")
                            numero_linha += 1
                
                print(f"✅ {companhia}: {len(df_filtered)} voos processados")
            
            # 4 linhas de zeros finais
            for _ in range(4):
                zeros_line = "0" * 200
                file.write(zeros_line + "\n")
                numero_linha += 1
            
            # Footer
            numero_linha_str = f"{numero_linha + 1:06}"
            linha_5_content = f"5 MULTI {data_emissao}"
            numero_linha_str2 = f"{numero_linha:06}E"
            espacos_necessarios = 200 - len(linha_5_content) - len(numero_linha_str) - len(numero_linha_str2)
            linha_5 = linha_5_content + (' ' * espacos_necessarios) + numero_linha_str2 + numero_linha_str
            file.write(linha_5 + "\n")
        
        print(f"✅ Arquivo SSIM gerado: {output_file}")
        print(f"📊 Total de linhas: {numero_linha}")
        print(f"🏢 Companhias: {len(companias_list)}")
        print("=" * 60)
        
        return output_file
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def gerar_ssim_w25_todas_companias(excel_path, output_file=None):
    """
    Gera arquivo SSIM para todas as companhias encontradas na Escala Holandesa
    """
    try:
        print(f"🔄 GERANDO SSIM PARA TODAS AS COMPANHIAS")
        print("=" * 60)
        
        # Ler arquivo Excel
        df = pd.read_excel(excel_path)
        print(f"✅ Arquivo lido: {len(df)} linhas")
        
        # Encontrar todas as companhias
        companias = set()
        for col in ['A.FLT', 'D.FLT']:
            if col in df.columns:
                for flight in df[col].dropna():
                    if flight != 'N/S':
                        airline = extrair_airline_w25(flight)
                        if airline != 'XX':
                            companias.add(airline)
        
        companias = sorted(list(companias))
        print(f"🏢 Companhias encontradas: {companias}")
        
        if not companias:
            return None
        
        # Usar função de múltiplas companhias
        return gerar_ssim_w25_multiplas_companias(excel_path, companias, output_file)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("Conversor Escala Holandesa para SSIM - AMS Team")
    print("Capacity Dnata Brasil - 2025")