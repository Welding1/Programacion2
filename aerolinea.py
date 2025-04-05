class Vuelo:
    def __init__(self, origen, destino, precio_base):
        self.origen = origen
        self.destino = destino
        self.precio_base = precio_base
        self.pasajeros = []
        self.recaudo = 0

    def vender_tiquete(self, pasajero):
        self.pasajeros.append(pasajero)
        self.recaudo += pasajero.calcular_precio_total(self.precio_base)

    def calcular_recaudo(self):
        return self.recaudo

    def costo_promedio(self):
        if len(self.pasajeros) > 0:
            return self.recaudo / len(self.pasajeros)
        return 0


class Pasajero:
    def __init__(self, nombre, edad, genero, clase, infante=False):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.clase = clase
        self.infante = infante
        self.equipaje = 0  # en kilos
        self.cargas_especiales = []  # Lista de cargas especiales
        self.valor_tiquete = 0
        self.precio_final = 0

    def calcular_precio_total(self, precio_base):
        self.valor_tiquete = precio_base
        if self.infante:
            self.valor_tiquete *= 0.93  # 7% de descuento

        self.precio_final = self.valor_tiquete

        # Calcular equipaje adicional
        if self.clase == "economica" and self.equipaje > 10:
            self.precio_final += (self.equipaje - 10) * 5000
        elif self.clase == "ejecutiva" and self.equipaje > 20:
            self.precio_final += (self.equipaje - 20) * 10000
        elif self.clase == "premium" and self.equipaje > 30:
            self.precio_final += (self.equipaje - 30) * (self.valor_tiquete * 0.01)

        # Calcular el costo de cargas especiales
        for carga in self.cargas_especiales:
            if carga[0] == "bicicleta":
                self.precio_final += carga[1] * 1000  # X es el costo por kilo de bicicleta
            elif carga[0] == "mascota":
                if carga[2] == "perro":
                    self.precio_final += self.valor_tiquete * 0.05
                elif carga[2] == "gato":
                    self.precio_final += self.valor_tiquete * 0.02

        return self.precio_final

    def agregar_equipaje(self, kilos):
        self.equipaje += kilos

    def agregar_carga_especial(self, tipo, peso=None, especie=None):
        if tipo == "bicicleta":
            self.cargas_especiales.append((tipo, peso))
        elif tipo == "mascota":
            self.cargas_especiales.append((tipo, peso, especie))


class Aerolinea:
    def __init__(self):
        self.vuelos = []
        self.recaudo_total_tiquetes = 0
        self.recaudo_total_equipaje = 0
        self.pasajeros = []

    def crear_vuelo(self, origen, destino, precio_base):
        vuelo = Vuelo(origen, destino, precio_base)
        self.vuelos.append(vuelo)

    def vender_tiquete(self, vuelo, pasajero):
        vuelo.vender_tiquete(pasajero)
        self.recaudo_total_tiquetes += pasajero.precio_final
        self.pasajeros.append(pasajero)

    def hacer_checkin(self, pasajero):
        # Cobro equipaje extra
        if pasajero.clase == "economica" and pasajero.equipaje > 10:
            self.recaudo_total_equipaje += (pasajero.equipaje - 10) * 5000
        elif pasajero.clase == "ejecutiva" and pasajero.equipaje > 20:
            self.recaudo_total_equipaje += (pasajero.equipaje - 20) * 10000
        elif pasajero.clase == "premium" and pasajero.equipaje > 30:
            self.recaudo_total_equipaje += (pasajero.equipaje - 30) * (pasajero.valor_tiquete * 0.01)

        # Cobro por carga especial
        for carga in pasajero.cargas_especiales:
            if carga[0] == "bicicleta":
                self.recaudo_total_equipaje += carga[1] * 1000  # X es el costo por kilo de bicicleta
            elif carga[0] == "mascota":
                if carga[2] == "perro":
                    self.recaudo_total_equipaje += pasajero.valor_tiquete * 0.05
                elif carga[2] == "gato":
                    self.recaudo_total_equipaje += pasajero.valor_tiquete * 0.02

    def devolver_pasaje(self, pasajero, vuelo):
        if pasajero in vuelo.pasajeros:
            vuelo.pasajeros.remove(pasajero)
            self.recaudo_total_tiquetes -= pasajero.precio_final

    def trayecto_mas_recaudado(self):
        trayecto = max(self.vuelos, key=lambda vuelo: vuelo.calcular_recaudo())
        return trayecto.origen, trayecto.destino, trayecto.calcular_recaudo()

    def quienes_viajan_mas(self, destino):
        hombres = 0
        mujeres = 0
        for vuelo in self.vuelos:
            if vuelo.origen != destino:
                continue
            for pasajero in vuelo.pasajeros:
                if pasajero.genero == "masculino":
                    hombres += 1
                elif pasajero.genero == "femenino":
                    mujeres += 1
        return "Mujeres" if mujeres > hombres else "Hombres"

    def recaudo_total(self):
        return self.recaudo_total_tiquetes + self.recaudo_total_equipaje

    def costo_promedio_por_trayecto(self):
        total_recaudo = 0
        total_pasajeros = 0
        for vuelo in self.vuelos:
            total_recaudo += vuelo.recaudo
            total_pasajeros += len(vuelo.pasajeros)
        return total_recaudo / total_pasajeros if total_pasajeros > 0 else 0
