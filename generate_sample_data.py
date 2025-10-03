# Sample Cliente Data Generator
# This script generates sample fixed-width data for testing

import os
from typing import List, Tuple

def create_sample_record(record_num: int = 1) -> str:
    """Create a sample fixed-width cliente record"""
    # Based on the field definitions, create a properly formatted record
    fields_data = [
        ('progressivo', f'{record_num:08d}', 8),           # Integer: Progressive number
        ('codice', f'CLI{record_num:03d}', 6),             # Alpha: Client code
        ('ragione_sociale', f'ACME Corporation SpA #{record_num}', 80),  # Alpha: Company name
        ('cognome', 'Rossi', 20),                          # Alpha: Last name
        ('nome', 'Mario', 20),                             # Alpha: First name
        ('indirizzo', f'Via Roma {100 + record_num}', 40), # Alpha: Address
        ('citta', 'Milano', 40),                           # Alpha: City
        ('prov', 'MI', 3),                                 # Alpha: Province
        ('telefono', f'02-{12345000 + record_num}', 20),   # Alpha: Phone
        ('telefono2', f'335-{1234000 + record_num}', 20),  # Alpha: Mobile phone
        ('email', '255', 255),                             # Integer: Email field length
        ('codice_fiscale', f'RSSMRA80A01F{200 + record_num}X', 16), # Alpha: Tax code
        ('parole_chiave', '12345678', 8),                  # Integer: Keywords
        ('partita_iva', f'{12345678000 + record_num}', 16), # Alpha: VAT number
        ('bonus', f'{1200 + (record_num * 100):012d}', 12), # Integer: Bonus amount
        ('libero', ' 1', 2),                               # Boolean: Free field
        ('cap', '20100', 5),                               # Alpha: ZIP code
        ('note', '255', 255),                              # Integer: Notes field
        ('codice_cosmo', f'COS{record_num:03d}', 6),       # Alpha: Cosmo code
        ('banca_cosmo', 'BAN001', 6),                      # Alpha: Bank code
        ('spedizione', 'Standard shipping method', 30),    # Alpha: Shipping
        ('pagamento_cosmo', 'PAG001', 6),                  # Alpha: Payment method
        ('chiuso', ' 0', 2),                               # Boolean: Closed
        ('codice_sponsor', f'SPO{record_num:03d}', 6),     # Alpha: Sponsor code
        ('sponsor', ' 1', 2),                              # Boolean: Is sponsor
        ('saldo_sponsor', f'{5000 + (record_num * 250):012d}', 12), # Integer: Sponsor balance
        ('codice_doc', f'{record_num:08d}', 8),            # Integer: Document code
        ('stato', 'Active', 40),                           # Alpha: Status
        ('scadenza_bonus', '20251231', 8),                 # Date: Bonus expiration
        ('trasferito_promo', ' 0', 2),                     # Boolean: Transferred promo
        ('titolo', 'Dott.', 20),                           # Alpha: Title
        ('copia_offerta_da', ' 0', 2),                     # Boolean: Copy offer from
        ('codice_promo', f'PROMO{record_num}', 6),         # Alpha: Promo code
        ('promozionale', ' 1', 2),                         # Boolean: Promotional
        ('sito_internet', '255', 255),                     # Integer: Website field
        ('indirizzo_fiscale', f'Via Roma {100 + record_num}', 40), # Alpha: Fiscal address
        ('citta_fiscale', 'Milano', 40),                   # Alpha: Fiscal city
        ('prov_fiscale', 'MI', 3),                         # Alpha: Fiscal province
        ('cap_fiscale', '20100', 5),                       # Alpha: Fiscal ZIP
        ('nominativo_fiscale', f'ACME Corporation SpA #{record_num}', 80), # Alpha: Fiscal name
        ('edificio', f'Building {chr(65 + (record_num % 5))}', 20), # Alpha: Building
        ('id', f'{record_num:08d}', 8),                    # Integer: ID
        ('id_adv_plan', f'{record_num:08d}', 8),           # Integer: Adv plan ID
        ('varie', f'Various information for record {record_num}', 255) # Alpha: Various
    ]

    # Build the fixed-width record
    record = ''
    for field_name, value, length in fields_data:
        # Pad or truncate the value to the exact field length
        formatted_value = str(value)[:length].ljust(length)
        record += formatted_value

    return record

def create_diverse_sample_records(num_records: int = 5) -> List[str]:
    """Create diverse sample records with varying data"""

    # Sample data variations
    companies = [
        'ACME Corporation SpA',
        'Beta Industries Srl',
        'Gamma Solutions Ltd',
        'Delta Manufacturing',
        'Epsilon Services SA'
    ]

    names = [
        ('Mario', 'Rossi'),
        ('Luigi', 'Verdi'),
        ('Anna', 'Bianchi'),
        ('Paolo', 'Neri'),
        ('Maria', 'Ferrari')
    ]

    cities = [
        ('Milano', 'MI', '20100'),
        ('Roma', 'RM', '00100'),
        ('Napoli', 'NA', '80100'),
        ('Torino', 'TO', '10100'),
        ('Bologna', 'BO', '40100')
    ]

    records = []

    for i in range(num_records):
        record_num = i + 1
        company = companies[i % len(companies)]
        name, surname = names[i % len(names)]
        city, province, cap = cities[i % len(cities)]

        # Create varied field data
        fields_data = [
            ('progressivo', f'{record_num:08d}', 8),
            ('codice', f'CLI{record_num:03d}', 6),
            ('ragione_sociale', company, 80),
            ('cognome', surname, 20),
            ('nome', name, 20),
            ('indirizzo', f'Via {surname} {100 + record_num}', 40),
            ('citta', city, 40),
            ('prov', province, 3),
            ('telefono', f'0{i+1}-{12345000 + record_num}', 20),
            ('telefono2', f'33{i+1}-{1234000 + record_num}', 20),
            ('email', '255', 255),
            ('codice_fiscale', f'{surname[:3].upper()}{name[:3].upper()}80A01F{200 + record_num}X', 16),
            ('parole_chiave', f'{12340000 + record_num:08d}', 8),
            ('partita_iva', f'{12345678000 + record_num * 1000}', 16),
            ('bonus', f'{1200 + (record_num * 100):012d}', 12),
            ('libero', f' {record_num % 2}', 2),
            ('cap', cap, 5),
            ('note', '255', 255),
            ('codice_cosmo', f'COS{record_num:03d}', 6),
            ('banca_cosmo', f'BAN{record_num:03d}', 6),
            ('spedizione', f'{["Standard", "Express", "Premium"][record_num % 3]} shipping', 30),
            ('pagamento_cosmo', f'PAG{record_num:03d}', 6),
            ('chiuso', f' {(record_num + 1) % 2}', 2),
            ('codice_sponsor', f'SPO{record_num:03d}', 6),
            ('sponsor', f' {record_num % 2}', 2),
            ('saldo_sponsor', f'{5000 + (record_num * 250):012d}', 12),
            ('codice_doc', f'{record_num:08d}', 8),
            ('stato', ['Active', 'Pending', 'Inactive'][record_num % 3], 40),
            ('scadenza_bonus', f'2025{(record_num % 12) + 1:02d}{(record_num % 28) + 1:02d}', 8),
            ('trasferito_promo', f' {(record_num + 1) % 2}', 2),
            ('titolo', ['Dott.', 'Ing.', 'Prof.', 'Sig.'][record_num % 4], 20),
            ('copia_offerta_da', f' {record_num % 2}', 2),
            ('codice_promo', f'PROMO{record_num}', 6),
            ('promozionale', f' {record_num % 2}', 2),
            ('sito_internet', '255', 255),
            ('indirizzo_fiscale', f'Via {surname} {100 + record_num}', 40),
            ('citta_fiscale', city, 40),
            ('prov_fiscale', province, 3),
            ('cap_fiscale', cap, 5),
            ('nominativo_fiscale', company, 80),
            ('edificio', f'Building {chr(65 + (record_num % 5))}', 20),
            ('id', f'{record_num:08d}', 8),
            ('id_adv_plan', f'{record_num:08d}', 8),
            ('varie', f'Record {record_num} - {name} {surname} from {city}', 255),
        ]

        # Build the fixed-width record
        record = ''
        for field_name, value, length in fields_data:
            formatted_value = str(value)[:length].ljust(length)
            record += formatted_value

        records.append(record)

    return records

def generate_sample_file(filename: str = 'sample_clienti.dat', num_records: int = 5, diverse: bool = True) -> str:
    """Generate a sample data file with multiple records"""

    if diverse:
        records = create_diverse_sample_records(num_records)
    else:
        records = [create_sample_record(i + 1) for i in range(num_records)]

    with open(filename, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(record + '\n')

    print(f"Created sample file '{filename}' with {num_records} records")
    print(f"Each record is {len(records[0]) if records else 0} characters long")

    # Show file size
    file_size = os.path.getsize(filename)
    print(f"File size: {file_size:,} bytes")

    return filename

def generate_large_sample_file(filename: str = 'large_sample_clienti.dat', num_records: int = 100) -> str:
    """Generate a larger sample file for performance testing"""
    return generate_sample_file(filename, num_records, diverse=True)

if __name__ == "__main__":
    # Generate different sample files
    print("Cliente Sample Data Generator")
    print("=" * 40)

    # Small diverse sample
    generate_sample_file('sample_clienti.dat', 5, diverse=True)

    print()

    # Larger sample for testing
    generate_sample_file('medium_sample_clienti.dat', 25, diverse=True)

    print()
    print("Sample files generated successfully!")
    print("Use these files to test the Cliente Record Reader with Excel export.")
