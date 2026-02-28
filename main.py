from modulo_global import ModuloGlobal
from modulo_transporte import ModuloTransporte
from modulo_geo import ModuloGeografico
from modulo_temporal import ModuloTemporal


class RainCheck:
    def __init__(self):
        self.m_global = ModuloGlobal()
        self.m_transporte = ModuloTransporte()
        self.m_geo = ModuloGeografico()
        self.m_temporal = ModuloTemporal()

        self.opciones = {
            '1': ('Modulo global', self.m_global.ejecutar),
            '2': ('Modulo transporte ', self.m_transporte.ejecutar),
            '3': ('Modulo geografico', self.m_geo.ejecutar),
            '4': ('Modulo temporal', self.m_temporal.ejecutar),
            '5': ('Salir', self.salir)
        }

    def showMenu(self):
        while True:
            print("<<<<<<<<< RAIN CHECK MADRID >>>>>>>>>>>>>")
            for o, (nombre, _) in self.opciones.items():
                print(f"{o} . {nombre}")

            choice = input("\n Selecciona una opcion: ")

            if choice in self.opciones:
                self.opciones[choice][1]()
            else:
                print("esa opcion no existe, escoge una de verdad")


    def salir(self):
        print("Gracias por usar RainCheck. ¡Cuidado con los charcos!")
        exit()


if __name__ == "__main__":
    app = RainCheck()
    app.showMenu()
