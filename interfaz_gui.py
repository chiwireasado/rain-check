import tkinter as tk
from tkinter import messagebox
import requests

class InterfazRainCheck:
    def __init__(self, root):
        self.root = root
        self.root.title("RainCheck Madrid - Interfaz Visual")
        self.root.geometry("450x500")
        self.root.configure(bg="#f0f0f0")

        # Credenciales y datos fijos
        self.lat = 40.4168
        self.lon = -3.7038
        self.client_id = "4300df6f-d6a6-4638-8973-ad05b55fb1bd"
        self.api_key = "259AD0A95B3AE7FEBF12A549AAC3CC9E9336A645AADB81B493BC4610191A1CA88F79E6DD7B68D49824084C21BAB8CB1B5D33FF0D324D6CE2125BCC82398F6FDA"

        # --- DISEÑO DE LA VENTANA ---
        tk.Label(root, text="🌧️ RAINCHECK MADRID 🚌", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # Campo para la hora
        tk.Label(root, text="Hora deseada (00-23):", bg="#f0f0f0").pack()
        self.entrada_hora = tk.Entry(root, justify="center")
        self.entrada_hora.pack(pady=5)

        # Campo para la parada
        tk.Label(root, text="Número de parada (Ej: 2539):", bg="#f0f0f0").pack()
        self.entrada_parada = tk.Entry(root, justify="center")
        self.entrada_parada.pack(pady=5)

        # Botón de búsqueda
        tk.Button(root, text="Consultar Datos", command=self.buscar_datos, bg="#002060", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

        # Caja de texto para mostrar los resultados
        self.caja_resultados = tk.Text(root, height=15, width=50, font=("Courier", 9))
        self.caja_resultados.pack(pady=10)

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

    def buscar_datos(self):
        hora = self.entrada_hora.get().strip()
        parada = self.entrada_parada.get().strip()

        # Limpiamos la caja de resultados antes de escribir
        self.caja_resultados.delete(1.0, tk.END)

        if not hora or not parada:
            messagebox.showwarning("Aviso", "Por favor, rellena la hora y la parada.")
            return

        self.caja_resultados.insert(tk.END, f"Buscando datos cruzados...\n{'-'*40}\n")
        self.root.update() # Forzamos a que la ventana se actualice visualmente

        # 1. Buscar Clima
        lluvia = "0.0"
        try:
            url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=precipitation&timezone=Europe%2FMadrid&forecast_days=1"
            clima = requests.get(url_clima).json()
            look = f"T{hora.zfill(2)}:00"
            for i in range(len(clima['hourly']['time'])):
                if look in clima['hourly']['time'][i]:
                    lluvia = clima['hourly']['precipitation'][i]
                    break
            self.caja_resultados.insert(tk.END, f"🌧️ Lluvia a las {hora}:00 -> {lluvia} mm\n")
        except:
            self.caja_resultados.insert(tk.END, "⚠️ Error al consultar el clima.\n")

        # 2. Buscar Autobuses
        token = self.obtener_token()
        if token:
            url_emt = f"https://openapi.emtmadrid.es/v2/transport/busemtmad/stops/{parada}/arriving/"
            try:
                # Usamos la versión a prueba de fallos que arreglamos antes
                peticion = requests.post(url_emt, headers={"accessToken": token}, json={"statistics": "N", "cultureInfo": "ES"})
                if peticion.status_code == 200:
                    datos = peticion.json()
                    if 'data' in datos and datos['data'] and 'Arrive' in datos['data'][0]:
                        self.caja_resultados.insert(tk.END, f"\n🚌 Autobuses en parada {parada}:\n")
                        for bus in datos['data'][0]['Arrive']:
                            minutos = bus['estimateArrive'] // 60
                            self.caja_resultados.insert(tk.END, f"   Línea {bus['line']:<4} -> {minutos} min\n")
                    else:
                        self.caja_resultados.insert(tk.END, "\n🚌 No hay autobuses en camino.\n")
                else:
                    self.caja_resultados.insert(tk.END, "\n⚠️ La EMT no devuelve datos válidos ahora mismo.\n")
            except:
                self.caja_resultados.insert(tk.END, "\n⚠️ Error de conexión con la EMT.\n")
        else:
            self.caja_resultados.insert(tk.END, "\n⚠️ Error de credenciales EMT (Cuenta inactiva).\n")

# Motor de arranque de la interfaz
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = InterfazRainCheck(ventana_principal)
    ventana_principal.mainloop()