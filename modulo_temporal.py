import requests

class ModuloTemporal:
        def __init__(self):
            self.lat = 40.4168
            self.lon = -3.7038 #estas son las de madrid

        def ejecutar(self):
            print("\n >>>> MODULO TEMPORAL: CONSULTA POR FECHA <<<")
            fecha = input("Introduce la fecha (Año-Mes-Dia): ")
            hora_usuario = input("Introduce la hora (00 a 23): ")

            url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
                   f"&hourly=precipitation&timezone=Europe%2FMadrid"
                   f"&start_date={fecha}&end_date={fecha}")

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()


                    tiempos = data['hourly']['time']
                    lluvias = data['hourly']['precipitation']

                    encontrado = False

                    busqueda = f"T{hora_usuario.zfill(2)}:00"

                    print(f"\nBuscando registros para la hora {hora_usuario}:00...")


                    for i in range(len(tiempos)):
                        now = tiempos[i]

                        if busqueda in now:
                            datoslluvia = lluvias[i]
                            print(f"¡Encontrado!")
                            print(f"Fecha y Hora: {now}")
                            print(f"Precipitación: {datoslluvia} mm")
                            encontrado = True
                            break

                    if not encontrado:
                        print(f"No se encontraron datos para la hora {hora_usuario}:00 en la fecha {fecha}.")

                else:
                    print("Error al obtener datos de la API. Revisa tus datos")

            except Exception as a:
                print(f"Ocurrió un error {a}")