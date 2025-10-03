#!/usr/bin/env python3
"""
Cliente File Reader - Main Application with Excel Export

This application demonstrates how to read and process fixed-width Cliente records
using the TracciatoRecordClienti specification, with automatic Excel export.

Usage:
    python main.py [filename] [options]

Options:
    --no-excel     Skip Excel export
    --no-summary   Don't include summary sheet in Excel

If no filename is provided, it will create and read a sample file.
"""

import sys
import os
import argparse
from cliente_reader import ClienteRecordReader, ClienteRecord
from generate_sample_data import generate_sample_file


def print_record_summary(record: ClienteRecord, record_num: int):
    """Print a summary of a single record"""
    print(f"Record #{record_num}:")
    print(f"  Progressivo: {record.progressivo}")
    print(f"  Codice: {record.codice}")
    print(f"  Ragione_sociale: {record.ragione_sociale}")
    print(f"  Nome e Cognome: {record.nome} {record.cognome}")
    print(f"  Indirizzo: {record.indirizzo}")
    print(f"  Città: {record.citta}")
    print(f"  Prov: {record.prov}")
    print(f"  Telefono: {record.telefono}")
    print(f"  Telefono2: {record.telefono2}")
    print(f"  Email: {record.email}")
    print(f"  Codice Fiscale: {record.codice_fiscale}")
    print(f"  Parole Chiave: {record.parole_chiave}")
    if record.partita_iva:
        print(f"  VAT: {record.partita_iva}")
    print(f"  Bonus: {record.bonus}")
    print(f"  Libero: {record.libero}")
    print(f"  CAP: {record.cap}")
    print(f"  Note: {record.note}")
    print(f"  Codice Cosmo: {record.codice_cosmo}")
    print(f"  Banca Cosmo: {record.banca_cosmo}")
    print(f"  Spedizione: {record.spedizione}")
    print(f"  Pagamento Cosmo: {record.pagamento_cosmo}")
    print(f"  Chiuso: {record.chiuso}")
    print(f"  Codice Sponsor: {record.codice_sponsor}")
    print(f"  Sponsor: {record.sponsor}")
    print(f"  Saldo Sponsor: {record.saldo_sponsor}")
    print(f"  Codice Doc: {record.codice_doc}")
    print(f"  Stato: {record.stato}")
    print(f"  Scadenza Bonus: {record.scadenza_bonus}")
    print(f"  Trasferito Promo: {record.trasferito_promo}")
    print(f"  Titolo: {record.titolo}")
    print(f"  Copia Offerta Da: {record.copiaoffertada}")
    print(f"  Codice Promo: {record.codicepromo}")
    print(f"  Promozionale: {record.promozionale}")
    print(f"  Sito Internet: {record.sitointernet}")
    print(f"  Indirizzo Fiscale: {record.indirizzofiscale}")
    print(f"  Città Fiscale: {record.cittafiscale}")
    print(f"  Prov Fiscale: {record.provfiscale}")
    print(f"  CAP Fiscale: {record.capfiscale}")
    print(f"  Nominativo Fiscale: {record.nominativofiscale}")
    print(f"  Edificio: {record.edificio}")
    print(f"  ID: {record.id}")
    print(f"  ID Adv Plan: {record.idadvplan}")
    print(f"  Varie: {record.varie}")
    print()


def print_field_analysis(records):
    """Print analysis of field usage across all records"""
    if not records:
        print("No records to analyze")
        return

    print("Field Analysis:")
    print("=" * 50)

    # Count non-empty fields
    field_usage = {}
    for record in records:
        for field_name in record.__dataclass_fields__.keys():
            value = getattr(record, field_name)
            if value and str(value).strip():
                field_usage[field_name] = field_usage.get(field_name, 0) + 1

    # Sort by usage frequency
    sorted_fields = sorted(field_usage.items(), key=lambda x: x[1], reverse=True)

    print(f"{'Field Name':<25} {'Used Count':<10} {'Usage %':<10}")
    print("-" * 45)

    total_records = len(records)
    for field_name, count in sorted_fields[:10]:  # Show top 10
        percentage = (count / total_records) * 100
        print(f"{field_name:<25} {count:<10} {percentage:.1f}%")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Cliente Record Reader with Excel Export')
    parser.add_argument('filename', nargs='?', help='Input data file')
    parser.add_argument('--no-excel', action='store_true', help='Skip Excel export')
    parser.add_argument('--no-summary', action='store_true', help='Don\'t include summary sheet')
    parser.add_argument('--fields', action='store_true', help='Show detailed field information')
    parser.add_argument('--output', '-o', help='Output Excel filename')
    return parser.parse_args()


def main():
    """Main application entry point"""
    args = parse_arguments()

    if args.fields:
        show_field_info()
        return

    print("Cliente Record Reader Application with Excel Export")
    print("=" * 60)

    # Determine input file
    if args.filename:
        filename = args.filename
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            return
    else:
        print("No filename provided. Creating sample data...")
        filename = generate_sample_file('sample_clienti.dat', 5)
        print()

    # Initialize reader
    reader = ClienteRecordReader()

    print(f"Reading file: {filename}")
    print(f"Expected record length: {reader.record_length} characters")
    print(f"Number of fields: {len(reader.fields)}")
    print()

    try:
        # Read records
        records = reader.read_file(filename)

        print(f"Successfully read {len(records)} records")
        print()

        if records:
            # Show first few records
            print("Record Details:")
            print("-" * 30)
            for i, record in enumerate(records[:3], 1):  # Show first 3 records
                print_record_summary(record, i)

            if len(records) > 3:
                print(f"... and {len(records) - 3} more records\n")

            # Field analysis
            print_field_analysis(records)

            # Excel export (unless disabled)
            if not args.no_excel:
                print("\n" + "=" * 40)
                print("Excel Export")
                print("=" * 40)

                # Determine output filename
                if args.output:
                    excel_filename = args.output
                else:
                    base_name = os.path.splitext(filename)[0]
                    excel_filename = f"{base_name}_clienti.xlsx"

                include_summary = not args.no_summary

                try:
                    result = reader.export_to_excel(records, excel_filename, include_summary)

                    if result:
                        print(f"✅ Excel export completed successfully!")
                        print(f"   📄 File: {excel_filename}")

                        file_size = os.path.getsize(excel_filename)
                        print(f"   📁 Size: {file_size:,} bytes")

                        if include_summary:
                            print("   📊 Sheets: Cliente_Data, Summary")
                        else:
                            print("   📊 Sheets: Cliente_Data")

                        print()
                        print("Excel file contents:")
                        print(f"  • {len(records)} data records")
                        print(f"  • {len(reader.fields)} columns")
                        if include_summary:
                            print("  • Summary with field usage analysis")
                        print("  • Auto-formatted headers and columns")

                except Exception as e:
                    print(f"❌ Excel export failed: {e}")
                    print("   Make sure pandas and openpyxl are installed:")
                    print("   pip install pandas openpyxl")
            else:
                print("\n📝 Excel export skipped (--no-excel flag)")

            # Validation
            print("\n" + "=" * 40)
            print("Validation")
            print("=" * 40)
            with open(filename, 'r', encoding='utf-8') as f:
                valid_count = 0
                invalid_count = 0
                for line_num, line in enumerate(f, 1):
                    clean_line = line.rstrip('\r\n')
                    if clean_line.strip():
                        is_valid = reader.validate_record_length(clean_line)
                        if is_valid:
                            valid_count += 1
                        else:
                            invalid_count += 1
                            print(f"❌ Line {line_num}: Invalid length ({len(clean_line)} chars, expected {reader.record_length})")

                if invalid_count == 0:
                    print(f"✅ All {valid_count} records have valid length")
                else:
                    print(f"⚠️  Found {invalid_count} invalid records out of {valid_count + invalid_count}")

        else:
            print("No valid records found in the file")

    except Exception as e:
        print(f"Error reading file: {e}")
        return


def show_field_info():
    """Show detailed field information"""
    reader = ClienteRecordReader()
    field_info = reader.get_field_info()

    print("Detailed Field Information")
    print("=" * 80)
    print(f"{'Field Name':<25} {'Type':<15} {'Length':<6} {'Start':<5} {'End':<5} {'Range'}")
    print("-" * 80)

    for field_name, info in field_info.items():
        range_str = f"{info['start_position']}-{info['end_position']}"
        print(f"{field_name:<25} {info['type']:<15} {info['length']:<6} "
              f"{info['start_position']:<5} {info['end_position']:<5} {range_str}")

    print(f"\nTotal record length: {sum(info['length'] for info in field_info.values())} characters")


if __name__ == "__main__":
    main()
