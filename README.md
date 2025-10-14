# ✈️ AMS SSIM Converter

**Professional W25 Amsterdam schedule to IATA SSIM converter**  
**Developed by Capacity Dnata Brasil - AMS Team**

## 🔧 Features

* ✅ **W25 Amsterdam format support** - Specialized for Schiphol Airport operations
* ✅ **SSIM compliance** - Standard 200-character line format
* ✅ **Link flights** - Automatic turnaround and night stop processing
* ✅ **AMS timezone processing** - Native +0100 (CET/CEST) support
* ✅ **Multi-airline support** - Single or all airlines conversion
* ✅ **Bilingual interface** - English and Dutch language support
* ✅ **Professional UI** - Dutch-themed orange design

## 🚀 Quick Start

### Web Application
```bash
streamlit run app.py
```

### Programmatic Usage
```python
from w25_to_ssim_converter import gerar_ssim_w25_single_airline, gerar_ssim_w25_todas_companias

# Single airline
result = gerar_ssim_w25_single_airline("w25_schedule.xlsx", "KL", "klm.ssim")

# All airlines
result = gerar_ssim_w25_todas_companias("w25_schedule.xlsx", "all_airlines.ssim")
```

## 📊 Input Format - W25 Amsterdam

The W25 Excel file should contain Amsterdam-centric flight data with these key columns:

### **Required Columns**
* **`OP.D.1` to `OP/D/7`**: Operating days (1=Monday, 2=Tuesday, etc.)
* **`A.FLT`**: Arrival flight number (e.g., `6E0021` = IndiGo flight 21)
* **`STA`**: Scheduled Time of Arrival (HH:MM:SS format)
* **`ORIG`**: Origin airport (3-letter IATA code)
* **`ATY`**: Aircraft type (e.g., `789`, `320/321`)
* **`D.FLT`**: Departure flight number (e.g., `6E0022`)
* **`STD`**: Scheduled Time of Departure (HH:MM:SS format)
* **`DEST`**: Destination airport (3-letter IATA code or `N/S` for night stop)
* **`FROM`**: Effective date (start of operation period)
* **`TILL`**: Discontinue date (end of operation period)
* **`FLT.TYPE`**: Flight type (e.g., `J/J` for passenger, `F/F` for cargo)

### **W25 Logic**
1. **Turnarounds**: When both `A.FLT` and `D.FLT` are present in same row
2. **Night Stops**: When `DEST` = `N/S`, departure flight is in next row
3. **Airline Extraction**: First 2 characters of flight number (e.g., `6E0021` → `6E`)
4. **Aircraft Processing**: Use part before `/` if present (e.g., `320/321` → `320`)

## 📄 Output Format - IATA SSIM

Generates standard SSIM files with:

* **200-character lines** - IATA standard format
* **Complete structure** - Header, Carrier Info, Flight Records, Footer
* **AMS timezone** - All times in +0100 (Amsterdam timezone)
* **Link flights** - Proper connection between arrival and departure
* **Sequential numbering** - Each line properly numbered

### Sample SSIM Output:
```
1AIRLINE STANDARD SCHEDULE DATA SET                                                                                                                                                 00000001
2U6E  0008    14OCT2514OCT2514OCT25Created by AMS Team Dnata Brasil    PEN08                                                                                                       00000002
3 6E 00210101J14OCT2514OCT251234567 BOM0930+0000  AMS1130+0100  789 6E 0022                                                                                                      00000003
3 6E 00220101J14OCT2514OCT251234567 AMS1330+0100  BOM1530+0000  789                                                                                                              00000004
5 6E 14OCT25                                                                                                                                                    000003E000005
```

## 🏢 Supported Airlines

The converter automatically detects and processes any airline present in the W25 file, including:

* **6E** (IndiGo)
* **AI** (Air India) 
* **KL** (KLM Royal Dutch Airlines)
* **AF** (Air France)
* **LH** (Lufthansa)
* **BA** (British Airways)
* And many more...

## 🛠️ Installation

```bash
git clone https://github.com/luisluna97/ams-ssim-converter.git
cd ams-ssim-converter
pip install -r requirements.txt
```

## 📋 Dependencies

* `streamlit>=1.28.0` - Web interface framework
* `pandas>=1.5.0` - Data processing and Excel handling
* `openpyxl>=3.0.0` - Excel file support

## 🔧 Technical Features

### **W25 Processing Engine**
* **Flight Extraction** - Intelligent parsing of airline codes and flight numbers
* **Time Conversion** - Multiple time format support with AMS timezone
* **Operating Days** - Flexible day-of-week processing
* **Aircraft Mapping** - Automatic type code standardization
* **Period Processing** - FROM/TILL date range handling

### **SSIM Generation**
* **Header Management** - Proper SSIM file structure
* **Carrier Records** - Individual airline processing
* **Flight Records** - Complete flight leg information
* **Link Processing** - Turnaround and night stop connections
* **Footer Generation** - Proper file termination

### **User Interface**
* **Bilingual Support** - English and Dutch translations
* **Dutch Theme** - Orange color scheme (Dutch national color)
* **File Upload** - Drag-and-drop Excel file support
* **Data Preview** - Real-time airline and flight statistics
* **Conversion Modes** - Single airline or all airlines processing
* **Download Integration** - Direct SSIM file download

## 📁 Project Structure

```
ams-ssim-converter/
├── app.py                          # Streamlit web interface
├── w25_to_ssim_converter.py        # Core conversion engine
├── version.py                      # Version management
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
├── CHANGELOG.md                    # Version history
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── .gitignore                      # Git ignore rules
```

## 🎮 How to Use

### **Web Interface**
1. **Language Selection** - Choose English or Dutch in sidebar
2. **Upload W25 File** - Drag and drop your Excel file
3. **Preview Data** - Review airlines and flight statistics
4. **Select Mode** - Choose single airline or all airlines
5. **Convert** - Generate SSIM file with validation
6. **Download** - Get your SSIM file instantly

### **Command Line**
```python
# Import the converter
from w25_to_ssim_converter import gerar_ssim_w25_single_airline

# Convert single airline
result = gerar_ssim_w25_single_airline(
    excel_path="my_w25_schedule.xlsx",
    codigo_iata="KL",
    output_file="klm_schedule.ssim"
)

print(result)  # Success message with file details
```

## ✅ Validation Features

The converter includes comprehensive validation:

* ✅ **W25 Structure** - Validates required columns and data types
* ✅ **Airline Codes** - Ensures valid 2-character IATA codes
* ✅ **Time Formats** - Supports multiple time input formats
* ✅ **Date Processing** - Robust FROM/TILL period handling
* ✅ **SSIM Compliance** - Ensures 200-character line format
* ✅ **Link Validation** - Verifies turnaround and night stop connections

## 🌍 Amsterdam Focus

This converter is specifically designed for Amsterdam Schiphol Airport (AMS) operations:

* **AMS-Centric Data** - All flights have one leg in Amsterdam
* **Local Timezone** - Native +0100 (CET/CEST) processing  
* **Dutch Integration** - Bilingual interface with Dutch support
* **Schiphol Operations** - Optimized for AMS traffic patterns
* **European Standards** - IATA European region compliance

## 📞 Technical Support

**Developed by**: Capacity Dnata Brasil - AMS Team  
**Lead Developer**: Luis Luna  
**Contact**: luis.evaristo@dnata.com.br

For technical support, feature requests, or integration questions, please contact the AMS team or open an issue on GitHub.

## 🏆 Why AMS Converter?

This converter provides enterprise-grade reliability specifically for Amsterdam operations:

* ✅ **AMS Specialized** - Built specifically for Schiphol Airport data
* ✅ **IATA Compliance** - Strict adherence to SSIM standards
* ✅ **Production Ready** - Handles real-world AMS operations data
* ✅ **Dutch Integration** - Native Dutch language and cultural support
* ✅ **Intelligent Processing** - Automatic turnaround and night stop detection
* ✅ **Flexible Output** - Single airline or comprehensive multi-airline processing

## 📈 Version History

### v1.0.0 (2025-10-14) - Initial Release
* 🚀 **Core Functionality** - W25 to SSIM conversion engine
* 🇳🇱 **Dutch Theme** - Orange color scheme and bilingual interface
* ✈️ **AMS Focus** - Specialized for Amsterdam Schiphol operations
* 🔗 **Link Processing** - Turnaround and night stop handling
* 📊 **Multi-Mode** - Single airline and all airlines conversion
* 🎨 **Professional UI** - Modern Streamlit interface with Dutch styling

---

_Professional Amsterdam Airport Operations Tool - AMS Team - Capacity Dnata Brasil - 2025_
