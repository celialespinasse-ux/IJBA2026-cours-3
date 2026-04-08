import csv
import re
import unicodedata

def normalize(name):
    if not name: return ""
    # Standardize spaces and case
    name = name.strip().upper()
    # Remove accents
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    # Replace anything not a letter or digit with a space
    name = re.sub(r'[^A-Z0-9]+', ' ', name)
    # Collapse multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def clean_number(s):
    if not s: return 0
    # Remove all non-digits (like spaces or dots for thousands)
    s = re.sub(r'[^0-9,]', '', s)
    if ',' in s:
        s = s.split(',')[0]
    return int(s) if s else 0

# Official Coordinates from Search
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

# Police Data Mapping
police_stats = {}
with open('effectif de police 2024 - Tableau croisé effectif de police.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # Header
    for row in reader:
        if not row or "Total" in row[0]: continue
        norm_name = normalize(row[0])
        agents = clean_number(row[1])
        pop = clean_number(row[2])
        police_stats[norm_name] = {'agents': agents, 'pop': pop}

# Final Merge
final_data = []
for name, coords in official_coords.items():
    stats = police_stats.get(name, {'agents': 0, 'pop': 0})
    agents = stats['agents']
    pop = stats['pop']
    density = (agents / pop * 1000) if pop > 0 else 0
    
    # Proper capitalization for display
    display_name = name.title().replace(" Sur ", "-sur-").replace(" En ", "-en-").replace(" Pres ", "-près-").replace(" De ", "-de-")
    if display_name == "Bordeaux": display_name = "Bordeaux"

    final_data.append({
        'commune': display_name,
        'lat': coords[0],
        'lng': coords[1],
        'agents': agents,
        'population': pop,
        'densite': round(density, 2)
    })

with open('police_map_data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['commune', 'lat', 'lng', 'agents', 'population', 'densite'])
    writer.writeheader()
    writer.writerows(final_data)

print(f"Processed {len(final_data)} communes.")
