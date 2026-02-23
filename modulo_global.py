import requests
import pandas as pd

def get_rain_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation&timezone=Europe%2FMadrid"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()


       #lo pone bonito
        df = pd.DataFrame({
            'Tiempo': data['hourly']['time'],
            'Precipitación (mm)': data['hourly']['precipitation']
        })
        return df
    return None