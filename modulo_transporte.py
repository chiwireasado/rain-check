import requests

class ModuloTransporte:
        def __init__(self):
            self.client_id = "chiwireasado"
            self.api_key = "Mjjlmp123*"
            self.base_url = "https://openapi.emtmadrid.es/v2/transport/busemtmad/stops"

        def login(self):
            url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"
            headers = {"X-ClientId": self.client_id, "passKey": self.api_key}
            try:
                response = requests.get(url, headers=headers)
                return response.json()['data'][0]['accessToken']
            except:
                return None


        def ejecutar(self):
            print("\n--- [MÓDULO TRANSPORTE EN TIEMPO REAL] ---")
            stop_id = input("Introduce el número de la parada (ej: 7265): ")

            token = self.login()
            if not token:
                print("Error: No se pudo autenticar con la EMT.")
                return

            url = f"{self.base_url}/{stop_id}/arriving/"
            headers = {"accessToken": token}


            payload = {"statistics": "N", "cultureInfo": "ES"}

            try:
                response = requests.post(url, headers=headers, json=payload)
                data = response.json()

                print(f"\nPróximos autobuses en parada {stop_id}:")
                arrivals = data['data'][0]['Arrive']

                for bus in arrivals:
                    linea = bus['line']
                    tiempo = bus['estimateArrive'] // 60
                    distancia = bus['DistanceBus']
                    print(f"Línea {linea}: {tiempo} min aprox. (a {distancia} metros)")

            except Exception as e:
                print(f"Error al conectar con EMT: {e}")