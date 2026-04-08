import csv
import re
import unicodedata

def normalize(name):
    if not name: return ""
    name = name.strip().upper()
    # Remove accents
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    # Replace dashes and multiple spaces with a single space
    name = re.sub(r'[- ]+', ' ', name)
    # Special cases if any
    if name == 'ST MEDARD EN JALLES': name = 'SAINT MEDARD EN JALLES'
    if name == 'ST LOUIS DE MONTFERRAND': name = 'SAINT LOUIS DE MONTFERRAND'
    if name == 'ST AUBIN DE MEDOC': name = 'SAINT AUBIN DE MEDOC'
    return name

years_files = {
    '2020': 'effectifs-de-police-municipale-2020 - Tableau croisé dynamique 1.csv',
    '2021': 'effectif de police 2021  - Tableau croisé dynamique 1.csv',
    '2022': 'effectif de police 2022 - Tableau croisé dynamique 1.csv',
    '2023': 'effectif de  police 2023 - Tableau croisé dynamique 1.csv',
    '2024': 'effectif de police 2024 - Tableau croisé effectif de police.csv'
}

all_police_data = {} # {commune_norm: {year: count}}

for year, filename in years_files.items():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if not row or len(row) < 2: continue
                commune_raw = row[0].strip('\xa0') # some files have &nbsp;
                commune = normalize(commune_raw)
                if commune == 'TOTAL GENERAL' or not commune: continue
                try:
                    count = int(re.sub(r'[^0-9]', '', row[1]))
                    if commune not in all_police_data:
                        all_police_data[commune] = {}
                    all_police_data[commune][year] = count
                except:
                    pass
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# GPS
gps_data = {}
with open('Feuille de calcul sans titre - Feuille 1 (3).csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        commune_raw = row['communes '].strip()
        commune = normalize(commune_raw)
        coords = row['coordonnées gps '].strip('"').split(',')
        if len(coords) == 2:
            gps_data[commune] = {
                'lat': coords[0].strip(),
                'lng': coords[1].strip(),
                'display_name': commune_raw
            }

# Merge
output = []
# Use keys from gps_data to ensure we only include communes we can map
for commune_norm, data in gps_data.items():
    row = {
        'commune': data['display_name'],
        'lat': data['lat'],
        'lng': data['lng']
    }
    police = all_police_data.get(commune_norm, {})
    for year in years_files.keys():
        row[f'agents_{year}'] = police.get(year, "N/A")
    output.append(row)

fieldnames = ['commune', 'lat', 'lng'] + [f'agents_{y}' for y in years_files.keys()]
with open('police_map_data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)

print(f"Merged {len(output)} communes.")
