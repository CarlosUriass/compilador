from dataclasses import dataclass
from .nodo_ast import NodoAST, TipoNodo



@dataclass
class NodoDeclaracion(NodoAST):
    """
    Sentencia más sencilla: declaración de variable sin asignación.

    GLC: declaracion → tipo ID ';'

    Ejemplo:  Entero x;
              Decimal precio;

    Campos:
        tipo_dato  — 'Entero' | 'Decimal' | 'Expresion' | 'Binario'
        nombre_id  — nombre de la variable (lexema del token ID)
    """
    tipo_dato:  str = ""
    nombre_id:  str = ""

    def __post_init__(self):
        # Forzar el TipoNodo correcto independientemente de lo que pase el caller
        self.tipo = TipoNodo.DECLARACION

    def __repr__(self) -> str:
        return f"Declaracion(tipo={self.tipo_dato!r}, id={self.nombre_id!r})"


@dataclass
class NodoDeclaracionAsig(NodoAST):
    """
    Declaración con asignación inmediata.

    GLC: declaracion_asig → tipo ID '=' expresion ';'

    Ejemplo:  Entero x = 5;
              Decimal pi = 3.14;

    Campos:
        tipo_dato  — tipo de la variable
        nombre_id  — nombre de la variable
        expresion  — NodoAST que representa el valor asignado
    """
    tipo_dato:  str     = ""
    nombre_id:  str     = ""
    expresion:  NodoAST = None  # type: ignore

    def __post_init__(self):
        self.tipo = TipoNodo.DECLARACION_ASIG
        if self.expresion:
            self.hijos = [self.expresion]

    def __repr__(self) -> str:
        return (f"DeclaracionAsig(tipo={self.tipo_dato!r}, "
                f"id={self.nombre_id!r}, expr={self.expresion!r})")


@dataclass
class NodoAsignacion(NodoAST):
    """
    Asignación a una variable ya declarada.

    GLC: asignacion → ID '=' expresion ';'

    Ejemplo:  x = x + 1;

    Campos:
        nombre_id  — variable destino
        expresion  — NodoAST del valor a asignar
    """
    nombre_id:  str     = ""
    expresion:  NodoAST = None  # type: ignore

    def __post_init__(self):
        self.tipo = TipoNodo.ASIGNACION
        if self.expresion:
            self.hijos = [self.expresion]

    def __repr__(self) -> str:
        return f"Asignacion(id={self.nombre_id!r}, expr={self.expresion!r})"


@dataclass
class NodoSalida(NodoAST):
    """
    Instrucción de salida.

    GLC: salida → 'Mostrar' argumento ';'

    Ejemplo:  Mostrar "Hola";
              Mostrar x;

    Campos:
        argumento  — NodoAST del valor a mostrar (ID, CADENA o expresion)
    """
    argumento: NodoAST = None  # type: ignore

    def __post_init__(self):
        self.tipo = TipoNodo.SALIDA
        if self.argumento:
            self.hijos = [self.argumento]

    def __repr__(self) -> str:
        return f"Salida(arg={self.argumento!r})"


@dataclass
class NodoEntrada(NodoAST):
    """
    Instrucción de entrada.

    GLC: entrada → 'Capturar' ID ';'

    Ejemplo:  Capturar nombre;

    Campos:
        nombre_id  — variable donde se almacena la entrada
    """
    nombre_id: str = ""

    def __post_init__(self):
        self.tipo = TipoNodo.ENTRADA

    def __repr__(self) -> str:
        return f"Entrada(id={self.nombre_id!r})"


@dataclass
class NodoBorrar(NodoAST):
    """
    Instrucción de borrado de variable.

    GLC: borrar → 'Borrar' ID ';'

    Ejemplo:  Borrar x;

    Campos:
        nombre_id  — variable a borrar
    """
    nombre_id: str = ""

    def __post_init__(self):
        self.tipo = TipoNodo.BORRAR

    def __repr__(self) -> str:
        return f"Borrar(id={self.nombre_id!r})"


@dataclass
class NodoCondicional(NodoAST):
    """
    Sentencia condicional con rama opcional.

    GLC: condicional → 'Si' condicion 'Entonces' cuerpo ['Sino' cuerpo]

    Campos:
        condicion  — NodoAST de la condición
        entonces   — lista de NodoAST del cuerpo verdadero
        sino       — lista de NodoAST del cuerpo alternativo (puede ser vacío)
    """
    condicion:  NodoAST = None   # type: ignore
    entonces:   list    = None   # type: ignore
    sino:       list    = None   # type: ignore

    def __post_init__(self):
        self.tipo = TipoNodo.CONDICIONAL
        self.entonces = self.entonces or []
        self.sino = self.sino or []
        self.hijos = ([self.condicion] if self.condicion else []) + self.entonces + self.sino

    def __repr__(self) -> str:
        return (f"Condicional(cond={self.condicion!r}, "
                f"entonces={self.entonces!r}, sino={self.sino!r})")


@dataclass
class NodoBucle(NodoAST):
    """
    Sentencia de repetición.

    GLC: bucle → 'Mientras' condicion 'Hacer' cuerpo

    Campos:
        condicion  — NodoAST de la condición de continuación
        cuerpo     — lista de NodoAST del cuerpo del bucle
    """
    condicion:  NodoAST = None   # type: ignore
    cuerpo:     list    = None   # type: ignore

    def __post_init__(self):
        self.tipo = TipoNodo.BUCLE
        self.cuerpo = self.cuerpo or []
        self.hijos = ([self.condicion] if self.condicion else []) + self.cuerpo

    def __repr__(self) -> str:
        return f"Bucle(cond={self.condicion!r}, cuerpo={self.cuerpo!r})"


# ---------------------------------------------------------------------------
# Nodos de expresión (hojas y nodos internos)
# ---------------------------------------------------------------------------

def nodo_id(nombre: str) -> NodoAST:
    """Crea un nodo hoja para un identificador."""
    return NodoAST(tipo=TipoNodo.ID, valor=nombre)


def nodo_literal(tipo: TipoNodo, valor) -> NodoAST:
    """Crea un nodo hoja para un literal (entero, real o cadena)."""
    return NodoAST(tipo=tipo, valor=valor)


def nodo_expresion_bin(operador: str, izq: NodoAST, der: NodoAST) -> NodoAST:
    """Crea un nodo de expresión binaria."""
    return NodoAST(tipo=TipoNodo.EXPRESION_BIN, valor=operador, hijos=[izq, der])


def nodo_condicion(operador: str, izq: NodoAST, der: NodoAST) -> NodoAST:
    """Crea un nodo de condición relacional (x > 0, a == b, etc.)"""
    return NodoAST(tipo=TipoNodo.CONDICION, valor=operador, hijos=[izq, der])


def nodo_expresion_una(operador: str, operando: NodoAST) -> NodoAST:
    """Crea un nodo de expresión unaria. Equivalente a make_ExpUna del main.c"""
    return NodoAST(tipo=TipoNodo.EXPRESION_UNA, valor=operador, hijos=[operando])


def nodo_condicion_log(operador: str, izq: NodoAST, der: NodoAST) -> NodoAST:
    """Crea un nodo de condición lógica (& o |)."""
    return NodoAST(tipo=TipoNodo.CONDICION_LOG, valor=operador, hijos=[izq, der])


# ---------------------------------------------------------------------------
# Nodo raíz del programa
# ---------------------------------------------------------------------------

@dataclass
class NodoPrograma(NodoAST):
    """
    Nodo raíz del AST. Envuelve todas las sentencias del programa.

    GLC: programa → 'Inicio' cuerpo 'Final'

    Campos:
        sentencias — lista de NodoAST con el cuerpo completo del programa
    """
    sentencias: list = None  # type: ignore

    def __post_init__(self):
        self.tipo = TipoNodo.PROGRAMA
        self.sentencias = self.sentencias or []
        self.hijos = self.sentencias

    def __repr__(self) -> str:
        body = "\n  ".join(repr(s) for s in self.sentencias)
        return f"Programa(\n  {body}\n)"

