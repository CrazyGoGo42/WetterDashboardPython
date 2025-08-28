# Streamlit Dashboard für Wetterdaten
# Aufgabe: Dashboard mit Stadtauswahl, Temperaturdiagramm und Kennzahlen

import streamlit as st
import pandas as pd
import os

# Dashboard Titel
st.title("🌤️ Wetter Dashboard")

# CSV Datei laden
# Erstmal prüfen ob die Datei existiert
if not os.path.exists('wetter.csv'):
    st.error("Datei wetter.csv nicht gefunden!")
    st.info("Führe zuerst weather_data.py aus um die Wetterdaten zu laden.")
    st.stop()

# CSV einlesen
df = pd.read_csv('wetter.csv')

# Zeitpunkt wieder als Datum formatieren
df['Zeitpunkt'] = pd.to_datetime(df['Zeitpunkt'])

# Sidebar für Stadtauswahl
st.sidebar.header("Stadt auswählen")
selected_city = st.sidebar.selectbox("Wähle eine Stadt:", df['Stadt'].unique())

# Daten für gewählte Stadt filtern
city_data = df[df['Stadt'] == selected_city]

# Überschrift mit ausgewählter Stadt
st.header(f"Wetter in {selected_city}")

# Kennzahl: Durchschnittstemperatur der letzten 24 Stunden
# Einfache Lösung: nehme die letzten 24 Datenpunkte
last_24_hours = city_data.tail(24)
avg_temp_24h = last_24_hours['Temperatur'].mean()

# Kennzahl anzeigen
st.metric("Durchschnittstemperatur (letzte 24h)", f"{avg_temp_24h:.1f}°C")

# Temperaturverlauf als Liniendiagramm
st.subheader("📈 Temperaturverlauf")

# Daten für das Diagramm vorbereiten
chart_data = city_data.set_index('Zeitpunkt')['Temperatur']

# Liniendiagramm anzeigen
st.line_chart(chart_data)

# Tabelle mit allen Daten
st.subheader("Alle Wetterdaten")
st.dataframe(city_data)

# Bonus: CSV Download
st.sidebar.header("Daten exportieren")

# CSV Download Button
csv_data = city_data.to_csv(index=False)
st.sidebar.download_button(
    label="CSV herunterladen",
    data=csv_data,
    file_name=f'wetter_{selected_city}.csv',
    mime='text/csv'
)

# Info am Ende
st.info(f"Zeigt {len(city_data)} Datenpunkte für {selected_city}")