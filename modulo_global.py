import pandas as po
from openpyxl.styles import Font, PatternFill, Alignment
import requests
import os

class ModuloGlobal:
    def __init__(self):
        self.lat_madrid = 40.4168
        self.lon_madrid = -3.7038
        self.client_id = "4300df6f-d6a6-4638-8973-ad05b55fb1bd"
        self.api_key = "259AD0A95B3AE7FEBF12A549AAC3CC9E9336A645AADB81B493BC4610191A1CA88F79E6DD7B68D49824084C21BAB8CB1B5D33FF0D324D6CE2125BCC82398F6FDA"


    def token(self):
        url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"
        credenciales = {"X-ClientId": self.client_id, "passKey": self.api_key}
        try:
            response = requests.get(url, headers=credenciales)

            if response.status_code != 200:
                print(f"Error de la EMT ({response.status_code}): {response.text}")
                return None

            return response.json()['data'][0]['accessToken']
        except Exception as a:
            print(f"Error de conexión. -> {a}")
            return None


    def ejecutar(self):
        print("\n >>> MÓDULO GLOBAL <<<")
        hora = input("1. Introduce la hora para el clima (00 a 23): ").strip()
        parada = input("2. Introduce el número de parada de bus: ").strip()

        url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat_madrid}&longitude={self.lon_madrid}&hourly=precipitation&timezone=Europe%2FMadrid&forecast_days=1"

        lluvia_contador = 0

        try:
            clima = requests.get(url_clima).json()
            tiempos = clima['hourly']['time']
            lluvias = clima['hourly']['precipitation']

            look = f"T{hora.zfill(2)}:00"
            for i in range(len(tiempos)):
                if look in tiempos[i]:
                    lluvia_contador = lluvias[i]
                    break
        except Exception as b:
            print(f"Error al obtener datos del clima. -> {b}")


        tiempos_bus = []
        tk = self.token()

        if tk:
            url_emt = f"https://openapi.emtmadrid.es/v2/transport/busemtmad/stops/{parada}/arriving/"
            credenciales_emt = {"accessToken": tk}
            payload = {"statistics": "N", "cultureInfo": "ES"}

            try:
                res_emt = requests.post(url_emt, headers=credenciales_emt, json=payload).json()

                if 'data' in res_emt and res_emt['data'] and 'Arrive' in res_emt['data'][0]:
                    llegadas = res_emt['data'][0]['Arrive']
                    for bus in llegadas:
                        tiempos_bus.append({
                            "linea": bus['line'],
                            "minutos de espera": bus['estimateArrive'] // 60
                        })
                else:
                    print("Error de autenticación en EMT. El reporte de buses estará vacío.")
            except Exception as c:
                print(f"Error al procesar buses de la EMT. -> {c}")



        print(f">>>> RESULTADOS DE RAINCHECK >>>")

        print(f"LLuvia prevista ({hora}:00): {lluvia_contador}mm")

        if lluvia_contador > 0:
            print("Estado: Se recomienda llevar paraguas 🌧️, hay alerta de lluvia, feliz dia")
        else:
            print("Estado: Puedes guardar el paraguas ☀️, feliz día")

        print(f"Buses en parada: {parada}")
        if tiempos_bus:
            for bus in tiempos_bus:
                print(f" > Linea {bus['linea']}: llegada en {bus['minutos de espera']} min")
        else:
            print("No hay informacion de busese")


        if lluvia_contador is not None:
            preguntarALexportar = input("\n¿Quieres ver tus estadisticas en excel? (si/no): ").strip()

            if preguntarALexportar == "si":
                self.exportar_a_excel(hora, lluvia_contador, parada, tiempos_bus)

            else:
                print("Genial, volviendo al menu principal...")
                print("recuerda, si no tienes otra peticion, escoger la opcion 5 para salir de RainCheck :)")



    def exportar_a_excel(self, hora, lluvia, parada, lista_buses):
        nombre_fichero = "estadisticas_raincheck.xlsx"

        datos_nuevos = []
        if not lista_buses:
            datos_nuevos.append({
                "HORA": f"{hora}:00",
                "LLUVIA": f"{lluvia}mm",
                "PARADA": parada,
                "LINEA": "Sin datos EMT",
                "ESPERA": "N/A"
            })
        else:
            for b in lista_buses:
                datos_nuevos.append({
                    "HORA": f"{hora}:00",
                    "LLUVIA": f"{lluvia}mm",
                    "PARADA": parada,
                    "LINEA": b['linea'],
                    "ESPERA": f"{b['minutos de espera']} min"
                })


        df_nuevo = po.DataFrame(datos_nuevos)


        if os.path.exists(nombre_fichero):
            df_antiguo = po.read_excel(nombre_fichero)
            df_final = po.concat([df_antiguo, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo


        try:
            with po.ExcelWriter(nombre_fichero, engine='openpyxl') as escritor:
                df_final.to_excel(escritor, index=False, sheet_name='Reporte')


                sheet = escritor.sheets['Reporte']

                back_ground = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
                letra = Font(color="FFFFFF", bold=True, size=12)
                center = Alignment(horizontal="center")

                for cell in sheet[1]:
                    cell.fill = back_ground
                    cell.font = letra
                    cell.alignment = center

                for column in sheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            print("Error al dibujar")
                    sheet.column_dimensions[column_letter].width = max_length + 4


            print(f"\n✅ Datos exportados!! el documento esta en '{nombre_fichero}'")
        except Exception as d:
            print(f"\n❌ Error al crear el Excel. -> {d}")