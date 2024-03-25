class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar_nodo(self, nuevo_nodo):
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = actual

    def ordenar_alfabeticamente(self):
        if self.cabeza is None:
            return

        cambios = True
        while cambios:
            cambios = False
            actual = self.cabeza
            while actual.siguiente:
                if actual.objeto.nombre > actual.siguiente.objeto.nombre:
                    
                    # Intercambiar los nodos
                    temp = actual.objeto
                    actual.objeto = actual.siguiente.objeto
                    actual.siguiente.objeto = temp
                    
                    cambios = True
                actual = actual.siguiente

    def buscar_nodo(self, dato):
        actual = self.cabeza
        while actual:
            if actual.objeto.nombre == dato:
                return actual
            actual = actual.siguiente
        return None


    def imprimir_lista(self):
        actual = self.cabeza
        while actual:
            print(f"  - {actual.objeto.objetivos}")
            actual = actual.siguiente 