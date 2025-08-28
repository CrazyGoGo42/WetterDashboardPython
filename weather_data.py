# Wetterdaten von Open-Meteo API abrufen
# Aufgabe: Daten für 3 Städte holen und als CSV speichern

import requests
import pandas as pd

# Koordinaten für die Städte (aus Google Maps kopiert)
cities = [
    {'name': 'Berlin', 'lat': 52.52, 'lon': 13.41},
    {'name': 'Paris', 'lat': 48.85, 'lon': 2.35},
    {'name': 'New York', 'lat': 40.71, 'lon': -74.01}
]

# Leere Liste für alle Wetterdaten
weather_data = []

print("Lade Wetterdaten...")

# Für jede Stadt Daten abrufen
for city in cities:
    print(f"Hole Daten für {city['name']}...")
    
    # API URL zusammenbauen
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    
    # API aufrufen
    response = requests.get(url)
    data = response.json()
    
    # Daten extrahieren
    times = data['hourly']['time']
    temperatures = data['hourly']['temperature_2m']
    humidity = data['hourly']['relativehumidity_2m']
    wind_speeds = data['hourly']['windspeed_10m']
    
    # Daten in Liste speichern
    for i in range(len(times)):
        weather_data.append({
            'Stadt': city['name'],
            'Zeitpunkt': times[i],
            'Temperatur': temperatures[i],
            'Luftfeuchtigkeit': humidity[i],
            'Wind': wind_speeds[i]
        })

# DataFrame erstellen
df = pd.DataFrame(weather_data)

# Zeitpunkt als Datum formatieren
df['Zeitpunkt'] = pd.to_datetime(df['Zeitpunkt'])

# Als CSV speichern
df.to_csv('wetter.csv', index=False)

print(f"{len(df)} Datensätze in wetter.csv gespeichert")
print("Erste paar Zeilen:")
print(df.head())