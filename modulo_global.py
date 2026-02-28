import requests
class ModuloGlobal:
    def __init__(self):
        self.lat_madrid = 40.4168
        self.lon_madrid = -3.7038

        self.client_id = "chiwireasado"
        self.api_key = "Mjjlmp123*"


    def token(self):
        url = "https://openapi.emtmadrid.es/v2/mobilitylabs/user/login/"
        credenciales = {"X-ClientId": self.client_id, "passKey": self.api_key}
        try:
            response = requests.get(url, headers=credenciales)
            return response.json()['data'][0]['accessToken']
        except:
            print("no se pudo establecer la conexion")
            return None


    def ejecutar(self):
        print("\n >>> MÓDULO GLOBAL <<<")
        hora = input("1. Introduce la hora para el clima (00 a 23): ")
        parada = input("2. Introduce el número de parada para transporte: ")

        url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat_madrid}&longitude={self.lon_madrid}&hourly=precipitation&timezone=Europe%2FMadrid&forecast_days=1"

        try:
            clima = requests.get(url_clima).json()
            tiempos = clima['hourly']['time']
            lluvias = clima['hourly']['precipitation']

            look = f"T{hora.zfill(2)}:00"
            lluvia_contador = 0

            for i in range(len(tiempos)):
                if look in tiempos[i]:
                    lluvia_contador = lluvias[i]
                    break

            tk = self.token()
            tiempos_bus = []

            if tk:
                url_emt = f"https://openapi.emtmadrid.es/v2/transport/busemtmad/stops/{parada}/arriving/"
                credenciales_emt = {"accessToken": tk}
                payload = {"statistics": "N", "cultureInfo": "ES"}

                res_emt = requests.post(url_emt, headers=credenciales_emt, json=payload).json()
                llegadas = res_emt['data'][0]['Arrive']


                for bus in llegadas:
                    tiempos_bus.append({
                        "linea": bus['line'],
                        "minutos de espera": bus['estimateArrive'] // 60
                    })
            else:
                print("Error de autenticación en EMT")


            print(f"LLuvia prevista ({hora}:00): {lluvia_contador}mm")
            if lluvia_contador > 0:
                print("Estado: Se recomienda llevar paraguas, hay alerta de lluvia, feliz dia")
            else:
                print("Estado: Sin lluvia. guarda el paraguas, feliz día")

            print(f"Autobus en parada: {parada}")
            if tiempos_bus:
                for bus in tiempos_bus:
                    print(f" > Linea {bus['linea']}: llegada en {bus['minutos']} min")
            else:
                print("No hay informacion de bus")

        except Exception as a:
            print(f"error en el modulo global. Error:{a}")


