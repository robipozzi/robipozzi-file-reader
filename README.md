# Cliente Record Reader with Excel Export

A Python project for reading and parsing fixed-width Cliente records based on the TracciatoRecordClienti specification, with **automatic Excel export functionality**.

## Overview

This project provides a complete solution for handling fixed-width record files containing customer (Cliente) data with **built-in Excel export**. It includes:

- **Fixed-width record parsing** with automatic type conversion
- **Automatic Excel export** with formatted sheets and summary analysis
- **Data validation** and error handling
- **Sample data generation** for testing
- **Comprehensive field analysis** tools
- **Professional Excel formatting** with auto-sized columns and styled headers

## New Excel Export Features ⭐

- **📊 Automatic Excel generation** after reading files
- **📈 Summary sheet** with field usage statistics
- **🎨 Professional formatting** with styled headers and auto-sized columns
- **📋 Multi-sheet workbooks** (Data + Summary)
- **🔢 Smart data type handling** (dates, booleans, integers)
- **📁 Flexible naming** with automatic filename generation

## Installation

```bash
# Install required dependencies for Excel export
pip install pandas openpyxl

# Or install from requirements.txt
pip install -r requirements.txt
```

## Files Structure

```
cliente-reader/
├── TracciatoRecordClienti.txt    # Original record specification
├── cliente_reader.py             # Main parsing library with Excel export
├── generate_sample_data.py       # Sample data generator
├── main.py                       # Enhanced main application
├── requirements.txt              # Updated with pandas/openpyxl
└── README.md                     # This file
```

## Record Specification

The Cliente record contains **44 fields** with a total length of **1,698 characters**:

| Field Category | Count | Examples |
|---------------|--------|----------|
| Identifiers   | 6      | Progressivo, Codice, ID |
| Personal Info | 8      | Nome, Cognome, Codice_Fiscale |
| Address       | 10     | Indirizzo, Citta, CAP |
| Business      | 8      | Ragione_sociale, Partita_IVA |
| Financial     | 6      | Bonus, Saldo_sponsor |
| Boolean Flags | 6      | Libero, Chiuso, Sponsor |

## Quick Start

### 1. Basic Usage with Excel Export

```bash
# Run with sample data (automatically creates Excel file)
python main.py

# Run with your own data file (creates corresponding Excel file)
python main.py your_data_file.dat

# Skip Excel export
python main.py your_data_file.dat --no-excel

# Custom Excel output filename
python main.py your_data_file.dat --output my_export.xlsx

# Skip summary sheet in Excel
python main.py your_data_file.dat --no-summary
```

### 2. Using the Enhanced Library

```python
from cliente_reader import ClienteRecordReader

# Initialize reader
reader = ClienteRecordReader()

# Read and automatically export to Excel
excel_file = reader.read_and_export_to_excel('cliente_data.dat')
print(f"Excel file created: {excel_file}")

# Or read first, then export with custom options
records = reader.read_file('cliente_data.dat')
reader.export_to_excel(records, 'custom_output.xlsx', include_summary=True)

# Convert to pandas DataFrame for further analysis
import pandas as pd
df = reader.records_to_dataframe(records)
print(df.head())
```

### 3. Excel Output Features

The generated Excel file includes:

**Data Sheet (`Cliente_Data`):**
- All 44 fields as columns
- Properly formatted headers with styling
- Auto-sized column widths
- Date fields formatted as YYYY-MM-DD
- Boolean fields as True/False

**Summary Sheet (`Summary`):**
- Total record count and field statistics
- Field usage analysis showing which fields are populated
- Data type information for each field
- Usage percentages for data quality assessment

## Example Excel Output

```
Cliente_Data Sheet:
┌─────────────┬────────┬──────────────────┬─────────┬───────┬─────────────┐
│ progressivo │ codice │ ragione_sociale  │ cognome │ nome  │ indirizzo   │
├─────────────┼────────┼──────────────────┼─────────┼───────┼─────────────┤
│           1 │ CLI001 │ ACME Corporation │ Rossi   │ Mario │ Via Roma 123│
│           2 │ CLI002 │ Beta Industries  │ Verdi   │ Luigi │ Via Milano 5│
└─────────────┴────────┴──────────────────┴─────────┴───────┴─────────────┘

Summary Sheet:
┌─────────────────────┬─────────────┬────────┬──────────────┬─────────┐
│ Field Name          │ Data Type   │ Length │ Non-Empty    │ Usage % │
├─────────────────────┼─────────────┼────────┼──────────────┼─────────┤
│ progressivo         │ integer     │      8 │           25 │  100.0% │
│ codice              │ alpha field │      6 │           25 │  100.0% │
│ ragione_sociale     │ alpha field │     80 │           23 │   92.0% │
└─────────────────────┴─────────────┴────────┴──────────────┴─────────┘
```

## Features

### Enhanced Excel Export
- **Automatic Excel generation** after reading any file
- **Professional formatting** with styled headers and borders
- **Smart column sizing** based on content length
- **Multi-sheet workbooks** with data and summary
- **Data type preservation** with proper Excel formatting

### Data Validation
- Record length validation
- Type conversion with error handling
- Missing field detection
- Excel file verification

### Analysis Tools
- Field usage statistics in Excel summary
- Record summary reports
- Data quality metrics
- Usage percentage calculations

### Error Handling
- Graceful handling of malformed records
- Detailed error reporting with line numbers
- Automatic padding for short records
- Excel export error recovery

## Example Console Output

```
Cliente Record Reader Application with Excel Export
============================================================
Reading file: sample_clienti.dat
Expected record length: 1698 characters
Number of fields: 44

Successfully read 5 records

Record Details:
------------------------------
Record #1:
  Progressive: 1
  Code: CLI001
  Company: ACME Corporation SpA
  Name: Mario Rossi
  City: Milano (MI)

========================================
Excel Export
========================================
Reading file: sample_clienti.dat
Found 5 records
Exporting to Excel: sample_clienti_clienti.xlsx
✅ Excel file created successfully: sample_clienti_clienti.xlsx
   📊 Includes summary sheet with field analysis
   📁 File size: 15,234 bytes

Excel file contents:
  • 5 data records
  • 44 columns
  • Summary with field usage analysis
  • Auto-formatted headers and columns
```

## Requirements

- **Python 3.7+**
- **pandas** (for DataFrame operations and Excel export)
- **openpyxl** (for Excel file creation and formatting)

Install with: `pip install pandas openpyxl`

## Command Line Options

```bash
python main.py [filename] [options]

Options:
  --no-excel     Skip Excel export
  --no-summary   Don't include summary sheet in Excel
  --output, -o   Custom Excel output filename  
  --fields       Show detailed field information
```

## Development

### Adding Custom Excel Formatting

```python
# Extend the export_to_excel method for custom formatting
def custom_excel_export(self, records, filename):
    df = self.records_to_dataframe(records)

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)

        # Add custom formatting
        workbook = writer.book
        worksheet = writer.sheets['Data']

        # Your custom formatting code here
```

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions about the record specification, refer to the original `TracciatoRecordClienti.txt` file.

For Excel export issues, ensure pandas and openpyxl are properly installed.
