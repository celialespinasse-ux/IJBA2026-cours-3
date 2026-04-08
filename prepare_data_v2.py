import csv
import re
import unicodedata

def normalize(name):
    if not name: return ""
    name = name.replace('\xa0', ' ')
    name = name.strip().upper()
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = re.sub(r'[- ]+', ' ', name)
    return name

def clean_number(s):
    if not s: return 0
    # The crucial part: remove ALL whitespace characters including \xa0
    s = "".join(s.split())
    # Handle European decimal comma (though population shouldn't have it, but for safety)
    s = s.replace(',', '.')
    # If there's a dot for thousands, remove it IF it's followed by 3 digits
    # But here the CSV seems to use spaces for thousands and comma for decimals.
    # After join(split()), "17 500,00" becomes "17500,00"
    if ',' in s:
        s = s.split(',')[0] # We want the integer part for population and agents
    match = re.search(r'([0-9]+)', s)
    if match:
        return int(match.group(1))
    return 0

# 1. Load GPS
gps_data = {}
with open('Feuille de calcul sans titre - Feuille 1 (3).csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        commune_raw = row['communes '].strip()
        commune_norm = normalize(commune_raw)
        coords = row['coordonnées gps '].strip('"').split(',')
        if len(coords) == 2:
            gps_data[commune_norm] = {
                'lat': coords[0].strip(),
                'lng': coords[1].strip(),
                'display_name': commune_raw
            }

# 2. Load Police 2024
police_2024 = {}
population_2024 = {}
with open('effectif de police 2024 - Tableau croisé effectif de police.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        if not row or "Total" in row[0]: continue
        commune_norm = normalize(row[0])
        agents = clean_number(row[1])
        pop = clean_number(row[2])
        police_2024[commune_norm] = agents
        population_2024[commune_norm] = pop

# 3. Merge
output = []
for commune_norm, data in gps_data.items():
    agents = police_2024.get(commune_norm, 0)
    pop = population_2024.get(commune_norm, 0)
    
    # Calculate density: agents per 1000 inhabitants
    density = (agents / pop * 1000) if pop > 0 else 0
    
    output.append({
        'commune': data['display_name'],
        'lat': data['lat'],
        'lng': data['lng'],
        'agents_2024': agents,
        'population': pop,
        'densite': round(density, 2)
    })

with open('police_map_data.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['commune', 'lat', 'lng', 'agents_2024', 'population', 'densite']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)

print("Data regenerated with correct thousands handling.")
