#!/usr/bin/env python3
"""
Conversor Dutch Schedule para SSIM - VERSÃO FINAL CORRIGIDA
AMS Team - Capacity Dnata Brasil - 14/10/2025

CHANGELOG v1.0.0 - 14/10/2025:
✅ Linhas EXATAMENTE 200 caracteres
✅ Dias operacionais com espaços nas posições corretas
✅ Next Flight conectando turnarounds e night stops
✅ Voos sem casamento repetem própria informação
✅ Header/Footer únicos para todas as companhias
✅ SEM linhas de zeros entre companhias
✅ Formato 100% compatível com IATA SSIM padrão
"""

import pandas as pd
from datetime import datetime, timedelta
import re

def extrair_airline(flight_number):
    if pd.isna(flight_number) or flight_number == 'N/S':
        return None
    flight_str = str(flight_number).strip().upper()
    match = re.match(r'^([A-Z0-9]{1,3})', flight_str)
    if match:
        airline = match.group(1)
        return airline[:2] if len(airline) >= 2 else airline + "X"
    return None

def extrair_numero_voo(flight_number):
    """Extrai número do voo - CORRIGIDO para pegar números DEPOIS das letras"""
    if pd.isna(flight_number) or flight_number == 'N/S':
        return None
    flight_str = str(flight_number).strip().upper()
    # Pular letras iniciais e pegar números (ex: 6E0021 → 0021)
    match = re.search(r'^[A-Z]*([0-9]+)', flight_str)
    if match:
        numero = match.group(1)
        return numero.zfill(4)  # Apenas zfill, SEM truncar
    return None

def processar_aircraft_type(aty_value):
    if pd.isna(aty_value):
        return "320"
    aty_str = str(aty_value).strip().upper()
    if '/' in aty_str:
        aty_str = aty_str.split('/')[0].strip()
    aty_clean = re.sub(r'[^A-Z0-9]', '', aty_str)
    return aty_clean[:3] if aty_clean else "320"

def converter_horario(time_value):
    if pd.isna(time_value):
        return None
    try:
        if isinstance(time_value, str):
            for fmt in ['%H:%M:%S', '%H:%M', '%H%M']:
                try:
                    return datetime.strptime(time_value.strip(), fmt).strftime('%H%M')
                except:
                    continue
        elif hasattr(time_value, 'hour'):
            return f"{time_value.hour:02d}{time_value.minute:02d}"
        else:
            time_str = str(time_value).strip()
            if ':' in time_str:
                parts = time_str.split(':')
                hour, minute = int(parts[0]), int(parts[1]) if len(parts) > 1 else 0
                return f"{hour:02d}{minute:02d}"
    except:
        pass
    return None

def gerar_dias_operacionais_ssim(row):
    """Gera dias com ESPAÇOS: '1  4 67' = dias 1,4,6,7"""
    dias = []
    for i in range(1, 8):
        col_name = f"OP.D.{i}" if i < 7 else "OP/D/7"
        if col_name in row and not pd.isna(row[col_name]) and str(row[col_name]).strip() != "":
            dias.append(str(i))
        else:
            dias.append(' ')
    return ''.join(dias) if any(d != ' ' for d in dias) else '1234567'

def processar_periodo(from_date, till_date):
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
    if pd.isna(flt_type):
        return "J", "J"
    flt_str = str(flt_type).strip().upper()
    if '/' in flt_str:
        parts = flt_str.split('/')
        return parts[0].strip() if parts else "J", parts[1].strip() if len(parts) > 1 else "J"
    return flt_str, flt_str

def construir_linha_ssim(airline, flight_num, itin_var, leg_seq, service_type,
                         period_from, period_to, days_of_op, dep_station, dep_time, dep_tz,
                         arr_station, arr_time, arr_tz, aircraft_type, next_flight_info, line_num):
    """
    Constrói linha 3 do SSIM com EXATAMENTE 200 caracteres
    Baseado no formato oficial EK
    """
    
    # Pos 0-75: Dados básicos
    linha = "3 "  # 0-2
    linha += f"{airline:<2} "  # 2-5
    linha += f"{flight_num}"  # 5-9
    linha += f"{itin_var}"  # 9-11
    linha += f"{leg_seq}"  # 11-13
    linha += f"{service_type}"  # 13-14
    linha += f"{period_from}"  # 14-21
    linha += f"{period_to}"  # 21-28
    linha += f"{days_of_op}"  # 28-35
    linha += " "  # 35-36
    linha += f"{dep_station:<3}"  # 36-39
    linha += f"{dep_time}"  # 39-43
    linha += f"{dep_time}"  # 43-47
    linha += f"{dep_tz}"  # 47-52
    linha += "  "  # 52-54
    linha += f"{arr_station:<3}"  # 54-57
    linha += f"{arr_time}"  # 57-61
    linha += f"{arr_time}"  # 61-65
    linha += f"{arr_tz}"  # 65-70
    linha += "  "  # 70-72
    linha += f"{aircraft_type:<3}"  # 72-75
    
    # Pos 75-128: Onward/Designator (53 espaços)
    linha += " " * 53
    
    # Pos 128-144: Next Flight Data (16 caracteres)
    if next_flight_info:
        next_airline, next_flight_num = next_flight_info
    else:
        # Repetir própria informação
        next_airline = airline
        next_flight_num = flight_num
    
    linha += f"{next_airline:<2}"  # 128-130
    linha += " " * 7  # 130-137
    linha += f"{next_airline:<2}"  # 137-139
    linha += "  "  # 139-141
    linha += f"{next_flight_num:>4}"  # 141-145 (4 dígitos, right-aligned)
    
    # Pos 145-192: Espaços (47 caracteres)
    linha += " " * 47
    
    # Pos 192-200: Line Number (8 caracteres)
    linha += f"{line_num:08d}"
    
    # Verificar comprimento
    if len(linha) != 200:
        print(f"⚠️ ERRO: Linha tem {len(linha)} caracteres, esperado 200!")
        linha = linha[:200].ljust(200)
    
    return linha

def gerar_ssim_completo(excel_path, companias_list=None, output_file=None):
    """
    Gera arquivo SSIM completo - VERSÃO FINAL
    """
    try:
        print("🔄 GERANDO SSIM - VERSÃO FINAL")
        print("=" * 80)
        
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
        
        print(f"🏢 Companhias: {', '.join(companias_list)}")
        
        if output_file is None:
            data_atual = datetime.now()
            if len(companias_list) == 1:
                output_file = f"{companias_list[0]}_{data_atual.strftime('%Y%m%d')}_AMS.ssim"
            else:
                output_file = f"MULTI_{data_atual.strftime('%Y%m%d')}_AMS.ssim"
        
        with open(output_file, 'w', encoding='utf-8') as file:
            numero_linha = 1
            data_emissao = datetime.now().strftime('%d%b%y').upper()
            
            # HEADER
            header = "1AIRLINE STANDARD SCHEDULE DATA SET"
            linha_1 = header.ljust(192) + f"{numero_linha:08}"
            file.write(linha_1 + "\n")
            numero_linha += 1
            
            # 4 zeros após header
            for _ in range(4):
                file.write("0" * 200 + "\n")
                numero_linha += 1
            
            # Carrier Info ÚNICA para TODAS as companhias
            carrier_code = companias_list[0] if len(companias_list) == 1 else "XX"
            linha_2 = f"2U{carrier_code}  0008    {data_emissao}{data_emissao}{data_emissao}Created by AMS Team Dnata Brasil    P"
            linha_2 = linha_2.ljust(188) + "EN08" + f"{numero_linha:08}"
            file.write(linha_2 + "\n")
            numero_linha += 1
            
            # 4 zeros após carrier
            for _ in range(4):
                file.write("0" * 200 + "\n")
                numero_linha += 1
            
            # PROCESSAR CADA COMPANHIA (SEM repetir 2U)
            flight_counter = {}
            
            for companhia in companias_list:
                print(f"\n🔄 Processando {companhia}...")
                
                df_cia = df[df.apply(lambda row: 
                    extrair_airline(row.get('A.FLT', '')) == companhia or 
                    extrair_airline(row.get('D.FLT', '')) == companhia, axis=1)].copy()
                
                if df_cia.empty:
                    continue
                
                df_cia = df_cia.reset_index(drop=True)
                
                # PROCESSAR VOOS
                voos_gerados = 0
                
                for idx, row in df_cia.iterrows():
                    from_date, till_date = processar_periodo(row.get('FROM'), row.get('TILL'))
                    arrive_type, depart_type = processar_flt_type(row.get('FLT.TYPE'))
                    days_of_op = gerar_dias_operacionais_ssim(row)
                    aircraft = processar_aircraft_type(row.get('ATY'))
                    
                    a_flt = row.get('A.FLT')
                    d_flt = row.get('D.FLT')
                    sta = converter_horario(row.get('STA'))
                    std = converter_horario(row.get('STD'))
                    orig = str(row.get('ORIG', 'XXX'))[:3].upper() if not pd.isna(row.get('ORIG')) else 'XXX'
                    dest = str(row.get('DEST', 'XXX'))[:3].upper() if not pd.isna(row.get('DEST')) else 'XXX'
                    
                    # VOO DE CHEGADA (ORIG → AMS)
                    if not pd.isna(a_flt) and a_flt != 'N/S' and orig != 'N/S':
                        airline_a = extrair_airline(a_flt)
                        if airline_a == companhia and sta:
                            flight_num_a = extrair_numero_voo(a_flt)
                            
                            # NÃO calculamos STD de origem - usamos STA de AMS como referência
                            # Horário de partida = STA menos 2h (genérico, pois não sabemos o real)
                            try:
                                sta_time = datetime.strptime(sta, '%H%M')
                                std_origem = (sta_time - timedelta(hours=2)).strftime('%H%M')
                            except:
                                std_origem = "0600"
                            
                            key_a = f"{companhia}_{flight_num_a}_ARR"
                            flight_counter[key_a] = flight_counter.get(key_a, 0) + 1
                            itin_var = f"{flight_counter[key_a]:02d}"
                            
                            # Next Flight: D.FLT se válido, senão repetir próprio
                            next_flight = None
                            if not pd.isna(d_flt) and d_flt != 'N/S' and dest != 'N/S':
                                airline_d = extrair_airline(d_flt)
                                if airline_d == companhia:
                                    flight_num_d = extrair_numero_voo(d_flt)
                                    next_flight = (companhia, flight_num_d)
                            elif dest == 'N/S' and not pd.isna(d_flt) and d_flt != 'N/S':
                                airline_d = extrair_airline(d_flt)
                                if airline_d == companhia:
                                    flight_num_d = extrair_numero_voo(d_flt)
                                    next_flight = (companhia, flight_num_d)
                            
                            if not next_flight:
                                next_flight = (companhia, flight_num_a)
                            
                            # Construir linha: ORIG → AMS
                            linha_ssim = construir_linha_ssim(
                                companhia, flight_num_a, itin_var, "01", arrive_type,
                                from_date, till_date, days_of_op,
                                orig, std_origem, "+0000",  # Horário de origem é calculado (não temos real)
                                "AMS", sta, "+0100",  # Horário de AMS é REAL da malha
                                aircraft, next_flight, numero_linha
                            )
                            file.write(linha_ssim + "\n")
                            numero_linha += 1
                            voos_gerados += 1
                    
                    # VOO DE SAÍDA (AMS → DEST)
                    if not pd.isna(d_flt) and d_flt != 'N/S' and dest != 'N/S':
                        airline_d = extrair_airline(d_flt)
                        if airline_d == companhia and std:
                            flight_num_d = extrair_numero_voo(d_flt)
                            
                            # NÃO calculamos STA de destino - usamos STD de AMS como referência
                            # Horário de chegada = STD mais 2h (genérico, pois não sabemos o real)
                            try:
                                std_time = datetime.strptime(std, '%H%M')
                                sta_destino = (std_time + timedelta(hours=2)).strftime('%H%M')
                            except:
                                sta_destino = "1400"
                            
                            key_d = f"{companhia}_{flight_num_d}_DEP"
                            flight_counter[key_d] = flight_counter.get(key_d, 0) + 1
                            itin_var = f"{flight_counter[key_d]:02d}"
                            
                            # Departure repete própria informação
                            next_flight = (companhia, flight_num_d)
                            
                            # Construir linha: AMS → DEST
                            linha_ssim = construir_linha_ssim(
                                companhia, flight_num_d, itin_var, "01", depart_type,
                                from_date, till_date, days_of_op,
                                "AMS", std, "+0100",  # Horário de AMS é REAL da malha
                                dest, sta_destino, "+0000",  # Horário de destino é calculado (não temos real)
                                aircraft, next_flight, numero_linha
                            )
                            file.write(linha_ssim + "\n")
                            numero_linha += 1
                            voos_gerados += 1
                
                print(f"✅ {companhia}: {voos_gerados} voos gerados")
            
            # FOOTER ÚNICO
            for _ in range(4):
                file.write("0" * 200 + "\n")
                numero_linha += 1
            
            footer = f"5 {'MULTI' if len(companias_list) > 1 else companias_list[0]} {data_emissao}"
            linha_5 = footer.ljust(187) + f"{numero_linha:06}E" + f"{numero_linha+1:06}"
            file.write(linha_5 + "\n")
        
        print(f"\n✅ Arquivo SSIM: {output_file}")
        print(f"📊 Linhas: {numero_linha + 1}")
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
    print("Dutch Schedule to SSIM Converter - AMS Team")
    print("Capacity Dnata Brasil - 2025")