# Regenerating the full code for the airline system using linked lists without comments after execution environment reset

class NodoPasajero:
    def __init__(self, pasajero):
        self.pasajero = pasajero
        self.siguiente = None

class NodoVuelo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.siguiente = None

class ListaEnlazadaPasajeros:
    def __init__(self):
        self.cabeza = None

    def agregar(self, pasajero):
        nuevo_nodo = NodoPasajero(pasajero)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def eliminar(self, nombre):
        actual = self.cabeza
        anterior = None
        while actual:
            if actual.pasajero.nombre == nombre:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                return actual.pasajero
            anterior = actual
            actual = actual.siguiente
        return None

    def buscar(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.pasajero.nombre == nombre:
                return actual.pasajero
            actual = actual.siguiente
        return None

    def recorrer(self):
        actual = self.cabeza
        while actual:
            yield actual.pasajero
            actual = actual.siguiente

class ListaEnlazadaVuelos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, vuelo):
        nuevo_nodo = NodoVuelo(vuelo)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener(self, indice):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == indice:
                return actual.vuelo
            actual = actual.siguiente
            contador += 1
        return None

    def recorrer(self):
        actual = self.cabeza
        while actual:
            yield actual.vuelo
            actual = actual.siguiente

class Pasajero:
    def __init__(self, nombre, edad, genero, clase, destino, valor_tiquete):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.clase = clase
        self.destino = destino
        self.valor_tiquete = valor_tiquete
        self.descuento = 0
        self.equipaje = 0
        self.cargas_especiales = []
        self.extra = 0
        if edad <= 13:
            self.descuento = valor_tiquete * 0.07
            self.valor_tiquete -= self.descuento

    def calcular_costo_equipaje(self):
        exceso = 0
        if self.clase == "economica":
            exceso = max(0, self.equipaje - 10)
            self.extra += exceso * 5000
        elif self.clase == "ejecutiva":
            exceso = max(0, self.equipaje - 20)
            self.extra += exceso * 10000
        elif self.clase == "premium":
            exceso = max(0, self.equipaje - 30)
            self.extra += exceso * (0.01 * self.valor_tiquete)

    def agregar_carga_especial(self, tipo, valor):
        if tipo == "bicicleta":
            self.extra += valor
        elif tipo == "perro":
            self.extra += self.valor_tiquete * 0.05
        elif tipo == "gato":
            self.extra += self.valor_tiquete * 0.02
        self.cargas_especiales.append(tipo)

class Vuelo:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
        self.pasajeros = ListaEnlazadaPasajeros()
        self.total_tiquetes = 0
        self.total_equipaje_extra = 0

    def agregar_pasajero(self, pasajero):
        self.pasajeros.agregar(pasajero)
        self.total_tiquetes += pasajero.valor_tiquete
        self.total_equipaje_extra += pasajero.extra

    def eliminar_pasajero(self, nombre):
        pasajero = self.pasajeros.eliminar(nombre)
        if pasajero:
            self.total_tiquetes -= pasajero.valor_tiquete
            self.total_equipaje_extra -= pasajero.extra

    def promedio_tiquete(self):
        count = 0
        suma = 0
        for p in self.pasajeros.recorrer():
            suma += p.valor_tiquete
            count += 1
        return suma / count if count > 0 else 0

class Aerolinea:
    def __init__(self):
        self.vuelos = ListaEnlazadaVuelos()

    def crear_vuelo(self):
        origen = input("Ingrese ciudad de origen: ")
        destino = input("Ingrese ciudad de destino: ")
        self.vuelos.agregar(Vuelo(origen, destino))
        print("Vuelo creado correctamente.")

    def mostrar_vuelos(self):
        for i, vuelo in enumerate(self.vuelos.recorrer()):
            print(f"{i + 1}. {vuelo.origen} -> {vuelo.destino}")

    def vender_tiquete(self):
        self.mostrar_vuelos()
        try:
            opcion = int(input("Seleccione el vuelo (número): ")) - 1
            vuelo = self.vuelos.obtener(opcion)
            nombre = input("Nombre del pasajero: ")
            edad = int(input("Edad: "))
            genero = input("Género (M/F): ").lower()
            clase = input("Clase (economica/ejecutiva/premium): ").lower()
            valor = float(input("Valor del tiquete: "))
            pasajero = Pasajero(nombre, edad, genero, clase, vuelo.destino, valor)
            vuelo.agregar_pasajero(pasajero)
            print("Tiquete vendido con éxito.")
        except:
            print("Error en los datos ingresados.")

    def hacer_checkin(self):
        self.mostrar_vuelos()
        try:
            opcion = int(input("Seleccione el vuelo (número): ")) - 1
            vuelo = self.vuelos.obtener(opcion)
            nombre = input("Ingrese nombre del pasajero: ")
            pasajero = vuelo.pasajeros.buscar(nombre)
            if pasajero:
                pasajero.equipaje = float(input("Peso del equipaje: "))
                pasajero.calcular_costo_equipaje()
                while True:
                    carga = input("¿Desea agregar carga especial? (bicicleta/perro/gato/no): ").lower()
                    if carga == "no":
                        break
                    elif carga == "bicicleta":
                        peso = float(input("Peso de la bicicleta: "))
                        pasajero.agregar_carga_especial("bicicleta", peso * 3000)
                    elif carga == "perro":
                        pasajero.agregar_carga_especial("perro", 0)
                    elif carga == "gato":
                        pasajero.agregar_carga_especial("gato", 0)
                print(f"Costo total adicional: {pasajero.extra}")
            else:
                print("Pasajero no encontrado.")
        except:
            print("Error durante el check-in.")

    def devolver_pasaje(self):
        self.mostrar_vuelos()
        try:
            opcion = int(input("Seleccione el vuelo (número): ")) - 1
            vuelo = self.vuelos.obtener(opcion)
            nombre = input("Nombre del pasajero a eliminar: ")
            vuelo.eliminar_pasajero(nombre)
            print("Pasaje devuelto correctamente.")
        except:
            print("Error al devolver el pasaje.")

    def trayecto_mas_recaudo(self):
        max_vuelo = None
        max_total = 0
        for vuelo in self.vuelos.recorrer():
            if vuelo.total_tiquetes > max_total:
                max_total = vuelo.total_tiquetes
                max_vuelo = vuelo
        if max_vuelo:
            print(f"Trayecto con más recaudo: {max_vuelo.origen} -> {max_vuelo.destino}, Total: {max_total}")
        else:
            print("No hay vuelos registrados.")

    def genero_dominante(self):
        destino = input("Ingrese el destino a consultar: ")
        hombres = mujeres = 0
        for vuelo in self.vuelos.recorrer():
            if vuelo.destino.lower() == destino.lower():
                for p in vuelo.pasajeros.recorrer():
                    if p.genero == "m":
                        hombres += 1
                    elif p.genero == "f":
                        mujeres += 1
        if hombres > mujeres:
            print(f"Más hombres viajan a {destino}")
        elif mujeres > hombres:
            print(f"Más mujeres viajan a {destino}")
        else:
            print(f"Igual número de hombres y mujeres a {destino}")

    def promedio_tiquete_por_vuelo(self):
        for vuelo in self.vuelos.recorrer():
            print(f"{vuelo.origen} -> {vuelo.destino}: Promedio = {vuelo.promedio_tiquete():.2f}")

    def recaudo_total_tiquetes(self):
        total = 0
        for vuelo in self.vuelos.recorrer():
            total += vuelo.total_tiquetes
        print(f"Recaudo total por tiquetes: {total}")

    def recaudo_equipaje_extra(self):
        total = 0
        for vuelo in self.vuelos.recorrer():
            total += vuelo.total_equipaje_extra
        print(f"Recaudo total por equipaje extra y cargas especiales: {total}")

def main():
    sistema = Aerolinea()
    while True:
        print("\\n--- MENÚ AEROLÍNEA ---")
        print("1. Crear vuelo")
        print("2. Vender tiquete")
        print("3. Hacer check-in")
        print("4. Devolver pasaje")
        print("5. Trayecto con más recaudo")
        print("6. Género dominante por destino")
        print("7. Promedio de tiquete por vuelo")
        print("8. Recaudo total de tiquetes")
        print("9. Recaudo por equipaje extra")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            sistema.crear_vuelo()
        elif opcion == "2":
            sistema.vender_tiquete()
        elif opcion == "3":
            sistema.hacer_checkin()
        elif opcion == "4":
            sistema.devolver_pasaje()
        elif opcion == "5":
            sistema.trayecto_mas_recaudo()
        elif opcion == "6":
            sistema.genero_dominante()
        elif opcion == "7":
            sistema.promedio_tiquete_por_vuelo()
        elif opcion == "8":
            sistema.recaudo_total_tiquetes()
        elif opcion == "9":
            sistema.recaudo_equipaje_extra()
        elif opcion == "0":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

