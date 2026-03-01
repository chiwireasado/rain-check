import requests
import pandas as pd


class ModuloTemporal:
    def __init__(self):
        self.lat = 40.4168
        self.lon = -3.7038  #Las coordenadas de Madrid

    def ejecutar(self):
        print(45 * "=" + "\n")
        print("[MÓDULO TEMPORAL: CLIMA POR FECHA EXACTA]")
        print("=" * 45)

        # Explicación del formato al usuario para evitar bloqueos
        print("Recuerda: El formato de la fecha debe ser AÑO-MES-DÍA (ej: 2026-02-28)")
        fecha = input("Introduce la fecha deseada: ").strip()
        hora_usuario = input("Introduce la hora en formato militar (00 a 23): ").strip()

        url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
               f"&hourly=precipitation&timezone=Europe%2FMadrid"
               f"&start_date={fecha}&end_date={fecha}")

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                tiempos = data['hourly']['time']
                lluvias = data['hourly']['precipitation']

                # Formateamos la búsqueda para que coincida con el JSON de la API
                busqueda = f"T{hora_usuario.zfill(2)}:00"

                datos_encontrados = []
                for i in range(len(tiempos)):
                    if busqueda in tiempos[i]:
                        datos_encontrados.append({
                            'Fecha y Hora': tiempos[i],
                            'Precipitación (mm)': lluvias[i]
                        })
                        break

                if datos_encontrados:
                    #Procesado con pandas
                    df = pd.DataFrame(datos_encontrados)
                    print( 45 * "-" + "\n")
                    print("RESULTADO DE LA BÚSQUEDA")
                    print("-" * 45)
                    print(df.to_string(index=False))

                    # EXPORTACIÓN A CSV
                    exportar = input("¿Crear csv (Excel)? (S/N):\n").strip().upper()
                    if exportar == 'S':
                        nombre_archivo = f'clima_{fecha}_H{hora_usuario.zfill(2)}.csv'
                        df.to_csv(nombre_archivo, index=False, sep=';', encoding='utf-8')
                        print(f"¡Archivo '{nombre_archivo}' generado con éxito!")
                else:
                    print(f"No se encontraron datos para la hora {hora_usuario}:00 en la fecha {fecha}.\n")
            else:
                print("Error al obtener datos de la API. Revisa que el formato de fecha sea correcto.\n")

        except Exception as e:
            print(f"Ocurrió un error de conexión: {e}\n")