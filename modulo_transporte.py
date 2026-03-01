import requests

class ModuloTransporte:
        def __init__(self):
            self.client_id = "chiwireasado"
            self.api_key = "Mjjlmp123*"


        def login(self):
            url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"
            credenciales = {"X-ClientId": self.client_id, "passKey": self.api_key}
            try:
                response = requests.get(url, headers=credenciales)
                return response.json()['data'][0]['accessToken']
            except:
                print("No se pudo conectar con la EMT")
                return None


        def ejecutar(self):
            print("\n>>>> [MÓDULO TRANSPORTE EN TIEMPO REAL <<<<")
            stop_id = input("Introduce el número de parada exacto")

            tk = self.token()

            if not tk:
                print("Error: No se pudo autenticar con la EMT.")
                return

            url = f"{self.base_url}/{stop_id}/arriving/"
            headers = {"accessToken": tk}


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