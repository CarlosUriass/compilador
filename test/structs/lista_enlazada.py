import unittest
from structs import ListaEnlazadaDobleCircular

class TestListaEnlazadaDobleCircular(unittest.TestCase):
    def setUp(self):
        self.lista = ListaEnlazadaDobleCircular()

    def test_inicializacion(self):
        self.assertTrue(self.lista.esta_vacia())
        self.assertEqual(len(self.lista), 0)
        self.assertEqual(self.lista.mostrar_adelante(), [])
        self.assertEqual(self.lista.mostrar_atras(), [])
        self.assertIsNone(self.lista.head)
        self.assertIsNone(self.lista.tail)

    def test_insertar_inicio(self):
        self.lista.insertar_inicio(10)
        self.assertEqual(len(self.lista), 1)
        self.assertEqual(self.lista.mostrar_adelante(), [10])
        self.assertEqual(self.lista.mostrar_atras(), [10])
        
        self.lista.insertar_inicio(20)
        self.assertEqual(len(self.lista), 2)
        self.assertEqual(self.lista.mostrar_adelante(), [20, 10])
        self.assertEqual(self.lista.mostrar_atras(), [10, 20])

    def test_insertar_final(self):
        self.lista.insertar_final("A")
        self.assertEqual(len(self.lista), 1)
        
        self.lista.insertar_final("B")
        self.lista.insertar_final("C")
        self.assertEqual(len(self.lista), 3)
        self.assertEqual(self.lista.mostrar_adelante(), ["A", "B", "C"])
        self.assertEqual(self.lista.mostrar_atras(), ["C", "B", "A"])

    def test_eliminar_inicio(self):
        # Caso: lista vacia
        self.assertIsNone(self.lista.eliminar_inicio())
        
        self.lista.insertar_final(1)
        self.lista.insertar_final(2)
        self.lista.insertar_final(3)
        
        # Eliminar el primer elemento
        eliminado = self.lista.eliminar_inicio()
        self.assertEqual(eliminado, 1)
        self.assertEqual(len(self.lista), 2)
        self.assertEqual(self.lista.mostrar_adelante(), [2, 3])
        self.assertEqual(self.lista.mostrar_atras(), [3, 2])
        
        # Vaciando la lista
        self.lista.eliminar_inicio()
        self.lista.eliminar_inicio()
        self.assertTrue(self.lista.esta_vacia())
        self.assertIsNone(self.lista.head)
        self.assertIsNone(self.lista.tail)

    def test_eliminar_final(self):
        # Caso: lista vacia
        self.assertIsNone(self.lista.eliminar_final())
        
        self.lista.insertar_final(10)
        self.lista.insertar_final(20)
        self.lista.insertar_final(30)
        
        # Eliminar el ultimo elemento
        eliminado = self.lista.eliminar_final()
        self.assertEqual(eliminado, 30)
        self.assertEqual(len(self.lista), 2)
        self.assertEqual(self.lista.mostrar_adelante(), [10, 20])
        self.assertEqual(self.lista.mostrar_atras(), [20, 10])
        
        # Vaciando la lista
        self.lista.eliminar_final()
        self.lista.eliminar_final()
        self.assertTrue(self.lista.esta_vacia())

    def test_buscar(self):
        # Buscar en lista vacia
        self.assertFalse(self.lista.buscar(100))
        
        self.lista.insertar_final(10)
        self.lista.insertar_final(20)
        self.lista.insertar_final(30)
        
        self.assertTrue(self.lista.buscar(10))
        self.assertTrue(self.lista.buscar(20))
        self.assertTrue(self.lista.buscar(30))
        self.assertFalse(self.lista.buscar(40))

    def test_eliminar_valor(self):
        # Eliminar valor en lista vacía
        self.assertFalse(self.lista.eliminar_valor(10))
        
        self.lista.insertar_final(10)
        self.lista.insertar_final(20)
        self.lista.insertar_final(30)
        self.lista.insertar_final(40)
        
        # Eliminar un nodo intermedio
        self.assertTrue(self.lista.eliminar_valor(20))
        self.assertEqual(len(self.lista), 3)
        self.assertEqual(self.lista.mostrar_adelante(), [10, 30, 40])
        self.assertEqual(self.lista.mostrar_atras(), [40, 30, 10])
        
        # Eliminar en la cabeza
        self.assertTrue(self.lista.eliminar_valor(10))
        self.assertEqual(len(self.lista), 2)
        self.assertEqual(self.lista.mostrar_adelante(), [30, 40])
        self.assertEqual(self.lista.head.dato, 30)
        
        # Eliminar en la cola
        self.assertTrue(self.lista.eliminar_valor(40))
        self.assertEqual(len(self.lista), 1)
        self.assertEqual(self.lista.mostrar_adelante(), [30])
        self.assertEqual(self.lista.tail.dato, 30)
        
        # Intentar eliminar un valor que no existe
        self.assertFalse(self.lista.eliminar_valor(100))
        self.assertEqual(len(self.lista), 1)
        
        # Eliminar el único nodo existente (vaciándola)
        self.assertTrue(self.lista.eliminar_valor(30))
        self.assertTrue(self.lista.esta_vacia())
        self.assertIsNone(self.lista.head)
        self.assertIsNone(self.lista.tail)

if __name__ == '__main__':
    unittest.main()
