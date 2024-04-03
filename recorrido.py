class Recorrido:
    def __init__(self):
        self.camino = []
        self.objetivos_recogidos = set()

    def agregar_al_camino(self, paso):
        self.camino.append(paso)

    def recoger_objetivo(self, obj):
        self.objetivos_recogidos.add(obj)

    def __str__(self):
        return str(self.camino)