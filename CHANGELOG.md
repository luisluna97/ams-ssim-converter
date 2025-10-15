# Changelog - AMS SSIM Converter

All notable changes to the AMS SSIM Converter project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2025-10-15

### Fixed
- 🐛 **Flight Number Extraction Bug**: Fixed regex to correctly extract flight numbers from airlines with numeric codes
  - Airlines like `6E` (IndiGo) were extracting wrong numbers
  - Example: `6E0021` was extracting as `0006` instead of `0021`
  - **Root Cause**: Regex `r'([0-9]+)'` was capturing first digit (6) instead of full number (0021)
  - **Solution**: Changed to `r'^[A-Z]*([0-9]+)'` to skip letters and capture numbers after
  - **Impact**: All numeric airline codes now work correctly (6E, 9W, etc.)

### Changed
- 🔧 **Flight Number Processing**: Removed `[:4]` truncation to support longer flight numbers
  - Previous: `numero.zfill(4)[:4]` (truncated at 4 digits)
  - Current: `numero.zfill(4)` (preserves all digits, zero-pads if needed)

### Test Results
- ✅ `6E0021` → `0021` (previously: `0006`)
- ✅ `6E0022` → `0022` (previously: `0006`)
- ✅ All 18 airlines: 1,481 flights processed correctly
- ✅ All lines: Exactly 200 characters

---

## [1.0.0] - 2025-10-14

### Added - Initial Release
- 🚀 **Core Dutch Schedule to SSIM Conversion Engine**
  - Complete Amsterdam schedule processing
  - IATA SSIM standard compliance (200-character lines)
  - Multi-airline support with automatic detection
  
### Technical Implementation
- ✅ **Days of Operation**: Correct spacing format (e.g., "1  4 67" for days 1, 4, 6, 7)
- ✅ **Next Flight Field**: Proper linking of turnarounds and night stops
- ✅ **Turnaround Processing**: A.FLT + D.FLT in same row → arrival links to departure
- ✅ **Night Stop Logic**: DEST=N/S → D.FLT shows departure flight
- ✅ **Unlinked Flights**: Repeat own information in next flight field
- ✅ **Single Header/Footer**: One header and footer for all airlines (no duplicates)
- ✅ **No Mid-File Zeros**: Zero lines only at start and end of file
- ✅ **Exact 200 Characters**: Every line precisely 200 characters
  
- 🇳🇱 **Dutch-Themed Interface**
  - Orange color scheme (Dutch national color)
  - Bilingual support (English/Dutch)
  - Professional Streamlit web interface
  
- ✈️ **Amsterdam-Specific Features**
  - AMS timezone processing (+0100 CET/CEST)
  - Turnaround flight linking (A.FLT ↔ D.FLT)
  - Night stop processing (N/S handling)
  - FROM/TILL period management
  
- 📊 **Data Processing Capabilities**
  - Intelligent airline code extraction (e.g., 6E0021 → 6E)
  - Aircraft type processing (320/321 → 320)
  - Operating days conversion (OP.D.1-7 format)
  - Flight type processing (J/J, F/F support)
  
- 🔧 **Technical Features**
  - Excel file upload and processing
  - Real-time data preview and statistics
  - Single airline or all airlines conversion modes
  - Automatic SSIM file generation and download
  - Comprehensive error handling and validation
  
- 📋 **Documentation**
  - Complete README with usage examples
  - Technical documentation for developers
  - Bilingual help system in application
  - Version management system

### Technical Details
- **Framework**: Streamlit 1.28.0+
- **Data Processing**: Pandas 1.5.0+
- **File Support**: Excel (.xlsx) via openpyxl 3.0.0+
- **Output Format**: IATA SSIM standard
- **Timezone**: Amsterdam +0100 (CET/CEST)
- **Languages**: English, Dutch (Nederlands)

### Supported W25 Columns
- `OP.D.1` to `OP/D/7` - Operating days
- `A.FLT` - Arrival flight number
- `STA` - Scheduled Time of Arrival
- `ORIG` - Origin airport
- `ATY` - Aircraft type
- `D.FLT` - Departure flight number  
- `STD` - Scheduled Time of Departure
- `DEST` - Destination airport
- `FROM` - Effective date
- `TILL` - Discontinue date
- `FLT.TYPE` - Flight type (J/F classification)

### SSIM Output Features
- Header record (Line 1)
- Carrier information records (Line 2U)
- Flight leg records (Line 3)
- Footer record (Line 5)
- 200-character line formatting
- Sequential line numbering
- Link flight processing
- Proper timezone handling

---

## Future Releases

### Planned Features
- [ ] **Enhanced Aircraft Mapping** - Extended aircraft type database
- [ ] **Advanced Validation** - More comprehensive data validation
- [ ] **Batch Processing** - Multiple file processing capability
- [ ] **API Integration** - REST API for programmatic access
- [ ] **Export Options** - Additional output formats (CSV, JSON)
- [ ] **Historical Analysis** - Schedule comparison and analysis tools

### Potential Improvements
- [ ] **Performance Optimization** - Large file processing improvements
- [ ] **UI Enhancements** - Additional visualization features
- [ ] **Language Support** - Additional European languages
- [ ] **Integration Tools** - Direct airline system integration
- [ ] **Reporting Features** - Schedule analysis and reporting

---

**Developed by**: AMS Team - Capacity Dnata Brasil  
**Contact**: luis.evaristo@dnata.com.br  
**Repository**: https://github.com/luisluna97/ams-ssim-converter
