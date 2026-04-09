---
name: leaflet-csv-mapper
description: Crée des cartes interactives Leaflet à partir de fichiers CSV (Latitude/Longitude). Utilise PapaParse pour le parsing des données et propose des fonds satellites (Esri) ou plans (OSM) avec intégration de limites administratives GeoJSON.
---

# Leaflet CSV Mapper

## Workflow

1. **Analyse du CSV** : Identifier le délimiteur (`,` ou `;`) et les noms de colonnes pour la localisation (ex: `latitude`, `longitude`, `geo_point`).
2. **Choix du Fond de Carte** :
   - `Satellite` : Esri World Imagery (précision visuelle).
   - `Plan` : OpenStreetMap ou CartoDB Light (lisibilité).
3. **Configuration Leaflet** :
   - Initialiser `L.map`.
   - Charger le CSV via `Papa.parse`.
   - Créer des `L.circleMarker` pour une meilleure performance et visibilité.
4. **Délimitations (Optionnel)** : Charger un fichier GeoJSON (communes, départements) pour ajouter un contexte territorial.

## Modèle de code (Boilerplate)

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>#map { height: 100vh; }</style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([44.84, -0.58], 11);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}').addTo(map);

        Papa.parse("donnees.csv", {
            download: true, header: true, skipEmptyLines: true,
            complete: function(results) {
                results.data.forEach(row => {
                    const lat = parseFloat(String(row.latitude).replace(',', '.'));
                    const lng = parseFloat(String(row.longitude).replace(',', '.'));
                    if (!isNaN(lat) && !isNaN(lng)) {
                        L.circleMarker([lat, lng], { radius: 6, fillColor: "yellow", color: "#000", fillOpacity: 0.9 }).addTo(map)
                         .bindPopup(`<b>${row.nom}</b>`);
                    }
                });
            }
        });
    </script>
</body>
</html>
```

## Astuces de débogage
- **Points absents** : Vérifier si `parseFloat` échoue à cause d'une virgule (utiliser `.replace(',', '.')`).
- **CORS** : Si le GeoJSON est sur un autre domaine, s'assurer que le serveur autorise les requêtes ou utiliser une source brute (GitHub Raw).
- **GitHub Pages** : Ajouter un cache-breaker `?v=` à l'URL du CSV pour forcer la mise à jour des données.
