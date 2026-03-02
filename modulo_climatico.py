import requests
import pandas as po
import os
from openpyxl.styles import Font, PatternFill, Alignment


class ModuloClimatico:
    def __init__(self):
        self.lat = 40.4168
        self.lon = -3.7038

    def ejecutar(self):
        print(" >>> MÓDULO CLIMÁTICO <<<")


        hora_usuario = input("Introduce la hora a consultar (00 a 23): ").strip()


        url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
               f"&hourly=temperature_2m,precipitation,uv_index&timezone=Europe%2FMadrid&forecast_days=1")

        try:
            response = requests.get(url).json()
            horas = response['hourly']['time']
            temps = response['hourly']['temperature_2m']
            lluvias = response['hourly']['precipitation']
            uv_indices = response['hourly']['uv_index']


            formato_hora = f"T{hora_usuario.zfill(2)}:00"
            encontrado = False

            for i in range(len(horas)):
                if formato_hora in horas[i]:
                    temp = temps[i]
                    lluvia = lluvias[i]
                    uv = uv_indices[i]
                    encontrado = True
                    break

            if encontrado:
                print(f"\nReporte para las {hora_usuario}:00 en Madrid")

                print(f"Temperatura: {temp}°C")
                print(f"Lluvia: {lluvia} mm")
                print(f"Índice UV: {uv}uv")


                if uv <= 2:
                    msg_uv = "Bajo (Seguro, pero igual usa crema solar :) )"
                elif uv <= 5:
                    msg_uv = "Moderado (Usa crema solar)"
                else:
                    msg_uv = "Alto (Evita el sol, y ponte mucha crema solar)"
                print(f" Consejo girlie: Nivel UV {msg_uv}")


                opcion = input("\n¿Quieres ver tus estadisticas en excel? (si/no): ").lower().strip()
                if opcion == "si":
                    self.exportar_excel_clima(hora_usuario, temp, lluvia, uv)
            else:
                print("❌ No se encontró información para esa hora")

        except Exception as e:
            print(f"❌ Error al conectar con el servicio meteorológico. -> {e}")

    def exportar_excel_clima(self, hora, temp, lluvia, uv):
        nombre_fichero = "reporte_climatico_detallado.xlsx"

        datos_nuevos = po.DataFrame([{
            "HORA": f"{hora}:00",
            "TEMPERATURA (°C)": f"{temp}°C",
            "LLUVIA (mm)": f"{lluvia}mm",
            "INDICE UV": uv
        }])

        if os.path.exists(nombre_fichero):
            df_final = po.concat([po.read_excel(nombre_fichero), datos_nuevos], ignore_index=True)
        else:
            df_final = datos_nuevos

        try:
            with po.ExcelWriter(nombre_fichero, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Clima_Detalle')
                sheet = writer.sheets['Clima_Detalle']

                back_ground = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
                letra = Font(color="FFFFFF", bold=True)

                for cell in sheet[1]:
                    cell.fill = back_ground
                    cell.font = letra
                    cell.alignment = Alignment(horizontal="center")


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

            print(f"✅ Archivo '{nombre_fichero}' actualizado correctamente.")

        except Exception as a:
            print(f"❌ No se pudo guardar el Excel. -> {a}")