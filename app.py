import streamlit as st
import pandas as pd
from datetime import datetime
import os
from w25_to_ssim_converter import gerar_ssim_w25_single_airline, gerar_ssim_w25_todas_companias, extrair_airline_w25
from version import get_version_info

# Traduções
TRANSLATIONS = {
    'en': {
        'title': '✈️ AMS SSIM Converter',
        'subtitle': 'W25 Amsterdam Schedule to SSIM Converter',
        'team': 'AMS Team - Capacity Dnata Brasil',
        'language': 'Language',
        'upload_file': 'Upload W25 Excel file',
        'file_types': 'Supported formats: Excel (.xlsx)',
        'processing': 'Processing W25 data...',
        'preview_title': 'W25 Data Preview',
        'airlines_found': 'Airlines found',
        'total_flights': 'Total flights',
        'conversion_mode': 'Conversion Mode',
        'single_airline': 'Single Airline',
        'all_airlines': 'All Airlines',
        'select_airline': 'Select Airline',
        'convert_button': 'Convert to SSIM',
        'converting': 'Converting...',
        'success': 'Success!',
        'download': 'Download SSIM File',
        'error': 'Error',
        'no_file': 'Please upload a W25 file first.',
        'no_airline': 'Please select an airline.',
        'help_title': '📋 How to Use',
        'help_steps': [
            '1. Upload your W25 Excel file',
            '2. Preview the data and available airlines',
            '3. Choose conversion mode (Single or All Airlines)',
            '4. Convert and download the SSIM file'
        ],
        'about_title': '🏢 About AMS Converter',
        'about_text': 'Professional converter for Amsterdam Schiphol (AMS) W25 schedules to IATA SSIM format.',
        'features': [
            '✅ W25 Amsterdam format support',
            '✅ SSIM compliance (200-character lines)',
            '✅ Link flights (turnarounds and night stops)',
            '✅ AMS timezone processing (+0100)',
            '✅ Multi-airline support'
        ],
        'contact': 'Contact: luis.evaristo@dnata.com.br'
    },
    'nl': {
        'title': '✈️ AMS SSIM Converter',
        'subtitle': 'W25 Amsterdam Schema naar SSIM Converter',
        'team': 'AMS Team - Capacity Dnata Brasil',
        'language': 'Taal',
        'upload_file': 'Upload W25 Excel bestand',
        'file_types': 'Ondersteunde formaten: Excel (.xlsx)',
        'processing': 'W25 gegevens verwerken...',
        'preview_title': 'W25 Gegevens Voorbeeld',
        'airlines_found': 'Luchtvaartmaatschappijen gevonden',
        'total_flights': 'Totaal vluchten',
        'conversion_mode': 'Conversie Modus',
        'single_airline': 'Enkele Luchtvaartmaatschappij',
        'all_airlines': 'Alle Luchtvaartmaatschappijen',
        'select_airline': 'Selecteer Luchtvaartmaatschappij',
        'convert_button': 'Converteer naar SSIM',
        'converting': 'Converteren...',
        'success': 'Succes!',
        'download': 'Download SSIM Bestand',
        'error': 'Fout',
        'no_file': 'Upload eerst een W25 bestand.',
        'no_airline': 'Selecteer een luchtvaartmaatschappij.',
        'help_title': '📋 Hoe te Gebruiken',
        'help_steps': [
            '1. Upload uw W25 Excel bestand',
            '2. Bekijk de gegevens en beschikbare luchtvaartmaatschappijen',
            '3. Kies conversie modus (Enkele of Alle Luchtvaartmaatschappijen)',
            '4. Converteer en download het SSIM bestand'
        ],
        'about_title': '🏢 Over AMS Converter',
        'about_text': 'Professionele converter voor Amsterdam Schiphol (AMS) W25 schema\'s naar IATA SSIM formaat.',
        'features': [
            '✅ W25 Amsterdam formaat ondersteuning',
            '✅ SSIM compliance (200-karakter regels)',
            '✅ Link vluchten (turnarounds en night stops)',
            '✅ AMS tijdzone verwerking (+0100)',
            '✅ Multi-luchtvaartmaatschappij ondersteuning'
        ],
        'contact': 'Contact: luis.evaristo@dnata.com.br'
    }
}

def main():
    st.set_page_config(
        page_title="AMS SSIM Converter - Dnata Brasil", 
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS customizado para tema holandês (laranja)
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #fff5f0;
        border: 1px solid #ff6b35;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 2px solid #ff6b35;
        border-radius: 0.5rem;
    }
    .stButton > button {
        background-color: #ff6b35;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #e55a2b;
    }
    .stInfo {
        background-color: #fff5f0;
        border-left: 4px solid #ff6b35;
    }
    .stSuccess {
        background-color: #f0f8f0;
        border-left: 4px solid #4caf50;
    }
    .stError {
        background-color: #fff0f0;
        border-left: 4px solid #f44336;
    }
    .stWarning {
        background-color: #fffbf0;
        border-left: 4px solid #ff9800;
    }
    .header-container {
        background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-container {
        background-color: #fff5f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ff6b35;
        margin: 0.5rem 0;
    }
    .help-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b35;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Seletor de idioma no sidebar
    with st.sidebar:
        st.markdown("### 🌐 Language / Taal")
        language = st.selectbox(
            "Select Language / Selecteer Taal",
            options=['en', 'nl'],
            format_func=lambda x: '🇬🇧 English' if x == 'en' else '🇳🇱 Nederlands',
            key='language_selector'
        )
    
    # Obter traduções
    t = TRANSLATIONS[language]
    
    # Header com gradiente laranja
    st.markdown(f"""
    <div class="header-container">
        <h1 style="margin: 0; font-size: 2.5rem;">{t['title']}</h1>
        <h3 style="margin: 0.5rem 0 0 0; opacity: 0.9;">{t['subtitle']}</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">{t['team']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seção de ajuda sempre visível
    with st.expander(t['help_title'], expanded=True):
        for step in t['help_steps']:
            st.write(step)
    
    # Upload de arquivo
    st.markdown(f"### 📁 {t['upload_file']}")
    uploaded_file = st.file_uploader(
        t['file_types'],
        type=['xlsx'],
        help="Upload your W25 Amsterdam schedule file"
    )
    
    if uploaded_file:
        try:
            # Processar arquivo
            with st.spinner(t['processing']):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ {t['success']} {len(df)} linhas carregadas")
            
            # Preview dos dados
            st.markdown(f"### 📊 {t['preview_title']}")
            
            # Encontrar companhias aéreas
            airlines = set()
            total_flights = 0
            
            for col in ['A.FLT', 'D.FLT']:
                if col in df.columns:
                    for flight in df[col].dropna():
                        if flight != 'N/S':
                            airline = extrair_airline_w25(flight)
                            if airline != 'XX':
                                airlines.add(airline)
                                total_flights += 1
            
            airlines = sorted(list(airlines))
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t['airlines_found'], len(airlines))
            with col2:
                st.metric(t['total_flights'], total_flights)
            with col3:
                st.metric("Linhas W25", len(df))
            
            # Mostrar primeiras linhas
            st.dataframe(df.head(), use_container_width=True)
            
            # Modo de conversão
            st.markdown(f"### ⚙️ {t['conversion_mode']}")
            
            conversion_mode = st.radio(
                "",
                options=['single', 'all'],
                format_func=lambda x: t['single_airline'] if x == 'single' else t['all_airlines'],
                horizontal=True
            )
            
            # Seleção de companhia (se modo single)
            selected_airline = None
            if conversion_mode == 'single':
                if airlines:
                    selected_airline = st.selectbox(
                        t['select_airline'],
                        options=airlines,
                        help="Selecione a companhia aérea para conversão"
                    )
                else:
                    st.warning("Nenhuma companhia aérea encontrada no arquivo")
            
            # Botão de conversão
            st.markdown("### 🚀 Conversão")
            
            if st.button(t['convert_button'], type="primary", use_container_width=True):
                if conversion_mode == 'single' and not selected_airline:
                    st.error(t['no_airline'])
                else:
                    with st.spinner(t['converting']):
                        # Salvar arquivo temporário
                        temp_file = f"temp_w25_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        df.to_excel(temp_file, index=False)
                        
                        try:
                            if conversion_mode == 'single':
                                result = gerar_ssim_w25_single_airline(temp_file, selected_airline)
                                output_file = f"{selected_airline}_{datetime.now().strftime('%Y%m%d')}_W25_AMS.ssim"
                            else:
                                result = gerar_ssim_w25_todas_companias(temp_file)
                                output_file = f"ALL_AIRLINES_{datetime.now().strftime('%Y%m%d')}_W25_AMS.ssim"
                            
                            # Limpar arquivo temporário
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
                            
                            if "sucesso" in result:
                                st.success(f"✅ {result}")
                                
                                # Botão de download
                                if os.path.exists(output_file):
                                    with open(output_file, 'r', encoding='utf-8') as f:
                                        ssim_content = f.read()
                                    
                                    st.download_button(
                                        label=f"📥 {t['download']}",
                                        data=ssim_content,
                                        file_name=output_file,
                                        mime="text/plain",
                                        type="primary",
                                        use_container_width=True
                                    )
                                    
                                    # Preview do SSIM
                                    st.markdown("### 📄 SSIM Preview (primeiras 10 linhas)")
                                    preview_lines = ssim_content.split('\n')[:10]
                                    st.code('\n'.join(preview_lines), language='text')
                                    
                                    # Limpar arquivo de saída
                                    os.remove(output_file)
                            else:
                                st.error(f"❌ {t['error']}: {result}")
                        
                        except Exception as e:
                            st.error(f"❌ {t['error']}: {str(e)}")
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
        
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    else:
        st.info(t['no_file'])
    
    # Seção sobre o projeto
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {t['about_title']}")
        st.write(t['about_text'])
        
        for feature in t['features']:
            st.write(feature)
    
    with col2:
        st.markdown("### 📞 Suporte")
        st.write(t['contact'])
        
        # Informações da versão
        version_info = get_version_info()
        st.markdown("### 📋 Versão")
        st.write(f"**Versão:** {version_info['version']}")
        st.write(f"**Data:** {version_info['build_date']}")
        st.write(f"**Equipe:** {version_info['team']}")

if __name__ == "__main__":
    main()
