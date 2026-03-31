import csv

input_file = 'subventions-metropole-de-bordeaux.csv'
output_file = 'subventions_nettoyees.csv'

def clean_id(val):
    if not val:
        return ""
    # Enlève le .0 si c'est un flottant
    if val.endswith('.0'):
        return val[:-2]
    return val

with open(input_file, mode='r', encoding='utf-8') as infile:
    # On saute la toute première ligne de titre
    infile.readline()
    
    reader = csv.DictReader(infile, delimiter=';')
    fieldnames = reader.fieldnames
    
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        
        for row in reader:
            # Nettoyage des colonnes ID
            row['idAttribuant'] = clean_id(row.get('idAttribuant', ''))
            row['idBeneficiaire'] = clean_id(row.get('idBeneficiaire', ''))
            
            # Suppression des espaces autour de chaque valeur
            row = {k: v.strip() if v else "" for k, v in row.items()}
            
            writer.writerow(row)

print(f"Nettoyage terminé. Nouveau fichier créé : {output_file}")
