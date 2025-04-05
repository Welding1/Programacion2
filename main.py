class Asignatura:
    def __init__(self, nombre, creditos, costo_credito):
        self.nombre = nombre
        self.creditos = creditos
        self.costo_credito = costo_credito
        self.estudiantes = []

    def agregar_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def calcular_recaudo(self):
        total = 0
        for estudiante in self.estudiantes:
            descuento = estudiante.calcular_descuento(self.costo_credito)
            total += (self.costo_credito - descuento) * self.creditos
        return total

    def cantidad_estudiantes(self):
        return len(self.estudiantes)

    def estudiantes_estrato(self, estrato):
        return len([est for est in self.estudiantes if est.estrato == estrato])


class Estudiante:
    def __init__(self, nombre, genero, edad, estrato):
        self.nombre = nombre
        self.genero = genero
        self.edad = edad
        self.estrato = estrato

    def calcular_descuento(self, costo_credito):
        if self.estrato == 1:
            return costo_credito * 0.50
        elif self.estrato == 2:
            return costo_credito * 0.30
        elif self.estrato == 3:
            return costo_credito * 0.10
        else:
            return 0


def registrar_asignaturas():
    asignaturas = []
    while True:
        try:
            nombre = input("Ingrese el nombre de la asignatura: ")
            if nombre == "":
                break
            creditos = int(input("Ingrese la cantidad de créditos: "))
            costo_credito = float(input("Ingrese el costo por crédito: "))
            asignatura = Asignatura(nombre, creditos, costo_credito)
            asignaturas.append(asignatura)
        except ValueError:
            print("Error: Por favor ingrese valores válidos.")
    return asignaturas


def registrar_estudiantes(asignaturas):
    while True:
        try:
            nombre = input("Ingrese el nombre del estudiante: ")
            if nombre == "":
                break
            genero = input("Ingrese el género del estudiante: ")
            edad = int(input("Ingrese la edad del estudiante: "))
            estrato = int(input("Ingrese el estrato del estudiante (1, 2 o 3): "))
            asignatura_nombre = input("Ingrese el nombre de la asignatura a la que se va a matricular: ")
            
            estudiante = Estudiante(nombre, genero, edad, estrato)
            asignatura = next((asignatura for asignatura in asignaturas if asignatura.nombre == asignatura_nombre), None)
            
            if asignatura:
                asignatura.agregar_estudiante(estudiante)
            else:
                print("La asignatura no existe.")
        except ValueError:
            print("Error: Por favor ingrese valores válidos.")


def mostrar_informacion(asignaturas):
    print("\nInformación sobre las asignaturas:")
    
    for asignatura in asignaturas:
        print(f"Asignatura: {asignatura.nombre}")
        print(f"Cantidad de estudiantes: {asignatura.cantidad_estudiantes()}")
        print(f"Recaudo total por matrícula: {asignatura.calcular_recaudo()}")
        
        estrato_1 = asignatura.estudiantes_estrato(1)
        print(f"Estudiantes de estrato 1 en esta asignatura: {estrato_1}")
        
    asignatura_max_recaudo = max(asignaturas, key=lambda x: x.calcular_recaudo())
    print(f"\nLa asignatura que más recaudó es: {asignatura_max_recaudo.nombre}")
    
    promedio_creditos = sum([asignatura.costo_credito for asignatura in asignaturas]) / len(asignaturas)
    print(f"Promedio de costo de los créditos: {promedio_creditos}")
    
    estrato = int(input("\nIngrese el estrato para calcular el total de descuentos (1, 2 o 3): "))
    total_descuentos = sum([asignatura.calcular_recaudo() * 0.50 if estrato == 1 else asignatura.calcular_recaudo() * 0.30 if estrato == 2 else asignatura.calcular_recaudo() * 0.10 for asignatura in asignaturas])
    print(f"Total de descuentos para el estrato {estrato}: {total_descuentos}")
    
    total_recaudado = sum([asignatura.calcular_recaudo() for asignatura in asignaturas])
    print(f"\nTotal de dinero recaudado entre todas las asignaturas: {total_recaudado}")


def main():
    asignaturas = registrar_asignaturas()
    registrar_estudiantes(asignaturas)
    mostrar_informacion(asignaturas)


if __name__ == "__main__":
    main()
