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