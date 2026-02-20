class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaEnlazadaDobleCircular:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def esta_vacia(self):
        return self.size == 0
    
    def __len__(self):
        return self.size

    def insertar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
            self.head.siguiente = self.head
            self.head.anterior = self.head
        else:
            nuevo_nodo.siguiente = self.head
            nuevo_nodo.anterior = self.tail
            self.head.anterior = nuevo_nodo
            self.tail.siguiente = nuevo_nodo
            self.head = nuevo_nodo
        self.size += 1

    def insertar_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
            self.head.siguiente = self.head
            self.head.anterior = self.head
        else:
            nuevo_nodo.siguiente = self.head
            nuevo_nodo.anterior = self.tail
            self.tail.siguiente = nuevo_nodo
            self.head.anterior = nuevo_nodo
            self.tail = nuevo_nodo
        self.size += 1

    def eliminar_inicio(self):
        if self.esta_vacia():
            return None
        
        nodo_eliminado = self.head
        dato_eliminado = nodo_eliminado.dato
        
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.siguiente
            self.head.anterior = self.tail
            self.tail.siguiente = self.head
            
        # Limpieza de punteros del nodo extraído
        nodo_eliminado.siguiente = None
        nodo_eliminado.anterior = None
        
        self.size -= 1
        return dato_eliminado

    def eliminar_final(self):
        if self.esta_vacia():
            return None
            
        nodo_eliminado = self.tail
        dato_eliminado = nodo_eliminado.dato
        
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.anterior
            self.tail.siguiente = self.head
            self.head.anterior = self.tail
            
        # Limpieza de punteros del nodo extraído
        nodo_eliminado.siguiente = None
        nodo_eliminado.anterior = None
        
        self.size -= 1
        return dato_eliminado

    def buscar(self, dato):
        if self.esta_vacia():
            return False
            
        actual = self.head
        while True:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
            if actual == self.head:
                break
        return False

    def eliminar_valor(self, dato):
        if self.esta_vacia():
            return False
            
        if self.head.dato == dato:
            self.eliminar_inicio()
            return True
            
        actual = self.head.siguiente
        while actual != self.head:
            if actual.dato == dato:
                actual.anterior.siguiente = actual.siguiente
                actual.siguiente.anterior = actual.anterior
                if actual == self.tail:
                    self.tail = actual.anterior
                
                # Limpieza de punteros
                actual.siguiente = None
                actual.anterior = None
                
                self.size -= 1
                return True
            actual = actual.siguiente
        return False

    def mostrar_adelante(self):
        if self.esta_vacia():
            return []
        
        elementos = []
        actual = self.head
        while True:
            elementos.append(actual.dato)
            actual = actual.siguiente
            if actual == self.head:
                break
        return elementos

    def mostrar_atras(self):
        if self.esta_vacia():
            return []
            
        elementos = []
        actual = self.tail
        while True:
            elementos.append(actual.dato)
            actual = actual.anterior
            if actual == self.tail:
                break
        return elementos