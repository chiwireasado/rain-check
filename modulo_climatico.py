import requests
import pandas as pd


class ModuloClimatico:
    def __init__(self):
        # Coordenadas de Madrid
        self.lat = 40.4168
        self.lon = -3.7038

    def ejecutar(self):
        print("\n--- [MÓDULO CLIMÁTICO: LLUVIA EN 24 HORAS] ---")

        # Llamada a la API de Open-Meteo para las últimas/próximas 24h
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
               f"&hourly=precipitation&past_days=1&forecast_days=1&timezone=Europe%2FMadrid")

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # Extraemos solo los primeros 24 registros (24 horas)
                tiempos = data['hourly']['time'][:24]
                lluvias = data['hourly']['precipitation'][:24]

                # PROCESADO CON PANDAS
                # Creamos un DataFrame (una tabla estructurada)
                df = pd.DataFrame({
                    'Fecha y Hora': tiempos,
                    'Precipitación (mm)': lluvias
                })

                # Mostramos los datos por pantalla
                print(df.to_string(index=False))

                # EXPORTACIÓN A CSV (Rombo de decisión en tu diagrama)
                exportar = input("\n¿Crear csv (Excel)? (S/N): ").strip().upper()
                if exportar == 'S':
                    # Pandas exporta a CSV automáticamente
                    df.to_csv('lluvia_24h_madrid.csv', index=False, sep=';', encoding='utf-8')
                    print("--> ¡Archivo 'lluvia_24h_madrid.csv' generado con éxito!")
            else:
                print("Error al consultar la API del clima.")

        except Exception as e:
            print(f"Se produjo un error de conexión: {e}")