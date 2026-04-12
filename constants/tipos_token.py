from enum import Enum

class TipoToken(Enum):
    """
    Enumeración que define los diferentes tipos de tokens 
    reconocidos por el analizador léxico.
    """
    ID = "ID"
    PALABRA_RESERVADA = "PALABRA_RESERVADA"

    NUMERO_ENTERO = "NUMERO_ENTERO"
    NUMERO_REAL = "NUMERO_REAL"
    CADENA = "CADENA"

    OP_ARITMETICO = "OP_ARITMETICO"
    OP_RELACIONAL = "OP_RELACIONAL"
    OP_LOGICO = "OP_LOGICO"
    OP_ASIGNACION = "OP_ASIGNACION"

    SIMBOLO_APERTURA = "SIMBOLO_APERTURA"
    SIMBOLO_CIERRE = "SIMBOLO_CIERRE"
    SIMBOLO_PUNTUACION = "SIMBOLO_PUNTUACION"

    ERROR = "ERROR"
    EOF = "EOF"     # Fin de archivo
