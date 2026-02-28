import requests
import pandas as po


class ModuloGlobal:
    def __init__(self):
        self.lat_madrid = 40.4168
        self.lon_madrid = -3.7038

    def get_rain_data(lat, lon):

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation&timezone=Europe%2FMadrid"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # esto es lo que arregla el formato
            datos = po.DataFrame({
                'Tiempo': data['hourly']['time'],
                'Precipitación (mm)': data['hourly']['precipitation']
            })
            return datos
        return None