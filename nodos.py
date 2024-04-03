class Nodo:
    def __init__(self, objeto):
        self.objeto = objeto
        self.siguiente = None
        self.anterior = None

class Estructura:
    def __init__(self, color):
        self.color = color
        self.siguiente = None
        self.anterior = None

class Objetivos:
    def __init__(self, nombre_ob, fila_ob, col_ob):
        self.nombre_ob = nombre_ob
        self.fila_ob = fila_ob
        self.col_ob = col_ob
        self.siguiente = None
        self.anterior = None