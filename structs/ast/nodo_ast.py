from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any


class TipoNodo(Enum):
    """
    Cada valor representa un tipo de nodo en el AST.
    """
    # Nodo raíz
    PROGRAMA         = auto()   # nodo raíz del programa completo

    # Sentencias
    DECLARACION      = auto()   
    DECLARACION_ASIG = auto()   
    ASIGNACION       = auto()   
    CONDICIONAL      = auto()   
    BUCLE            = auto()   
    SALIDA           = auto()   
    ENTRADA          = auto()   
    BORRAR           = auto()   

    # Expresiones
    EXPRESION_BIN    = auto()   
    EXPRESION_UNA    = auto()   
    CONDICION        = auto()   
    CONDICION_LOG    = auto()   

    # Hojas (terminales)
    LITERAL_ENTERO   = auto()   
    LITERAL_REAL     = auto()   
    LITERAL_CADENA   = auto()   
    ID               = auto()   


@dataclass
class NodoAST:
    """
    Clase base del AST

    Atributos:
        tipo   — tipo del nodo (TipoNodo)
        valor  — valor del nodo (lexema, operador, tipo_dato, etc.)
        hijos  — lista de NodoAST hijos (para recorrer en pre/in/post-orden)
    """
    tipo:   TipoNodo
    valor:  Any             = None
    hijos:  list            = field(default_factory=list)

    def __repr__(self) -> str:
        if self.hijos:
            hijos_repr = ", ".join(repr(h) for h in self.hijos)
            return f"{self.tipo.name}({self.valor!r}, [{hijos_repr}])"
        return f"{self.tipo.name}({self.valor!r})"
