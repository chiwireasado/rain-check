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
        headers = {"X-ClientId": self.client_id, "passKey": self.api_key}
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                return res.json()['data'][0]['accessToken']
            return None
        except:
            return None

    def ejecutar(self):
        print(" >>> MODULO TRANSPORTE <<<")

        parada = input("Introduce el numero de parada (Nº Parada -> ej: 1234): ").strip()

        token = self.obtener_token()

        if not token:
            print("Acceso denegado. Tu cuenta EMT aún no está activa.")
            return


        url_emt = f"https://openapi.emtmadrid.es/v2/transport/busemtmad/stops/{parada}/arriving/"
        credenciales = {"accessToken": token}

        payload = {"statistics": "N", "cultureInfo": "ES"}

        try:
            print(f"Buscando informacion de parada: {parada}...")
            response = requests.post(url_emt, headers=credenciales, json=payload).json()

            if 'data' in response and response['data']:
                llegadas = response['data'][0].get('Arrive', [])

                if llegadas:
                    print(f"\nINFORMACIÓN ACTUALIZADA (Punto {parada}):")
                    print(f"{'LÍNEA':<8} | {'TIEMPO ESPERA':<15} | {'DISTANCIA'}")


                    lista_para_excel = []


                    llegadas_ordenadas = sorted(llegadas, key=lambda x: x['estimateArrive'])

                    for bus in llegadas_ordenadas:
                        linea = bus['line']
                        segundos = bus['estimateArrive']
                        minutos = segundos // 60
                        distancia = bus['DistanceBus']

                        tiempo_texto = f"{minutos} min" if minutos > 0 else "Llegando..."

                        print(f"{linea:<8} | {tiempo_texto:<15} | {distancia} metros")

                        lista_para_excel.append({
                            "PUNTO EXACTO": parada,
                            "LINEA": linea,
                            "ESTADO": tiempo_texto,
                            "DISTANCIA (m)": distancia
                        })


                    exportarALpreguntar = input("\n¿Deseas guardar este reporte de tiempo real en Excel? (si/no): ").lower().strip()

                    if exportarALpreguntar == "si":
                        self.exportar_transporte_pro(lista_para_excel)
                else:
                    print("No hay informacion de buses aproximándose a esta parada")
            else:
                print("La parada no existe o no tiene servicio.")

        except Exception as i:
            print(f"❌ Error en la consulta de tiempo real. -> {i}")

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