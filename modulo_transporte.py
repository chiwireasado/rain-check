import requests
import pandas as po
import os
from openpyxl.styles import Font, PatternFill, Alignment


class ModuloTransporte:
    def __init__(self):
        self.client_id = "4300df6f-d6a6-4638-8973-ad05b55fb1bd"
        self.api_key = "259AD0A95B3AE7FEBF12A549AAC3CC9E9336A645AADB81B493BC4610191A1CA88F79E6DD7B68D49824084C21BAB8CB1B5D33FF0D324D6CE2125BCC82398F6FDA"

    def obtener_token(self):
        url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"

        credenciales = {
            "X-ClientId": self.client_id,
            "passKey": self.api_key
        }
        try:
            res = requests.get(url, headers=credenciales)
            if res.status_code == 200:
                return res.json()['data'][0]['accessToken']
            else:
                print("error del token")
        except:
            print("error de red")
            return None

    def ejecutar(self):
        print(" >>> MODULO TRANSPORTE <<<")
        parada = input("Introduce el numero de parada (Nº Parada -> ej: 1234): ").strip()

        token = self.obtener_token()
        if not token:
            print("Acceso denegado. Tu cuenta EMT aún no está activa")
            return

        url_emt = f"https://openapi.emtmadrid.es/v3/transport/busemtmad/stops/{parada}/arrives/"

        credenciales = {
            "accessToken": token,
            "Content-Type": "application/json",
        }

        payload = {
            "cultureInfo": "ES",
            "Text_StopRequired_YN": "Y",
            "Text_EstimationsRequired_YN": "Y",
            "Text_IncidencesRequired_YN": "N"
        }

        print(f"Buscando informacion de parada: {parada}...")

        try:
            response = requests.post(url_emt, headers=credenciales, json=payload)

            if response.status_code != 200:
                print(f"Codigo de estado: {response.status_code}")
                print(f"error del servidor. CODIGO -> {response.status_code}")
                print({response.text[:200]})
                return


            res_emt = response.json()

            llegadas = []
            if 'data' in res_emt and len(res_emt['data']) > 0:
                datos = res_emt['data'][0]

                for clave in  ['Arrives', 'Arrive', 'arrives']:
                    if clave in datos:
                        llegadas = datos[clave]
                        break

                if llegadas:
                    print(f"\n>>> Parada: {parada} <<<")
                    print(f"{'LÍNEA': <8} | {'TIEMPO ESPERA':<15} | {'DISTANCIA'}")

                lista_para_excel = []
                llegadas_ordenadas = sorted(llegadas, key=lambda x: x.get('estimateArrive', 0))

                for bus in llegadas_ordenadas:
                    linea = bus.get('line')
                    segundos = bus.get('estimateArrive', 0)
                    minutos = segundos // 60
                    distancia = bus.get('DistanceBus')
                    tiempo_texto = f"{minutos} min" if minutos > 0 else "Llegando..."

                    print(f"{linea:<8} | {tiempo_texto:<15} | {distancia} metros")

                    lista_para_excel.append({
                        "PUNTO EXACTO": parada,
                        "LINEA": linea,
                        "ESTADO": tiempo_texto,
                        "DISTANCIA (m)": distancia
                    })

                exportarALpreguntar = input("\n¿Deseas guardar este reporte en Excel? (si/no): ").lower().strip()
                if exportarALpreguntar == "si":
                    self.exportar_transporte_pro(lista_para_excel)
            else:
                print("📭 No hay información de buses aproximándose a esta parada.")

        except Exception as i:
            print(f"❌ Se produjo un error -> {i} volviendo a menu....")


    def exportar_transporte_pro(self, datos):
        nombre = "reporte_tiempo_real_transporte.xlsx"

        df_nuevo = po.DataFrame(datos)

        if os.path.exists(nombre):
            df_final = po.concat([po.read_excel(nombre), df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo

        try:
            with po.ExcelWriter(nombre, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='TiempoReal')
                sheet = writer.sheets['TiempoReal']


                back_ground = PatternFill(start_color="006600", end_color="006600", fill_type="solid")
                letra = Font(color="FFFFFF", bold=True)

                for cell in sheet[1]:
                    cell.fill = back_ground
                    cell.font = letra
                    cell.alignment = Alignment(horizontal="center")


                for col in sheet.columns:
                    max_len = max(len(str(cell.value)) for cell in col)
                    sheet.column_dimensions[col[0].column_letter].width = max_len + 5

            print(f"✅ Historial de tiempo real actualizado en '{nombre}'")
        except Exception as g:
            print(f"❌ No se pudo actualizar el Excel: {g}")