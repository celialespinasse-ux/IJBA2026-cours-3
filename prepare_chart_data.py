import csv
import json

file_path = 'délinquance nouvelle aquitaine (Bon) - Copie de Tableau croisé dynamique 3 1.csv'

# Définir les catégories
vols_categories = [
    "Vols d'accessoires sur véhicules",
    "Vols dans les véhicules",
    "Vols de véhicule",
    "Vols sans violence contre des personnes",
    "Vols violents sans arme"
]
violences_cat = "Violences physiques hors cadre familial"
cambriolages_cat = "Cambriolages de logement"

results = {}
years = ['2020', '2021', '2022', '2023', '2024', '2025']

with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    # Skip title and header
    next(reader) # SUM de taux_pour_mille,,annee,,,,,,
    header = next(reader) # indicateur,nom communes,2020,2021,2022,2023,2024,2025,Total général
    
    current_indicator = ""
    for row in reader:
        if not row or len(row) < 9:
            continue
        
        indicator = row[0].strip()
        if indicator:
            current_indicator = indicator
            
        city = row[1].strip()
        if not city or city == "Total général":
            continue
            
        if city not in results:
            results[city] = {
                'Vols (total)': [0.0] * 6,
                'Violences hors cadre familial': [0.0] * 6,
                'Cambriolages': [0.0] * 6
            }
            
        # Extract annual data
        for i, year in enumerate(years):
            val_str = row[i+2].replace(',', '.')
            try:
                val = float(val_str) if val_str else 0.0
            except ValueError:
                val = 0.0
                
            if current_indicator in vols_categories:
                results[city]['Vols (total)'][i] += val
            elif current_indicator == violences_cat:
                results[city]['Violences hors cadre familial'][i] = val
            elif current_indicator == cambriolages_cat:
                results[city]['Cambriolages'][i] = val

# Sauvegarder les données traitées
with open('delinquance_data.json', 'w', encoding='utf-8') as f:
    json.dump({'years': years, 'data': results}, f, ensure_ascii=False, indent=2)

print("Données extraites avec succès dans delinquance_data.json")
