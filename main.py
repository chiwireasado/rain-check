from modulo_global import ModuloGlobal
from modulo_transporte import ModuloTransporte
from modulo_climatico import ModuloClimatico
from modulo_temporal import ModuloTemporal
import time


class RainCheck:
    def __init__(self):
        self.m_global = ModuloGlobal()
        self.m_transporte = ModuloTransporte()
        self.m_climatico = ModuloClimatico()
        self.m_temporal = ModuloTemporal()

    def mostrar_encabezado(self):
        print("\n" + "=" * 45)
        print("RAINCHECK MADRID - PANEL DE CONTROL ")
        print("=" * 45)

    def showMenu(self):
        while True:
            self.mostrar_encabezado()
            print("  [1] Módulo Global (Lluvia y Transporte)")
            print("  [2] Módulo de Transporte (Tiempos EMT)")
            print("  [3] Módulo Climático (Análisis 24h y CSV)")
            print("  [4] Módulo Temporal (Consulta por Fecha)")
            print("  [5] Salir del Sistema")
            print("-" * 45)

            choice = input("Selecciona una opción (1-5): ").strip()

            if choice == '1':
                print("\n[Iniciando Módulo Global...]")
                self.m_global.ejecutar()
            elif choice == '2':
                self.m_transporte.ejecutar()
            elif choice == '3':
                self.m_climatico.ejecutar()
            elif choice == '4':
                self.m_temporal.ejecutar()
            elif choice == '5':
                print("Gracias por usar RainCheck. \n")
                time.sleep(1)
                exit()
            else:
                print("Opción no válida. Por favor, introduce un número del 1 al 5.\n")
                time.sleep(1)


if __name__ == "__main__":
    app = RainCheck()
    app.showMenu()