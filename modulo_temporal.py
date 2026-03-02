import requests
import pandas as po
import os
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment


class ModuloTemporal:
    def __init__(self):
        self.lat = 40.4168
        self.lon = -3.7038

    def ejecutar(self):
        print(" >>> MÓDULO TEMPORAL: GRÁFICO DE LLUVIA (24H) <<<")


        url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
               f"&hourly=precipitation&timezone=Europe%2FMadrid&forecast_days=1")

        try:
            response = requests.get(url).json()
            horas_raw = response['hourly']['time']
            lluvias = response['hourly']['precipitation']


            horas_limpias = [h.split("T")[1] for h in horas_raw]


            df = po.DataFrame({
                "HORA": horas_limpias,
                "LLUVIA (mm)": lluvias
            })



            print("Generando reporte con gráfico...")


            self.exportar_con_grafico(df)

        except Exception as f:
            print(f"❌ Error al obtener datos temporales. -> {f}")

    def exportar_con_grafico(self, df):
        nombre_fichero = "analisis_lluvia_24h.xlsx"

        try:

            with po.ExcelWriter(nombre_fichero, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Lluvia_24h')
                workbook = writer.book
                sheet = writer.sheets['Lluvia_24h']


                color = PatternFill(start_color="CCECFF", end_color="CCECFF", fill_type="solid")
                letra = Font(bold=True)

                for cell in sheet[1]:
                    cell.fill = color
                    cell.font = letra
                    cell.alignment = Alignment(horizontal="center")


                chart = LineChart()
                chart.title = "Evolución de la Lluvia (Últimas 24h)"
                chart.style = 13
                chart.y_axis.title = 'Precipitación (mm)'
                chart.x_axis.title = 'Hora del día'


                data = Reference(sheet, min_col=2, min_row=1, max_row=25)

                cats = Reference(sheet, min_col=1, min_row=2, max_row=25)

                chart.add_data(data, titles_from_data=True)
                chart.set_categories(cats)


                s1 = chart.series[0]
                s1.graphicalProperties.line.solidFill = "00B0F0"


                sheet.add_chart(chart, "D2")


                sheet.column_dimensions['A'].width = 15
                sheet.column_dimensions['B'].width = 15

            print(f"✅ Datos exportados y grafico creado!! el documento esta en '{nombre_fichero}'")


        except Exception as h:
            print(f"❌ Error al crear el gráfico. -> {h}")