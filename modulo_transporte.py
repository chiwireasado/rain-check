import requests


class ModuloTransporte:
    def __init__(self):
        self.base_url = "https://openapi.emtmadrid.es/v2/transport/busemtmad/stops"
        self.client_id = None
        self.api_key = None

    def pedir_credenciales(self):
        print("\n--- [AUTENTICACIÓN EMT MADRID] ---")
        print("Para evitar bloqueos, por favor usa tus credenciales de MobilityLabs.")
        self.client_id = input("Introduce tu ClientId: ").strip()
        self.api_key = input("Introduce tu passKey: ").strip()

    def login(self):
        if not self.client_id or not self.api_key:
            self.pedir_credenciales()

        url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"
        headers = {"X-ClientId": self.client_id, "passKey": self.api_key}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()['data'][0]['accessToken']
            else:
                return None
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

    def ejecutar(self):
        print("\n--- [MÓDULO TRANSPORTE EN TIEMPO REAL] ---")
        stop_id = input("Introduce el número de la parada (ej: 7265): ")

        token = self.login()
        if not token:
            print("Error: No se pudo autenticar con la EMT. Revisa tus credenciales.")
            # Reseteamos las credenciales para que las vuelva a pedir en el siguiente intento
            self.client_id = None
            self.api_key = None
            return

        url = f"{self.base_url}/{stop_id}/arriving/"
        headers = {"accessToken": token}
        payload = {"statistics": "N", "cultureInfo": "ES"}

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"\nPróximos autobuses en parada {stop_id}:")
                arrivals = data['data'][0]['Arrive']

                if not arrivals:
                    print("No hay datos de autobuses próximos para esta parada.")
                    return

                for bus in arrivals:
                    linea = bus['line']
                    tiempo = bus['estimateArrive'] // 60
                    distancia = bus['DistanceBus']
                    print(f"Línea {linea}: {tiempo} min aprox. (a {distancia} metros)")
            else:
                print("Error al consultar la parada. Verifica el número.")

        except Exception as e:
            print(f"Error al conectar con EMT: {e}")