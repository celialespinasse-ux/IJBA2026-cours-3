import csv
import re
import unicodedata

def normalize(name):
    if not name: return ""
    name = name.strip().upper()
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = re.sub(r'[^A-Z0-9]+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def clean_number(s):
    if not s: return 0
    s = re.sub(r'[^0-9,]', '', s)
    if ',' in s: s = s.split(',')[0]
    return int(s) if s else 0

official_coords = {
    "AMBARES ET LAGRAVE": (44.9244, -0.4851),
    "AMBES": (45.0131, -0.5314),
    "ARTIGUES PRES BORDEAUX": (44.8598, -0.4951),
    "BASSENS": (44.9039, -0.5172),
    "BEGLES": (44.8078, -0.5494),
    "BLANQUEFORT": (44.9111, -0.6381),
    "BORDEAUX": (44.8378, -0.5792),
    "BOULIAC": (44.8133, -0.5011),
    "BRUGES": (44.8825, -0.6122),
    "CARBON BLANC": (44.8953, -0.5064),
    "CENON": (44.8572, -0.5322),
    "EYSINES": (44.8844, -0.6503),
    "FLOIRAC": (44.8372, -0.5244),
    "GRADIGNAN": (44.7722, -0.6172),
    "LE BOUSCAT": (44.8653, -0.5994),
    "LE HAILLAN": (44.8722, -0.6781),
    "LE TAILLAN MEDOC": (44.9053, -0.6694),
    "LORMONT": (44.8789, -0.5222),
    "MARTIGNAS SUR JALLE": (44.8411, -0.7761),
    "MERIGNAC": (44.8386, -0.6472),
    "PAREMPUYRE": (44.9494, -0.6053),
    "PESSAC": (44.8061, -0.6311),
    "SAINT AUBIN DE MEDOC": (44.9122, -0.7231),
    "SAINT LOUIS DE MONTFERRAND": (44.9522, -0.5411),
    "SAINT MEDARD EN JALLES": (44.8961, -0.7181),
    "SAINT VINCENT DE PAUL": (44.9544, -0.4694),
    "TALENCE": (44.8011, -0.5903),
    "VILLENAVE D ORNON": (44.7733, -0.5672)
}

files = {
    '2020': 'effectifs-de-police-municipale-2020 - Tableau croisé dynamique 1.csv',
    '2021': 'effectif de police 2021  - Tableau croisé dynamique 1.csv',
    '2022': 'effectif de police 2022 - Tableau croisé dynamique 1.csv',
    '2023': 'effectif de  police 2023 - Tableau croisé dynamique 1.csv',
    '2024': 'effectif de police 2024 - Tableau croisé effectif de police.csv'
}

data_by_commune = {name: {year: 0 for year in files.keys()} for name in official_coords.keys()}

for year, filename in files.items():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if not row or "Total" in row[0]: continue
                norm_name = normalize(row[0])
                if norm_name in data_by_commune:
                    data_by_commune[norm_name][year] = clean_number(row[1])
    except Exception as e:
        print(f"Error reading {filename}: {e}")

output = []
for name, years_data in data_by_commune.items():
    lat, lng = official_coords[name]
    row = {'commune': name.title(), 'lat': lat, 'lng': lng}
    row.update(years_data)
    output.append(row)

with open('police_evolution.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['commune', 'lat', 'lng', '2020', '2021', '2022', '2023', '2024'])
    writer.writeheader()
    writer.writerows(output)

print("Evolution data ready.")
