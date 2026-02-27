from enum import Enum

class Operador(Enum):
    MULTIPLICACION = "*"
    SUMA = "+"
    POTENCIA = "**"
    RESTA = "-"
    DIVISION = "/"
    MENOR_QUE = "<"
    MAYOR_QUE = ">"
    MENOR_IGUAL = "<="
    MAYOR_IGUAL = ">="
    DIFERENTE = "!="
    IGUAL = "=="
    AND_BIT = "&"
    OR_BIT = "|"