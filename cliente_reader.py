"""
Cliente Record Reader - Python module for reading fixed-width Cliente records

This module provides functionality to read and parse fixed-width records
based on the TracciatoRecordClienti specification, with Excel export capability.

Author: Generated from record specification
"""

from dataclasses import dataclass, fields
from typing import List, Optional, Any, Dict
from datetime import datetime, date
import re
import pandas as pd
import os


@dataclass
class ClienteField:
    """Represents a field definition in the Cliente record"""
    name: str
    length: int
    field_type: str
    start_pos: int = 0

    def parse_value(self, raw_value: str) -> Any:
        """Parse raw string value based on field type"""
        clean_value = raw_value.strip()

        if self.field_type == 'integer':
            return int(clean_value) if clean_value and clean_value.isdigit() else 0
        elif self.field_type == 'boolean':
            return clean_value.upper() in ['TRUE', '1', 'Y', 'S', 'SI'] or clean_value.strip() == '1'
        elif self.field_type == 'date':
            # Assuming YYYYMMDD format for 8-character dates
            if len(clean_value) == 8 and clean_value.isdigit():
                try:
                    year = int(clean_value[:4])
                    month = int(clean_value[4:6])
                    day = int(clean_value[6:8])
                    return date(year, month, day)
                except ValueError:
                    return None
            return None
        else:  # alpha field
            return clean_value


@dataclass
class ClienteRecord:
    """Represents a complete Cliente record with all fields"""
    progressivo: str = 0
    codice: str = ''
    ragione_sociale: str = ''
    cognome: str = ''
    nome: str = ''
    indirizzo: str = ''
    citta: str = ''
    prov: str = ''
    telefono: str = ''
    telefono2: str = ''
    email: str = 0
    codice_fiscale: str = ''
    parole_chiave: int = 0
    partita_iva: str = ''
    bonus: int = 0
    libero: bool = False
    cap: str = ''
    note: int = 0
    codice_cosmo: str = ''
    banca_cosmo: str = ''
    spedizione: str = ''
    pagamento_cosmo: str = ''
    chiuso: bool = False
    codice_sponsor: str = ''
    sponsor: bool = False
    saldo_sponsor: int = 0
    codice_doc: int = 0
    stato: str = ''
    scadenza_bonus: Optional[date] = None
    trasferito_promo: bool = False
    titolo: str = ''
    copiaoffertada: bool = False
    codicepromo: str = ''
    promozionale: bool = False
    sitointernet: int = 0
    indirizzofiscale: str = ''
    cittafiscale: str = ''
    provfiscale: str = ''
    capfiscale: str = ''
    nominativofiscale: str = ''
    edificio: str = ''
    id: int = 0
    idadvplan: int = 0
    varie: str = ''

    def to_dict(self) -> Dict[str, Any]:
        """Convert the record to a dictionary for easy DataFrame creation"""
        record_dict = {}
        for field in fields(self):
            value = getattr(self, field.name)
            # Convert dates to string for Excel compatibility
            if isinstance(value, date):
                record_dict[field.name] = value.strftime('%Y-%m-%d')
            else:
                record_dict[field.name] = value
        return record_dict


class ClienteRecordReader:
    """Fixed-width record reader for Cliente files with Excel export"""

    def __init__(self):
        """Initialize the reader with field specifications"""
        self.fields = self._define_fields()
        self.record_length = sum(field.length for field in self.fields)

    def _define_fields(self) -> List[ClienteField]:
        """Define all fields with their positions and types"""
        fields_spec = [
            ClienteField('progressivo', 8, 'alpha field', 0),
            ClienteField('codice', 6, 'alpha field', 8),
            ClienteField('ragione_sociale', 80, 'alpha field', 14),
            ClienteField('cognome', 20, 'alpha field', 94),
            ClienteField('nome', 20, 'alpha field', 114),
            ClienteField('indirizzo', 40, 'alpha field', 134),
            ClienteField('citta', 40, 'alpha field', 174),
            ClienteField('prov', 3, 'alpha field', 214),
            ClienteField('telefono', 20, 'alpha field', 217),
            ClienteField('telefono2', 20, 'alpha field', 237),
            ClienteField('email', 255, 'alpha field', 257),
            ClienteField('codice_fiscale', 16, 'alpha field', 512),
            ClienteField('parole_chiave', 8, 'integer', 528),
            ClienteField('partita_iva', 16, 'alpha field', 536),
            ClienteField('bonus', 12, 'integer', 552),
            ClienteField('libero', 2, 'boolean', 564),
            ClienteField('cap', 5, 'alpha field', 566),
            ClienteField('note', 255, 'integer', 571),
            ClienteField('codice_cosmo', 6, 'alpha field', 826),
            ClienteField('banca_cosmo', 6, 'alpha field', 832),
            ClienteField('spedizione', 30, 'alpha field', 838),
            ClienteField('pagamento_cosmo', 6, 'alpha field', 868),
            ClienteField('chiuso', 2, 'boolean', 874),
            ClienteField('codice_sponsor', 6, 'alpha field', 876),
            ClienteField('sponsor', 2, 'boolean', 882),
            ClienteField('saldo_sponsor', 12, 'integer', 884),
            ClienteField('codice_doc', 8, 'integer', 896),
            ClienteField('stato', 40, 'alpha field', 904),
            ClienteField('scadenza_bonus', 8, 'date', 944),
            ClienteField('trasferito_promo', 2, 'boolean', 952),
            ClienteField('titolo', 20, 'alpha field', 954),
            ClienteField('copiaoffertada', 2, 'boolean', 974),
            ClienteField('codicepromo', 6, 'alpha field', 976),
            ClienteField('promozionale', 2, 'boolean', 982),
            ClienteField('sitointernet', 255, 'integer', 984),
            ClienteField('indirizzofiscale', 40, 'alpha field', 1239),
            ClienteField('cittafiscale', 40, 'alpha field', 1279),
            ClienteField('provfiscale', 3, 'alpha field', 1319),
            ClienteField('capfiscale', 5, 'alpha field', 1322),
            ClienteField('nominativofiscale', 80, 'alpha field', 1327),
            ClienteField('edificio', 20, 'alpha field', 1407),
            ClienteField('id', 8, 'integer', 1427),
            ClienteField('idadvplan', 8, 'integer', 1435),
            ClienteField('varie', 255, 'alpha field', 1443),
        ]
        return fields_spec

    def parse_record(self, line: str) -> ClienteRecord:
        """Parse a single fixed-width record line into a ClienteRecord object"""
        if len(line) < self.record_length:
            # Pad the line if it's shorter than expected
            line = line.ljust(self.record_length)

        values = {}

        for field_def in self.fields:
            start = field_def.start_pos
            end = start + field_def.length
            raw_value = line[start:end]
            parsed_value = field_def.parse_value(raw_value)
            values[field_def.name] = parsed_value

        return ClienteRecord(**values)

    def read_file(self, filename: str, encoding: str = 'utf-8') -> List[ClienteRecord]:
        """Read an entire file and return list of ClienteRecord objects"""
        records = []

        with open(filename, 'r', encoding=encoding) as file:
            for line_num, line in enumerate(file, 1):
                try:
                    # Remove newline characters but preserve record structure
                    clean_line = line.rstrip('\r\n')
                    if clean_line.strip():  # Skip empty lines
                        record = self.parse_record(clean_line)
                        records.append(record)
                except Exception as e:
                    print(f"Error parsing line {line_num}: {e}")
                    print(f"Line content: {repr(line)}")

        return records

    def records_to_dataframe(self, records: List[ClienteRecord]) -> pd.DataFrame:
        """Convert list of ClienteRecord objects to pandas DataFrame"""
        if not records:
            return pd.DataFrame()

        # Convert each record to dictionary
        data = [record.to_dict() for record in records]

        # Create DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to match field order
        field_names = [field.name for field in self.fields]
        df = df.reindex(columns=field_names)

        return df

    def export_to_excel(self, records: List[ClienteRecord], output_filename: str, 
                       include_summary: bool = True) -> str:
        """Export records to Excel file with optional summary sheet"""

        # Create DataFrame
        df = self.records_to_dataframe(records)

        if df.empty:
            print("No records to export")
            return None

        # Create Excel writer object
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:

            # Write main data sheet
            df.to_excel(writer, sheet_name='Cliente_Data', index=False)

            # Get the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Cliente_Data']

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass

                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width

            # Add header formatting if openpyxl is available
            try:
                header_font = openpyxl.styles.Font(bold=True, color="FFFFFF")
                header_fill = openpyxl.styles.PatternFill(start_color="366092", end_color="366092", fill_type="solid")

                for cell in worksheet[1]:  # First row
                    cell.font = header_font
                    cell.fill = header_fill
            except NameError:
                pass  # openpyxl not available, skip formatting

            # Add summary sheet if requested
            if include_summary:
                self._create_summary_sheet(writer, df, records)

        return output_filename

    def _create_summary_sheet(self, writer, df: pd.DataFrame, records: List[ClienteRecord]):
        """Create a summary sheet with statistics and field information"""

        summary_data = []

        # Basic statistics
        summary_data.append(['Total Records', len(records)])
        summary_data.append(['Total Fields', len(self.fields)])
        summary_data.append(['Record Length', f'{self.record_length} characters'])
        summary_data.append([''])  # Empty row

        # Field usage analysis
        summary_data.append(['Field Usage Analysis', ''])
        summary_data.append(['Field Name', 'Data Type', 'Length', 'Non-Empty Count', 'Usage %'])

        for field_def in self.fields:
            field_name = field_def.name
            non_empty_count = 0

            for record in records:
                value = getattr(record, field_name)
                if value and str(value).strip() and str(value) != '0':
                    non_empty_count += 1

            usage_percent = (non_empty_count / len(records) * 100) if records else 0

            summary_data.append([
                field_name,
                field_def.field_type,
                field_def.length,
                non_empty_count,
                f'{usage_percent:.1f}%'
            ])

        # Create summary DataFrame and write to Excel
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False, header=False)

        # Format the summary sheet
        summary_worksheet = writer.sheets['Summary']

        # Auto-adjust column widths for summary
        for column in summary_worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            adjusted_width = min(max_length + 2, 30)
            summary_worksheet.column_dimensions[column_letter].width = adjusted_width

    def read_and_export_to_excel(self, input_filename: str, output_filename: str = None,
                                encoding: str = 'utf-8', include_summary: bool = True) -> str:
        """Read a file and automatically export to Excel"""

        # Generate output filename if not provided
        if output_filename is None:
            base_name = os.path.splitext(input_filename)[0]
            output_filename = f"{base_name}_clienti.xlsx"

        print(f"Reading file: {input_filename}")

        # Read records
        records = self.read_file(input_filename, encoding)

        if not records:
            print("No records found to export")
            return None

        print(f"Found {len(records)} records")
        print(f"Exporting to Excel: {output_filename}")

        # Export to Excel
        result = self.export_to_excel(records, output_filename, include_summary)

        if result:
            print(f"✅ Excel file created successfully: {output_filename}")
            if include_summary:
                print("   📊 Includes summary sheet with field analysis")

            # File size info
            file_size = os.path.getsize(output_filename)
            print(f"   📁 File size: {file_size:,} bytes")

        return result

    def validate_record_length(self, line: str) -> bool:
        """Validate that a record line has the expected length"""
        return len(line.rstrip('\r\n')) == self.record_length

    def get_field_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all fields"""
        return {
            field.name: {
                'length': field.length,
                'type': field.field_type,
                'start_position': field.start_pos,
                'end_position': field.start_pos + field.length - 1
            }
            for field in self.fields
        }


# Import openpyxl for Excel formatting
try:
    import openpyxl
    import openpyxl.styles
except ImportError:
    print("Warning: openpyxl not found. Excel formatting will be basic.")
    openpyxl = None


def main():
    """Example usage of the ClienteRecordReader with Excel export"""
    reader = ClienteRecordReader()

    print("Cliente Record Reader with Excel Export")
    print("=" * 50)
    print(f"Expected record length: {reader.record_length} characters")
    print(f"Number of fields: {len(reader.fields)}")
    print()

    # Display field information
    print("Field definitions:")
    print(f"{'Field Name':<25} {'Type':<15} {'Length':<6} {'Start':<5} {'End':<5}")
    print("-" * 70)

    for field_def in reader.fields:
        end_pos = field_def.start_pos + field_def.length - 1
        print(f"{field_def.name:<25} {field_def.field_type:<15} {field_def.length:<6} {field_def.start_pos:<5} {end_pos:<5}")


if __name__ == "__main__":
    main()
