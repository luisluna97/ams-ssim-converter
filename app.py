import streamlit as st
import pandas as pd
from datetime import datetime
import os
from w25_to_ssim_converter import gerar_ssim_w25_single_airline, gerar_ssim_w25_todas_companias, gerar_ssim_w25_multiplas_companias, extrair_airline
from version import get_version_info

# Traduções
TRANSLATIONS = {
    'en': {
        'title': 'AMS SSIM Converter',
        'subtitle': 'Dutch Schedule Converter • AMS Team - Capacity Dnata Brasil',
        'tagline': 'Transform Amsterdam schedules to IATA SSIM format',
        'help_title': 'Help & Format Info',
        'help_content': '''
**📖 How to use:** Upload Excel → Select mode → Convert → Download

**📋 Schedule Columns:** `A.FLT`, `D.FLT`, `STA`, `STD`, `ORIG`, `DEST`, `ATY`, `FROM`, `TILL`, `FLT.TYPE`, `OP.D.1-7`

**🔧 Output:** IATA-standard SSIM files with 200-character lines
        ''',
        'release_title': 'Release Notes',
        'upload': 'Upload Dutch Schedule (Excel)',
        'processing': 'Processing schedule data...',
        'success': 'File uploaded successfully',
        'preview': 'Schedule Data Preview',
        'airlines_found': 'Airlines found in file',
        'select_mode': 'Select Conversion Mode',
        'single': 'Single Airline',
        'multiple': 'Multiple Airlines (Custom Selection)',
        'all': 'All Airlines',
        'select_airline': 'Select Airline',
        'select_airlines': 'Select Airlines',
        'convert': 'Convert to SSIM',
        'converting': 'Converting to SSIM...',
        'download': 'Download SSIM File',
        'ssim_preview': 'SSIM Preview',
        'validation': 'SSIM Validation',
        'line_length': 'Line length',
        'structure': 'SSIM structure',
        'contact': 'Contact: luis.evaristo@dnata.com.br'
    },
    'nl': {
        'title': 'AMS SSIM Converter',
        'subtitle': 'Dutch Schedule Converter • AMS Team - Capacity Dnata Brasil',
        'tagline': 'Transformeer Amsterdam schema\'s naar IATA SSIM formaat',
        'help_title': 'Help & Formaat Info',
        'help_content': '''
**📖 Hoe te gebruiken:** Upload Excel → Selecteer modus → Converteer → Download

**📋 Schema Kolommen:** `A.FLT`, `D.FLT`, `STA`, `STD`, `ORIG`, `DEST`, `ATY`, `FROM`, `TILL`, `FLT.TYPE`, `OP.D.1-7`

**🔧 Output:** IATA-standaard SSIM bestanden met 200-karakter regels
        ''',
        'release_title': 'Release Notes',
        'upload': 'Upload Escala Holandesa (Excel)',
        'processing': 'Schema gegevens verwerken...',
        'success': 'Bestand succesvol geüpload',
        'preview': 'Schema Gegevens Voorbeeld',
        'airlines_found': 'Luchtvaartmaatschappijen gevonden in bestand',
        'select_mode': 'Selecteer Conversie Modus',
        'single': 'Enkele Luchtvaartmaatschappij',
        'multiple': 'Meerdere Luchtvaartmaatschappijen (Aangepaste Selectie)',
        'all': 'Alle Luchtvaartmaatschappijen',
        'select_airline': 'Selecteer Luchtvaartmaatschappij',
        'select_airlines': 'Selecteer Luchtvaartmaatschappijen',
        'convert': 'Converteer naar SSIM',
        'converting': 'Converteren naar SSIM...',
        'download': 'Download SSIM Bestand',
        'ssim_preview': 'SSIM Voorbeeld',
        'validation': 'SSIM Validatie',
        'line_length': 'Regellengte',
        'structure': 'SSIM structuur',
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
    
    # CSS customizado - tema laranja holandês
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
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
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
    .stError {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Seletor de idioma no canto superior direito
    col_lang, col_space = st.columns([1, 4])
    with col_lang:
        language = st.selectbox(
            "🌐",
            options=['en', 'nl'],
            format_func=lambda x: '🇬🇧 EN' if x == 'en' else '🇳🇱 NL',
            label_visibility="collapsed"
        )
    
    t = TRANSLATIONS[language]
    
    # Header profissional - cor laranja
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%); padding: 2rem; border-radius: 1rem; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">✈️ {t['title']}</h1>
        <p style="color: #fff5f0; margin: 0.5rem 0 0 0; font-size: 1.1rem; font-weight: 500;">{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de informações
    version_info = get_version_info()
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**{t['tagline']}**")
    with col2:
        st.markdown(f"**Version {version_info['version']}** • {version_info['build_date']}")
    with col3:
        st.markdown("[📱 **GitHub**](https://github.com/luisluna97/ams-ssim-converter)")
    
    # Help e Release Notes fixos
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander(f"❓ {t['help_title']}"):
            st.markdown(t['help_content'])
    
    with col2:
        with st.expander(f"📋 {t['release_title']}"):
            st.markdown(f"""
            ### v{version_info['version']} - {version_info['build_date']}
            ✨ Dutch Schedule to SSIM conversion
            🇳🇱 Dutch orange theme + bilingual (EN/NL)
            🔗 Turnarounds and night stops with Next Flight
            ⏰ AMS timezone (+0100) support
            📊 Multiple Airlines (Custom Selection) mode
            """)
    
    st.markdown("---")
    
    # Upload de arquivo
    st.markdown(f"### 📁 {t['upload']}")
    uploaded_file = st.file_uploader(
        "Choose a W25 Excel file",
        type=['xlsx', 'xls'],
        help="Upload your W25 Amsterdam schedule Excel file"
    )
    
    if uploaded_file:
        try:
            with st.spinner(t['processing']):
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ {t['success']} • {len(df)} rows")
            
            # Preview dos dados
            st.markdown(f"### 📊 {t['preview']}")
            
            # Encontrar companhias aéreas
            airlines = set()
            for col in ['A.FLT', 'D.FLT']:
                if col in df.columns:
                    for flight in df[col].dropna():
                        if flight != 'N/S':
                            airline = extrair_airline(flight)
                            if airline:
                                airlines.add(airline)
            
            airlines = sorted(list(airlines))
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t['airlines_found'], len(airlines))
            with col2:
                st.metric("Total Rows", len(df))
            with col3:
                st.metric("Columns", len(df.columns))
            
            # Mostrar primeiras linhas
            st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown("---")
            
            # Seleção de modo de conversão
            st.markdown(f"### ⚙️ {t['select_mode']}")
            
            conversion_mode = st.radio(
                "",
                options=['single', 'multiple', 'all'],
                format_func=lambda x: t['single'] if x == 'single' else (t['multiple'] if x == 'multiple' else t['all']),
                horizontal=True
            )
            
            # Seleção de companhia(s)
            selected_airline = None
            selected_airlines = []
            
            if conversion_mode == 'single':
                if airlines:
                    selected_airline = st.selectbox(
                        t['select_airline'],
                        options=airlines
                    )
            elif conversion_mode == 'multiple':
                if airlines:
                    selected_airlines = st.multiselect(
                        t['select_airlines'],
                        options=airlines,
                        help="Select multiple airlines for combined SSIM file"
                    )
            
            st.markdown("---")
            
            # Botão de conversão
            if st.button(f"🚀 {t['convert']}", type="primary", use_container_width=True):
                if conversion_mode == 'single' and not selected_airline:
                    st.error("Please select an airline")
                elif conversion_mode == 'multiple' and not selected_airlines:
                    st.error("Please select at least one airline")
                else:
                    with st.spinner(t['converting']):
                        # Salvar arquivo temporário
                        temp_file = f"temp_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        df.to_excel(temp_file, index=False)
                        
                        try:
                            if conversion_mode == 'single':
                                output_file = gerar_ssim_w25_single_airline(temp_file, selected_airline)
                            elif conversion_mode == 'multiple':
                                output_file = gerar_ssim_w25_multiplas_companias(temp_file, selected_airlines)
                            else:
                                output_file = gerar_ssim_w25_todas_companias(temp_file)
                            
                            # Limpar temp
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
                            
                            if output_file and os.path.exists(output_file):
                                with open(output_file, 'r', encoding='utf-8') as f:
                                    ssim_content = f.read()
                                
                                st.success("✅ SSIM file generated successfully!")
                                
                                # Download button
                                st.download_button(
                                    label=f"📥 {t['download']}",
                                    data=ssim_content,
                                    file_name=output_file,
                                    mime="text/plain",
                                    type="primary",
                                    use_container_width=True
                                )
                                
                                # SSIM Preview
                                st.markdown(f"### 📄 {t['ssim_preview']} (first 50 lines)")
                                preview_lines = ssim_content.split('\n')[:50]
                                st.code('\n'.join(preview_lines), language='text')
                                
                                # Validação
                                st.markdown(f"### ✅ {t['validation']}")
                                col1, col2 = st.columns(2)
                                
                                lines = ssim_content.split('\n')
                                all_200 = all(len(line) == 200 for line in lines if line.strip())
                                
                                with col1:
                                    status = "✅ Valid" if all_200 else "❌ Invalid"
                                    st.metric(t['line_length'], status)
                                
                                with col2:
                                    has_header = any(line.startswith('1AIRLINE') for line in lines)
                                    has_footer = any(line.startswith('5 ') for line in lines)
                                    structure_ok = has_header and has_footer
                                    status = "✅ Complete" if structure_ok else "❌ Incomplete"
                                    st.metric(t['structure'], status)
                                
                                # Limpar output
                                os.remove(output_file)
                            else:
                                st.error("❌ Error generating SSIM file")
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
    
    else:
        st.info("👆 Please upload a W25 Excel file to begin")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**{t['contact']}** • AMS Team - Capacity Dnata Brasil - 2025")

if __name__ == "__main__":
    main()