#!/usr/bin/env python3
"""
Conversor W25 Amsterdam Schedule para SSIM - AMS Team
Desenvolvido por Capacity Dnata Brasil - 14/10/2025
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
    Extrai código da companhia aérea do número do voo W25
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
            airline = airline + "X"  # Padding se necessário
        return airline[:2]  # Máximo 2 caracteres para IATA
    
    return "XX"  # Fallback

def extrair_numero_voo_w25(flight_number):
    """
    Extrai número do voo do flight number W25
    Exemplo: '6E0021' → '0021', 'AI155' → '155'
    """
    if pd.isna(flight_number) or flight_number == 'N/S':
        return "001"
    
    flight_str = str(flight_number).strip().upper()
    
    # Usar regex para extrair números
    match = re.search(r'([0-9]+)', flight_str)
    if match:
        numero = match.group(1)
        # Garantir que tem pelo menos 3 dígitos
        return numero.zfill(4)[:4]  # Máximo 4 dígitos
    
    return "001"  # Fallback

def processar_aty_w25(aty_value):
    """
    Processa código ATY do W25, removendo barra se existir
    Exemplo: '320/321' → '320'
    """
    if pd.isna(aty_value):
        return "320"  # Default
    
    aty_str = str(aty_value).strip().upper()
    
    # Se tem barra, pegar apenas a parte antes
    if '/' in aty_str:
        aty_str = aty_str.split('/')[0].strip()
    
    # Remover espaços e caracteres especiais
    aty_clean = re.sub(r'[^A-Z0-9]', '', aty_str)
    
    return aty_clean[:3] if aty_clean else "320"

def converter_horario_w25(time_value):
    """
    Converte horário W25 para formato SSIM HHMM
    """
    if pd.isna(time_value):
        return "0000"
    
    try:
        if isinstance(time_value, str):
            # Tentar diferentes formatos
            for fmt in ['%H:%M:%S', '%H:%M', '%H%M', '%H.%M']:
                try:
                    time_obj = datetime.strptime(time_value.strip(), fmt)
                    return time_obj.strftime('%H%M')
                except:
                    continue
        elif hasattr(time_value, 'hour'):
            # Se é objeto datetime/time
            return f"{time_value.hour:02d}{time_value.minute:02d}"
        else:
            # Tentar converter para string e processar
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
    
    return days if days else "1234567"  # Default todos os dias

def processar_periodo_w25(from_date, till_date):
    """
    Processa período FROM/TILL para formato SSIM
    """
    try:
        if pd.isna(from_date):
            from_date = datetime.now()
        if pd.isna(till_date):
            till_date = datetime.now() + timedelta(days=365)
        
        # Converter para datetime se necessário
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
    Processa FLT.TYPE do W25 para determinar tipo de serviço
    J/J = Passenger/Passenger, F/F = Cargo/Cargo
    """
    if pd.isna(flt_type):
        return "J", "J"  # Default passenger
    
    flt_str = str(flt_type).strip().upper()
    
    if '/' in flt_str:
        parts = flt_str.split('/')
        arrive_type = parts[0].strip() if len(parts) > 0 else "J"
        depart_type = parts[1].strip() if len(parts) > 1 else "J"
        return arrive_type, depart_type
    
    return flt_str, flt_str

def encontrar_night_stop_pair(df, current_idx):
    """
    Encontra o par de night stop na linha seguinte
    """
    if current_idx + 1 < len(df):
        next_row = df.iloc[current_idx + 1]
        current_row = df.iloc[current_idx]
        
        # Verificar se é o mesmo voo base
        current_aflt = current_row.get('A.FLT', '')
        next_dflt = next_row.get('D.FLT', '')
        
        if (not pd.isna(current_aflt) and not pd.isna(next_dflt) and 
            extrair_airline_w25(current_aflt) == extrair_airline_w25(next_dflt)):
            return next_row
    
    return None

def gerar_ssim_w25_single_airline(excel_path, codigo_iata, output_file=None):
    """
    Gera arquivo SSIM para uma companhia específica a partir de dados W25
    """
    try:
        # Ler arquivo Excel
        df = pd.read_excel(excel_path)
        
        # Filtrar por companhia aérea
        df_filtered = df[df.apply(lambda row: 
            extrair_airline_w25(row.get('A.FLT', '')) == codigo_iata or 
            extrair_airline_w25(row.get('D.FLT', '')) == codigo_iata, axis=1)]
        
        if df_filtered.empty:
            return f"Nenhum voo encontrado para a companhia {codigo_iata}"
        
        # Reset index para facilitar processamento
        df_filtered = df_filtered.reset_index(drop=True)
        
        # Gerar linhas SSIM
        ssim_lines = []
        line_number = 1
        processed_indices = set()  # Para evitar processar a mesma linha duas vezes
        
        # Header (Linha 1)
        header = "1AIRLINE STANDARD SCHEDULE DATA SET"
        ssim_lines.append(ajustar_linha(header + f"{line_number:08d}"))
        line_number += 1
        
        # Carrier Info (Linha 2U)
        data_atual = datetime.now()
        carrier_info = f"2U{codigo_iata}  0008    {data_atual.strftime('%d%b%y').upper()}{data_atual.strftime('%d%b%y').upper()}{data_atual.strftime('%d%b%y').upper()}Created by AMS Team Dnata Brasil    P"
        ssim_lines.append(ajustar_linha(carrier_info + f"EN08{line_number:08d}"))
        line_number += 1
        
        # Flight Records (Linha 3)
        for idx, row in df_filtered.iterrows():
            if idx in processed_indices:
                continue
                
            # Processar período de operação
            from_date, till_date = processar_periodo_w25(row.get('FROM'), row.get('TILL'))
            
            # Processar tipo de voo
            arrive_type, depart_type = processar_flt_type_w25(row.get('FLT.TYPE'))
            
            # Processar voo de chegada (A.FLT)
            if not pd.isna(row.get('A.FLT')) and row.get('A.FLT') != 'N/S':
                airline_code = extrair_airline_w25(row['A.FLT'])
                if airline_code == codigo_iata:
                    flight_num = extrair_numero_voo_w25(row['A.FLT'])
                    sta = converter_horario_w25(row.get('STA', ''))
                    orig = str(row.get('ORIG', 'XXX'))[:3]
                    aty = processar_aty_w25(row.get('ATY', '320'))
                    days = gerar_operating_days_w25(row)
                    
                    # Calcular horário de saída (2h antes da chegada como padrão)
                    try:
                        sta_time = datetime.strptime(sta, '%H%M')
                        std_time = sta_time - timedelta(hours=2)
                        std = std_time.strftime('%H%M')
                    except:
                        std = "0600"  # Default
                    
                    # Determinar next flight
                    next_flight = ""
                    if not pd.isna(row.get('D.FLT')) and row.get('D.FLT') != 'N/S':
                        next_flight = f"{codigo_iata} {extrair_numero_voo_w25(row['D.FLT'])}"
                    
                    flight_line = f"3 {codigo_iata} {flight_num}0101{arrive_type}{from_date}{till_date}{days} {orig}{std}{std}+0000  AMS{sta}{sta}+0100  {aty}"
                    ssim_lines.append(ajustar_linha(flight_line + f"{next_flight:<15}" + f"{line_number:08d}"))
                    line_number += 1
            
            # Processar voo de saída (D.FLT)
            if not pd.isna(row.get('D.FLT')) and row.get('D.FLT') != 'N/S':
                airline_code = extrair_airline_w25(row['D.FLT'])
                if airline_code == codigo_iata:
                    flight_num = extrair_numero_voo_w25(row['D.FLT'])
                    std = converter_horario_w25(row.get('STD', ''))
                    dest = str(row.get('DEST', 'XXX'))[:3]
                    aty = processar_aty_w25(row.get('ATY', '320'))
                    days = gerar_operating_days_w25(row)
                    
                    # Calcular horário de chegada (2h após a saída como padrão)
                    try:
                        std_time = datetime.strptime(std, '%H%M')
                        sta_time = std_time + timedelta(hours=2)
                        sta = sta_time.strftime('%H%M')
                    except:
                        sta = "1400"  # Default
                    
                    flight_line = f"3 {codigo_iata} {flight_num}0101{depart_type}{from_date}{till_date}{days} AMS{std}{std}+0100  {dest}{sta}{sta}+0000  {aty}"
                    ssim_lines.append(ajustar_linha(flight_line + f"{' ':<15}" + f"{line_number:08d}"))
                    line_number += 1
            
            # Verificar night stop
            elif (not pd.isna(row.get('A.FLT')) and row.get('A.FLT') != 'N/S' and 
                  str(row.get('DEST', '')).upper() == 'N/S'):
                # Procurar par de night stop
                ns_pair = encontrar_night_stop_pair(df_filtered, idx)
                if ns_pair is not None:
                    processed_indices.add(idx + 1)  # Marcar próxima linha como processada
                    
                    # Processar voo de saída do night stop
                    if not pd.isna(ns_pair.get('D.FLT')):
                        airline_code = extrair_airline_w25(ns_pair['D.FLT'])
                        if airline_code == codigo_iata:
                            flight_num = extrair_numero_voo_w25(ns_pair['D.FLT'])
                            std = converter_horario_w25(ns_pair.get('STD', ''))
                            dest = str(ns_pair.get('DEST', 'XXX'))[:3]
                            aty = processar_aty_w25(ns_pair.get('ATY', '320'))
                            days = gerar_operating_days_w25(ns_pair)
                            
                            # Calcular horário de chegada
                            try:
                                std_time = datetime.strptime(std, '%H%M')
                                sta_time = std_time + timedelta(hours=2)
                                sta = sta_time.strftime('%H%M')
                            except:
                                sta = "1400"
                            
                            flight_line = f"3 {codigo_iata} {flight_num}0101{depart_type}{from_date}{till_date}{days} AMS{std}{std}+0100  {dest}{sta}{sta}+0000  {aty}"
                            ssim_lines.append(ajustar_linha(flight_line + f"{' ':<15}" + f"{line_number:08d}"))
                            line_number += 1
        
        # Footer (Linha 5)
        footer = f"5 {codigo_iata} {data_atual.strftime('%d%b%y').upper()}"
        ssim_lines.append(ajustar_linha(footer + f"{line_number-1:06d}E{line_number:06d}"))
        
        # Salvar arquivo
        if output_file is None:
            output_file = f"{codigo_iata}_{data_atual.strftime('%Y%m%d')}_W25_AMS.ssim"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in ssim_lines:
                f.write(line + '\n')
        
        return f"Arquivo SSIM gerado com sucesso: {output_file} ({len(ssim_lines)} linhas)"
        
    except Exception as e:
        return f"Erro ao processar arquivo: {str(e)}"

def gerar_ssim_w25_todas_companias(excel_path, output_file=None):
    """
    Gera arquivo SSIM para todas as companhias encontradas no W25
    """
    try:
        # Ler arquivo Excel
        df = pd.read_excel(excel_path)
        
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
        
        if not companias:
            return "Nenhuma companhia aérea válida encontrada"
        
        # Gerar SSIM combinado
        all_ssim_lines = []
        data_atual = datetime.now()
        line_number = 1
        
        # Header global
        header = "1AIRLINE STANDARD SCHEDULE DATA SET"
        all_ssim_lines.append(ajustar_linha(header + f"{line_number:08d}"))
        line_number += 1
        
        # Processar cada companhia
        for codigo_iata in companias:
            # Filtrar por companhia
            df_filtered = df[df.apply(lambda row: 
                extrair_airline_w25(row.get('A.FLT', '')) == codigo_iata or 
                extrair_airline_w25(row.get('D.FLT', '')) == codigo_iata, axis=1)]
            
            if df_filtered.empty:
                continue
            
            df_filtered = df_filtered.reset_index(drop=True)
            processed_indices = set()
            
            # Carrier Info para esta companhia
            carrier_info = f"2U{codigo_iata}  0008    {data_atual.strftime('%d%b%y').upper()}{data_atual.strftime('%d%b%y').upper()}{data_atual.strftime('%d%b%y').upper()}Created by AMS Team Dnata Brasil    P"
            all_ssim_lines.append(ajustar_linha(carrier_info + f"EN08{line_number:08d}"))
            line_number += 1
            
            # Flight Records para esta companhia
            for idx, row in df_filtered.iterrows():
                if idx in processed_indices:
                    continue
                    
                from_date, till_date = processar_periodo_w25(row.get('FROM'), row.get('TILL'))
                arrive_type, depart_type = processar_flt_type_w25(row.get('FLT.TYPE'))
                
                # Processar voo de chegada
                if not pd.isna(row.get('A.FLT')) and row.get('A.FLT') != 'N/S':
                    airline_code = extrair_airline_w25(row['A.FLT'])
                    if airline_code == codigo_iata:
                        flight_num = extrair_numero_voo_w25(row['A.FLT'])
                        sta = converter_horario_w25(row.get('STA', ''))
                        orig = str(row.get('ORIG', 'XXX'))[:3]
                        aty = processar_aty_w25(row.get('ATY', '320'))
                        days = gerar_operating_days_w25(row)
                        
                        try:
                            sta_time = datetime.strptime(sta, '%H%M')
                            std_time = sta_time - timedelta(hours=2)
                            std = std_time.strftime('%H%M')
                        except:
                            std = "0600"
                        
                        next_flight = ""
                        if not pd.isna(row.get('D.FLT')) and row.get('D.FLT') != 'N/S':
                            next_flight = f"{codigo_iata} {extrair_numero_voo_w25(row['D.FLT'])}"
                        
                        flight_line = f"3 {codigo_iata} {flight_num}0101{arrive_type}{from_date}{till_date}{days} {orig}{std}{std}+0000  AMS{sta}{sta}+0100  {aty}"
                        all_ssim_lines.append(ajustar_linha(flight_line + f"{next_flight:<15}" + f"{line_number:08d}"))
                        line_number += 1
                
                # Processar voo de saída
                if not pd.isna(row.get('D.FLT')) and row.get('D.FLT') != 'N/S':
                    airline_code = extrair_airline_w25(row['D.FLT'])
                    if airline_code == codigo_iata:
                        flight_num = extrair_numero_voo_w25(row['D.FLT'])
                        std = converter_horario_w25(row.get('STD', ''))
                        dest = str(row.get('DEST', 'XXX'))[:3]
                        aty = processar_aty_w25(row.get('ATY', '320'))
                        days = gerar_operating_days_w25(row)
                        
                        try:
                            std_time = datetime.strptime(std, '%H%M')
                            sta_time = std_time + timedelta(hours=2)
                            sta = sta_time.strftime('%H%M')
                        except:
                            sta = "1400"
                        
                        flight_line = f"3 {codigo_iata} {flight_num}0101{depart_type}{from_date}{till_date}{days} AMS{std}{std}+0100  {dest}{sta}{sta}+0000  {aty}"
                        all_ssim_lines.append(ajustar_linha(flight_line + f"{' ':<15}" + f"{line_number:08d}"))
                        line_number += 1
        
        # Footer global
        footer = f"5 ALL {data_atual.strftime('%d%b%y').upper()}"
        all_ssim_lines.append(ajustar_linha(footer + f"{line_number-1:06d}E{line_number:06d}"))
        
        # Salvar arquivo
        if output_file is None:
            output_file = f"ALL_AIRLINES_{data_atual.strftime('%Y%m%d')}_W25_AMS.ssim"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in all_ssim_lines:
                f.write(line + '\n')
        
        return f"Arquivo SSIM gerado com sucesso: {output_file} ({len(all_ssim_lines)} linhas, {len(companias)} companhias)"
        
    except Exception as e:
        return f"Erro ao processar arquivo: {str(e)}"

if __name__ == "__main__":
    # Teste básico
    print("W25 to SSIM Converter - AMS Team")
    print("Capacity Dnata Brasil - 2025")
