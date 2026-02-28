import requests
import pandas as pd


class ModuloGlobal:
    def __init__(self):
        # estas son las coordenadas de Madrid
        self.lat_madrid = 40.4168
        self.lon_madrid = -3.7038
        self.base_url_emt = "https://openapi.emtmadrid.es/v2/transport/busemtmad/stops"

    def login_emt(self, client_id, api_key):
        """Autenticación dinámica para que no nos baneen la cuenta."""
        url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"
        headers = {"X-ClientId": client_id, "passKey": api_key}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()['data'][0]['accessToken']
        except Exception:
            return None
        return None

    def ejecutar(self):
        print( 45 * "=" + "\n")
        print("[MÓDULO GLOBAL: LLUVIA Y TRANSPORTE]")
        print("=" * 45)

        #Inputs del usuario (los rombos que hicimos en el diagrama)
        stop_id = input("Introduce el ID de la parada (ej: 7265): ").strip()
        hora_deseada = input("Introduce la hora deseada (00-23): ").strip()

        #las credenciales EMT
        print("[Autenticación EMT Requerida]\n")
        client_id = input("Introduce tu ClientId: ").strip()
        api_key = input("Introduce tu passKey: ").strip()

        token = self.login_emt(client_id, api_key)
        if not token:
            print("Error de autenticación con la EMT\n")
            return

        #LLamamos a la API del Clima
        print("Consultando previsiones meteorológicas...\n")
        url_clima = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat_madrid}"
                     f"&longitude={self.lon_madrid}&hourly=precipitation&timezone=Europe%2FMadrid")

        lluvia_detectada = "0.0"
        try:
            res_clima = requests.get(url_clima)
            if res_clima.status_code == 200:
                data_clima = res_clima.json()
                tiempos = data_clima['hourly']['time']
                lluvias = data_clima['hourly']['precipitation']

                # Buscamos la hora exacta que pidió el usuario
                busqueda = f"T{hora_deseada.zfill(2)}:00"
                for i in range(len(tiempos)):
                    if busqueda in tiempos[i]:
                        lluvia_detectada = lluvias[i]
                        break
        except Exception as e:
            print(f"Error al obtener el clima: {e}")

        #Llamamos a la API de Transporte
        print("⏳ Consultando tiempos de espera en la parada...")
        url_transporte = f"{self.base_url_emt}/{stop_id}/arriving/"
        headers = {"accessToken": token}
        payload = {"statistics": "N", "cultureInfo": "ES"}

        datos_procesados = []
        try:
            res_trans = requests.post(url_transporte, headers=headers, json=payload)
            if res_trans.status_code == 200:
                data_trans = res_trans.json()
                arrivals = data_trans['data'][0]['Arrive']

                # Mapeo de datos para Pandas
                for bus in arrivals:
                    datos_procesados.append({
                        'Parada': stop_id,
                        'Línea': bus['line'],
                        'Espera (minutos)': bus['estimateArrive'] // 60,
                        'Distancia (metros)': bus['DistanceBus'],
                        f'Lluvia a las {hora_deseada}:00 (mm)': lluvia_detectada
                    })
        except Exception as e:
            print(f"Error al conectar con EMT: {e}")

        #Muestra los resultados y exporta el CSV
        if not datos_procesados:
            print("No hay datos de autobuses para esa parada en este momento.\n")
            return

        #Creamos el DataFrame
        df = pd.DataFrame(datos_procesados)
        print(45 * "-" + "\n")
        print("RESULTADOS CRUZADOS")
        print("-" * 45)
        print(df.to_string(index=False))

        #Pregunta de exportación según el diagrama de flujo
        exportar = input("¿Crear csv (Excel)? (S/N): ").strip().upper()
        if exportar == 'S':
            nombre_archivo = f'analisis_global_parada_{stop_id}.csv'
            df.to_csv(nombre_archivo, index=False, sep=';', encoding='utf-8')
            print(f"¡Archivo '{nombre_archivo}' generado, listo para ver en Excel.")