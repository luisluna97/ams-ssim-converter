#!/usr/bin/env python3
"""
Conversor Escala Holandesa para SSIM - VERSÃO CORRIGIDA
AMS Team - Capacity Dnata Brasil - 14/10/2025

LÓGICA CORRETA:
- Dias operacionais: posições específicas com espaços
- Next Flight: campo para conectar voos
- Turnaround: mesma linha A.FLT + D.FLT
- Night Stop: casar por número de voo + dias operacionais
"""

import pandas as pd
from datetime import datetime, timedelta
import re

def extrair_airline(flight_number):
    """Extrai código da companhia (primeiras 2 letras/números)"""
    if pd.isna(flight_number) or flight_number == 'N/S':
        return None
    
    flight_str = str(flight_number).strip().upper()
    match = re.match(r'^([A-Z0-9]{1,3})', flight_str)
    if match:
        airline = match.group(1)
        return airline[:2] if len(airline) >= 2 else airline + "X"
    return None

def extrair_numero_voo(flight_number):
    """Extrai número do voo"""
    if pd.isna(flight_number) or flight_number == 'N/S':
        return None
    
    flight_str = str(flight_number).strip().upper()
    match = re.search(r'([0-9]+)', flight_str)
    if match:
        return match.group(1).zfill(4)[:4]
    return None

def processar_aircraft_type(aty_value):
    """Processa tipo de aeronave"""
    if pd.isna(aty_value):
        return "320"
    
    aty_str = str(aty_value).strip().upper()
    if '/' in aty_str:
        aty_str = aty_str.split('/')[0].strip()
    
    aty_clean = re.sub(r'[^A-Z0-9]', '', aty_str)
    return aty_clean[:3] if aty_clean else "320"

def converter_horario(time_value):
    """Converte horário para HHMM"""
    if pd.isna(time_value):
        return None
    
    try:
        if isinstance(time_value, str):
            for fmt in ['%H:%M:%S', '%H:%M', '%H%M']:
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
    
    return None

def gerar_dias_operacionais_ssim(row):
    """
    Gera string de dias operacionais no formato SSIM correto
    Posições 1-7, com ESPAÇOS nos dias não operacionais
    Exemplo: '1    67' = dias 1, 6 e 7
    """
    dias = ['', '', '', '', '', '', '']  # 7 posições
    
    for i in range(1, 8):
        col_name = f"OP.D.{i}" if i < 7 else "OP/D/7"
        if col_name in row and not pd.isna(row[col_name]) and str(row[col_name]).strip() != "":
            dias[i-1] = str(i)
        else:
            dias[i-1] = ' '
    
    # Se não tem nenhum dia, usar todos
    if all(d == ' ' for d in dias):
        return '1234567'
    
    return ''.join(dias)

def processar_periodo(from_date, till_date):
    """Processa período FROM/TILL"""
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

def processar_flt_type(flt_type):
    """Processa FLT.TYPE (J/J, F/F, etc)"""
    if pd.isna(flt_type):
        return "J", "J"
    
    flt_str = str(flt_type).strip().upper()
    if '/' in flt_str:
        parts = flt_str.split('/')
        return parts[0].strip() if len(parts) > 0 else "J", parts[1].strip() if len(parts) > 1 else "J"
    
    return flt_str, flt_str

def construir_linha_ssim(
    airline, flight_num, itinerary_var, leg_seq, service_type,
    period_from, period_to, days_of_op,
    dep_station, dep_time, dep_timezone,
    arr_station, arr_time, arr_timezone,
    aircraft_type, next_flight_data, line_number
):
    """
    Constrói linha 3 do SSIM com posições EXATAS
    Total: 200 caracteres
    """
    # Campos obrigatórios
    linha = f"3 "  # Pos 1-2
    linha += f"{airline:<2} "  # Pos 3-5
    linha += f"{flight_num}"  # Pos 6-9
    linha += f"{itinerary_var}"  # Pos 10-11
    linha += f"{leg_seq}"  # Pos 12-13
    linha += f"{service_type}"  # Pos 14
    linha += f"{period_from}"  # Pos 15-21
    linha += f"{period_to}"  # Pos 22-28
    linha += f"{days_of_op}"  # Pos 29-35 (7 chars)
    linha += " "  # Pos 36 (Frequency Rate)
    linha += f"{dep_station:<3}"  # Pos 37-39
    linha += f"{dep_time}"  # Pos 40-43
    linha += f"{dep_time}"  # Pos 44-47 (Aircraft STD = Passenger STD)
    linha += f"{dep_timezone}"  # Pos 48-52
    linha += "  "  # Pos 53-54 (Dep Terminal)
    linha += f"{arr_station:<3}"  # Pos 55-57
    linha += f"{arr_time}"  # Pos 58-61
    linha += f"{arr_time}"  # Pos 62-65 (Aircraft STA = Passenger STA)
    linha += f"{arr_timezone}"  # Pos 66-70
    linha += "  "  # Pos 71-72 (Arr Terminal)
    linha += f"{aircraft_type:<3}"  # Pos 73-75
    
    # Pos 76-115: Onward Airline/Flight + Airline Designator (40 chars)
    linha += " " * 40
    
    # Pos 116-155: Next Flight Data + Airline Code/Number (40 chars)
    # Formato: "             AA       AA 1234           "
    if next_flight_data:
        next_airline, next_flight = next_flight_data
        next_section = f"{' ':13}{next_airline:<2}{' ':7}{next_airline:<2}{next_flight:>5}{' ':11}"
    else:
        next_section = " " * 40
    linha += next_section
    
    # Pos 156-175: Reserved/Operational Suffix (20 chars)
    linha += " " * 20
    
    # Pos 176-184: Record Serial Number (9 chars)
    linha += f"{line_number:08d} "
    
    # Pos 185-200: Spacing/Reserved (16 chars)
    linha += " " * 16
    
    # Garantir exatamente 200 caracteres
    return linha[:200].ljust(200)

def gerar_ssim_completo(excel_path, companias_list=None, output_file=None):
    """
    Gera arquivo SSIM completo com lógica correta
    """
    try:
        print("🔄 GERANDO SSIM - VERSÃO CORRIGIDA")
        print("=" * 80)
        
        # Ler Excel
        df = pd.read_excel(excel_path)
        print(f"✅ Arquivo lido: {len(df)} linhas")
        
        # Determinar companhias
        if companias_list is None:
            companias = set()
            for col in ['A.FLT', 'D.FLT']:
                if col in df.columns:
                    for flight in df[col].dropna():
                        if flight != 'N/S':
                            airline = extrair_airline(flight)
                            if airline:
                                companias.add(airline)
            companias_list = sorted(list(companias))
        
        print(f"🏢 Companhias: {companias_list}")
        
        # Preparar output
        if output_file is None:
            data_atual = datetime.now()
            if len(companias_list) == 1:
                output_file = f"{companias_list[0]}_{data_atual.strftime('%Y%m%d')}_AMS.ssim"
            else:
                output_file = f"MULTI_{data_atual.strftime('%Y%m%d')}_AMS.ssim"
        
        with open(output_file, 'w', encoding='utf-8') as file:
            numero_linha = 1
            data_emissao = datetime.now().strftime('%d%b%y').upper()
            
            # ===== HEADER ÚNICO =====
            header_content = "1AIRLINE STANDARD SCHEDULE DATA SET"
            linha_1 = header_content.ljust(200 - 8) + f"{numero_linha:08}"
            file.write(linha_1 + "\n")
            numero_linha += 1
            
            # 4 linhas de zeros
            for _ in range(4):
                file.write("0" * 200 + "\n")
                numero_linha += 1
            
            # ===== PROCESSAR CADA COMPANHIA =====
            flight_counter = {}  # Para itinerary variation
            
            for companhia in companias_list:
                print(f"\n🔄 Processando {companhia}...")
                
                # Filtrar dados desta companhia
                df_cia = df[df.apply(lambda row: 
                    extrair_airline(row.get('A.FLT', '')) == companhia or 
                    extrair_airline(row.get('D.FLT', '')) == companhia, axis=1)].copy()
                
                if df_cia.empty:
                    continue
                
                df_cia = df_cia.reset_index(drop=True)
                
                # Carrier Info (2U)
                linha_2_content = f"2U{companhia}  0008    {data_emissao}{data_emissao}{data_emissao}Created by AMS Team Dnata Brasil    P"
                linha_2 = linha_2_content.ljust(200 - 12) + "EN08" + f"{numero_linha:08}"
                file.write(linha_2 + "\n")
                numero_linha += 1
                
                # 4 linhas de zeros
                for _ in range(4):
                    file.write("0" * 200 + "\n")
                    numero_linha += 1
                
                # ===== PROCESSAR VOOS =====
                processed_rows = set()
                
                for idx, row in df_cia.iterrows():
                    if idx in processed_rows:
                        continue
                    
                    # Dados comuns
                    from_date, till_date = processar_periodo(row.get('FROM'), row.get('TILL'))
                    arrive_type, depart_type = processar_flt_type(row.get('FLT.TYPE'))
                    days_of_op = gerar_dias_operacionais_ssim(row)
                    aircraft = processar_aircraft_type(row.get('ATY'))
                    
                    # ==== CASO 1: TURNAROUND (A.FLT e D.FLT na mesma linha) ====
                    a_flt = row.get('A.FLT')
                    d_flt = row.get('D.FLT')
                    sta = converter_horario(row.get('STA'))
                    std = converter_horario(row.get('STD'))
                    orig = str(row.get('ORIG', 'XXX'))[:3].upper() if not pd.isna(row.get('ORIG')) else 'XXX'
                    dest = str(row.get('DEST', 'XXX'))[:3].upper() if not pd.isna(row.get('DEST')) else 'XXX'
                    
                    # Voo de chegada
                    if not pd.isna(a_flt) and a_flt != 'N/S' and orig != 'N/S':
                        airline_a = extrair_airline(a_flt)
                        if airline_a == companhia and sta:
                            flight_num_a = extrair_numero_voo(a_flt)
                            
                            # Calcular STD (2h antes se não tiver)
                            std_calc = std if std else (datetime.strptime(sta, '%H%M') - timedelta(hours=2)).strftime('%H%M')
                            
                            # Itinerary variation
                            key_a = f"{companhia}_{flight_num_a}"
                            flight_counter[key_a] = flight_counter.get(key_a, 0) + 1
                            itin_var = f"{flight_counter[key_a]:02d}"
                            
                            # Next flight (se tem D.FLT válido na mesma linha)
                            next_flight = None
                            if not pd.isna(d_flt) and d_flt != 'N/S' and dest != 'N/S':
                                airline_d = extrair_airline(d_flt)
                                if airline_d == companhia:
                                    flight_num_d = extrair_numero_voo(d_flt)
                                    next_flight = (companhia, flight_num_d)
                            
                            # Construir linha SSIM
                            linha_ssim = construir_linha_ssim(
                                airline=companhia,
                                flight_num=flight_num_a,
                                itinerary_var=itin_var,
                                leg_seq="01",
                                service_type=arrive_type,
                                period_from=from_date,
                                period_to=till_date,
                                days_of_op=days_of_op,
                                dep_station=orig,
                                dep_time=std_calc,
                                dep_timezone="+0000",
                                arr_station="AMS",
                                arr_time=sta,
                                arr_timezone="+0100",
                                aircraft_type=aircraft,
                                next_flight_data=next_flight,
                                line_number=numero_linha
                            )
                            file.write(linha_ssim + "\n")
                            numero_linha += 1
                    
                    # Voo de saída
                    if not pd.isna(d_flt) and d_flt != 'N/S' and dest != 'N/S':
                        airline_d = extrair_airline(d_flt)
                        if airline_d == companhia and std:
                            flight_num_d = extrair_numero_voo(d_flt)
                            
                            # Calcular STA (2h depois se não tiver)
                            sta_calc = sta if sta else (datetime.strptime(std, '%H%M') + timedelta(hours=2)).strftime('%H%M')
                            
                            # Itinerary variation
                            key_d = f"{companhia}_{flight_num_d}"
                            flight_counter[key_d] = flight_counter.get(key_d, 0) + 1
                            itin_var = f"{flight_counter[key_d]:02d}"
                            
                            # Construir linha SSIM
                            linha_ssim = construir_linha_ssim(
                                airline=companhia,
                                flight_num=flight_num_d,
                                itinerary_var=itin_var,
                                leg_seq="01",
                                service_type=depart_type,
                                period_from=from_date,
                                period_to=till_date,
                                days_of_op=days_of_op,
                                dep_station="AMS",
                                dep_time=std,
                                dep_timezone="+0100",
                                arr_station=dest,
                                arr_time=sta_calc,
                                arr_timezone="+0000",
                                aircraft_type=aircraft,
                                next_flight_data=None,
                                line_number=numero_linha
                            )
                            file.write(linha_ssim + "\n")
                            numero_linha += 1
                    
                    processed_rows.add(idx)
                
                print(f"✅ {companhia}: {len(df_cia)} registros processados")
            
            # ===== FOOTER ÚNICO =====
            # 4 linhas de zeros
            for _ in range(4):
                file.write("0" * 200 + "\n")
                numero_linha += 1
            
            # Linha 5
            if len(companias_list) == 1:
                footer_content = f"5 {companias_list[0]} {data_emissao}"
            else:
                footer_content = f"5 MULTI {data_emissao}"
            
            footer_line = footer_content.ljust(200 - 13) + f"{numero_linha:06}E" + f"{numero_linha+1:06}"
            file.write(footer_line + "\n")
        
        print(f"\n✅ Arquivo SSIM gerado: {output_file}")
        print(f"📊 Total de linhas: {numero_linha + 1}")
        print("=" * 80)
        
        return output_file
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

# Funções de compatibilidade
def gerar_ssim_w25_single_airline(excel_path, codigo_iata, output_file=None):
    return gerar_ssim_completo(excel_path, [codigo_iata], output_file)

def gerar_ssim_w25_multiplas_companias(excel_path, companias_list, output_file=None):
    return gerar_ssim_completo(excel_path, companias_list, output_file)

def gerar_ssim_w25_todas_companias(excel_path, output_file=None):
    return gerar_ssim_completo(excel_path, None, output_file)

if __name__ == "__main__":
    print("Conversor Escala Holandesa para SSIM - VERSÃO CORRIGIDA")
    print("AMS Team - Capacity Dnata Brasil - 2025")
