"""
Analizador Sintáctico
=====================
Recorre la ListaEnlazadaDobleCircular de tokens producida por el analizador
léxico y construye un AST (lista de NodoAST) verificando la gramática del
lenguaje.

Uso:
    from analizador_sintactico import analizar_sintaxis
    lista_nodos = analizar_sintaxis(lista_tokens)
"""

from constants.tipos_token import TipoToken
from structs.lista_enlazada import ListaEnlazadaDobleCircular
from structs.ast import (
    NodoAST, TipoNodo,
    NodoDeclaracion, NodoDeclaracionAsig,
    NodoAsignacion, NodoSalida, NodoEntrada, NodoBorrar,
    NodoCondicional, NodoBucle, NodoPrograma,
    nodo_id, nodo_literal, nodo_expresion_bin,
    nodo_condicion, nodo_condicion_log,
)


# ---------------------------------------------------------------------------
# Error sintáctico con posición
# ---------------------------------------------------------------------------

class ErrorSintactico(Exception):
    """Se lanza cuando la secuencia de tokens no respeta la gramática."""

    def __init__(self, mensaje: str, linea: int = 0, columna: int = 0):
        pos = f"\n  → línea {linea}, columna {columna}" if linea else ""
        super().__init__(f"{mensaje}{pos}")
        self.linea = linea
        self.columna = columna


# ---------------------------------------------------------------------------
# Cursor sobre la lista enlazada
# ---------------------------------------------------------------------------

class Cursor:
    """
    Mantiene un puntero al nodo actual de la lista enlazada de tokens.
    Cada token es una tupla: (TipoToken, lexema, linea, columna).
    """

    def __init__(self, lista: ListaEnlazadaDobleCircular):
        self._nodo_actual = lista.head
        self._lista = lista
        self.linea   = 0
        self.columna = 0

    # ---- Inspección -------------------------------------------------------

    def peek(self) -> tuple | None:
        """Devuelve la tupla completa (tipo, lexema, linea, col) sin avanzar."""
        if self._nodo_actual is None:
            return None
        return self._nodo_actual.dato

    def peek_tipo(self) -> TipoToken | None:
        t = self.peek()
        return t[0] if t else None

    def peek_lexema(self) -> str | None:
        t = self.peek()
        return t[1] if t else None

    def tiene_tokens(self) -> bool:
        return self._nodo_actual is not None

    # ---- Avance -----------------------------------------------------------

    def consume(self) -> tuple:
        """Devuelve el token actual, actualiza posición y avanza al siguiente."""
        if self._nodo_actual is None:
            raise ErrorSintactico(
                "Se esperaba un token pero se llegó al final del archivo.",
                self.linea, self.columna
            )

        dato = self._nodo_actual.dato          # (tipo, lexema, linea, col)
        self.linea   = dato[2]
        self.columna = dato[3]

        siguiente = self._nodo_actual.siguiente
        if siguiente is self._lista.head:
            self._nodo_actual = None           # vuelta completa → fin
        else:
            self._nodo_actual = siguiente

        return dato

    def esperar(self, tipo: TipoToken, lexema: str | None = None) -> tuple:
        """
        Consume el token actual verificando tipo (y lexema opcional).
        Lanza ErrorSintactico con posición si no coincide.
        """
        tok = self.peek()
        if tok is None:
            raise ErrorSintactico(
                f"Se esperaba {tipo.value!r}"
                + (f" '{lexema}'" if lexema else "")
                + " pero se llegó al final del archivo.",
                self.linea, self.columna
            )

        tok_tipo, tok_lexema, tok_lin, tok_col = tok

        if tok_tipo != tipo:
            raise ErrorSintactico(
                f"Se esperaba tipo {tipo.value!r}"
                + (f" '{lexema}'" if lexema else "")
                + f" pero se encontró {tok_tipo.value!r} ('{tok_lexema}').",
                tok_lin, tok_col
            )
        if lexema is not None and tok_lexema != lexema:
            raise ErrorSintactico(
                f"Se esperaba '{lexema}' pero se encontró '{tok_lexema}'.",
                tok_lin, tok_col
            )
        return self.consume()


# ---------------------------------------------------------------------------
# Conjuntos de operadores
# ---------------------------------------------------------------------------

TIPOS_DATO   = {"Entero", "Decimal", "Expresion", "Binario"}
OP_ARITM_MUL = {"*", "/", "**"}
OP_ARITM_ADD = {"+", "-"}

# Tokens que indican fin de cuerpo anidado (comparación sobre los primeros 2 elementos)
_FIN_CUERPO = {
    (TipoToken.PALABRA_RESERVADA, "Final"),
    (TipoToken.PALABRA_RESERVADA, "Sino"),
}


def _es_fin_cuerpo(tok: tuple | None) -> bool:
    if tok is None:
        return True
    return (tok[0], tok[1]) in _FIN_CUERPO


# ---------------------------------------------------------------------------
# Funciones de parseo por sentencia
# ---------------------------------------------------------------------------

def parsear_factor(cur: Cursor) -> NodoAST:
    """factor → NUMERO_ENTERO | NUMERO_REAL | CADENA | ID | '(' expresion ')'"""
    tok = cur.peek()
    if tok is None:
        raise ErrorSintactico("Se esperaba un factor pero se llegó al final.",
                               cur.linea, cur.columna)

    tipo, lexema, lin, col = tok

    if tipo == TipoToken.NUMERO_ENTERO:
        cur.consume()
        return nodo_literal(TipoNodo.LITERAL_ENTERO, int(lexema))

    if tipo == TipoToken.NUMERO_REAL:
        cur.consume()
        return nodo_literal(TipoNodo.LITERAL_REAL, float(lexema))

    if tipo == TipoToken.CADENA:
        cur.consume()
        return nodo_literal(TipoNodo.LITERAL_CADENA, lexema)

    if tipo == TipoToken.ID:
        cur.consume()
        return nodo_id(lexema)

    if tipo == TipoToken.SIMBOLO_APERTURA and lexema == "(":
        cur.consume()
        nodo = parsear_expresion(cur)
        cur.esperar(TipoToken.SIMBOLO_CIERRE, ")")
        return nodo

    raise ErrorSintactico(
        f"Se esperaba un factor (número, cadena, ID o '(') "
        f"pero se encontró {tipo.value!r} ('{lexema}').",
        lin, col
    )


def parsear_termino(cur: Cursor) -> NodoAST:
    """termino → factor { ('*' | '/' | '**') factor }"""
    izq = parsear_factor(cur)
    while cur.tiene_tokens():
        tok = cur.peek()
        if tok and tok[0] == TipoToken.OP_ARITMETICO and tok[1] in OP_ARITM_MUL:
            op = cur.consume()[1]
            der = parsear_factor(cur)
            izq = nodo_expresion_bin(op, izq, der)
        else:
            break
    return izq


def parsear_expresion(cur: Cursor) -> NodoAST:
    """expresion → termino { ('+' | '-') termino }"""
    izq = parsear_termino(cur)
    while cur.tiene_tokens():
        tok = cur.peek()
        if tok and tok[0] == TipoToken.OP_ARITMETICO and tok[1] in OP_ARITM_ADD:
            op = cur.consume()[1]
            der = parsear_termino(cur)
            izq = nodo_expresion_bin(op, izq, der)
        else:
            break
    return izq


def parsear_condicion(cur: Cursor) -> NodoAST:
    """condicion → expresion op_rel expresion | condicion ('&'|'|') condicion"""
    izq = parsear_expresion(cur)

    tok = cur.peek()
    if tok and tok[0] == TipoToken.OP_RELACIONAL:
        op = cur.consume()[1]
        der = parsear_expresion(cur)
        nodo = nodo_condicion(op, izq, der)
    else:
        nodo = izq

    while cur.tiene_tokens():
        tok = cur.peek()
        if tok and tok[0] == TipoToken.OP_LOGICO:
            op = cur.consume()[1]
            der = parsear_condicion(cur)
            nodo = nodo_condicion_log(op, nodo, der)
        else:
            break

    return nodo


def parsear_declaracion(cur: Cursor, tipo_dato: str) -> NodoAST:
    """declaracion → tipo ID ';'   |   declaracion_asig → tipo ID '=' expresion ';'"""
    _, nombre, lin, col = cur.esperar(TipoToken.ID)

    tok = cur.peek()
    if tok and tok[0] == TipoToken.OP_ASIGNACION:
        cur.consume()
        expr = parsear_expresion(cur)
        cur.esperar(TipoToken.SIMBOLO_PUNTUACION, ";")
        return NodoDeclaracionAsig(
            tipo=TipoNodo.DECLARACION_ASIG,
            tipo_dato=tipo_dato,
            nombre_id=nombre,
            expresion=expr,
        )

    cur.esperar(TipoToken.SIMBOLO_PUNTUACION, ";")
    return NodoDeclaracion(
        tipo=TipoNodo.DECLARACION,
        tipo_dato=tipo_dato,
        nombre_id=nombre,
    )


def parsear_asignacion(cur: Cursor, nombre_id: str) -> NodoAST:
    """asignacion → ID '=' expresion ';'  (ID ya consumido)"""
    cur.esperar(TipoToken.OP_ASIGNACION, "=")
    expr = parsear_expresion(cur)
    cur.esperar(TipoToken.SIMBOLO_PUNTUACION, ";")
    return NodoAsignacion(tipo=TipoNodo.ASIGNACION, nombre_id=nombre_id, expresion=expr)


def parsear_salida(cur: Cursor) -> NodoAST:
    """salida → 'Mostrar' argumento ';'"""
    tok = cur.peek()
    if tok is None:
        raise ErrorSintactico("Se esperaba argumento para Mostrar.", cur.linea, cur.columna)

    tipo, lexema, lin, col = tok

    if tipo == TipoToken.CADENA:
        cur.consume()
        arg = nodo_literal(TipoNodo.LITERAL_CADENA, lexema)
    elif tipo == TipoToken.ID:
        cur.consume()
        arg = nodo_id(lexema)
    else:
        arg = parsear_expresion(cur)

    cur.esperar(TipoToken.SIMBOLO_PUNTUACION, ";")
    return NodoSalida(tipo=TipoNodo.SALIDA, argumento=arg)


def parsear_entrada(cur: Cursor) -> NodoAST:
    """entrada → 'Capturar' ID ';'"""
    _, nombre, *_ = cur.esperar(TipoToken.ID)
    cur.esperar(TipoToken.SIMBOLO_PUNTUACION, ";")
    return NodoEntrada(tipo=TipoNodo.ENTRADA, nombre_id=nombre)


def parsear_borrar(cur: Cursor) -> NodoAST:
    """borrar → 'Borrar' ID ';'"""
    _, nombre, *_ = cur.esperar(TipoToken.ID)
    cur.esperar(TipoToken.SIMBOLO_PUNTUACION, ";")
    return NodoBorrar(tipo=TipoNodo.BORRAR, nombre_id=nombre)


def parsear_condicional(cur: Cursor) -> NodoAST:
    """condicional → 'Si' condicion 'Entonces' cuerpo ['Sino' cuerpo]"""
    cond = parsear_condicion(cur)
    cur.esperar(TipoToken.PALABRA_RESERVADA, "Entonces")
    cuerpo_entonces = parsear_cuerpo(cur)

    cuerpo_sino = []
    tok = cur.peek()
    if tok and (tok[0], tok[1]) == (TipoToken.PALABRA_RESERVADA, "Sino"):
        cur.consume()
        cuerpo_sino = parsear_cuerpo(cur)

    return NodoCondicional(
        tipo=TipoNodo.CONDICIONAL,
        condicion=cond,
        entonces=cuerpo_entonces,
        sino=cuerpo_sino,
    )


def parsear_bucle(cur: Cursor) -> NodoAST:
    """bucle → 'Mientras' condicion 'Hacer' cuerpo"""
    cond = parsear_condicion(cur)
    cur.esperar(TipoToken.PALABRA_RESERVADA, "Hacer")
    cuerpo = parsear_cuerpo(cur)
    return NodoBucle(tipo=TipoNodo.BUCLE, condicion=cond, cuerpo=cuerpo)


# ---------------------------------------------------------------------------
# Cuerpo y sentencia (núcleo del switch)
# ---------------------------------------------------------------------------

def parsear_sentencia(cur: Cursor) -> NodoAST | None:
    """
    Inspecciona el token actual con match/case y delega al parser correcto.
    Retorna None si el token indica fin de cuerpo.
    """
    if not cur.tiene_tokens():
        return None

    tok = cur.peek()
    if _es_fin_cuerpo(tok):
        return None

    tipo, lexema, lin, col = tok

    match (tipo, lexema):

        # ── Declaración (con o sin asignación inmediata) ──────────────────
        case (TipoToken.PALABRA_RESERVADA, kw) if kw in TIPOS_DATO:
            cur.consume()
            return parsear_declaracion(cur, kw)

        # ── Asignación ────────────────────────────────────────────────────
        case (TipoToken.ID, nombre):
            cur.consume()
            return parsear_asignacion(cur, nombre)

        # ── Salida ────────────────────────────────────────────────────────
        case (TipoToken.PALABRA_RESERVADA, "Mostrar"):
            cur.consume()
            return parsear_salida(cur)

        # ── Entrada ───────────────────────────────────────────────────────
        case (TipoToken.PALABRA_RESERVADA, "Capturar"):
            cur.consume()
            return parsear_entrada(cur)

        # ── Borrar ────────────────────────────────────────────────────────
        case (TipoToken.PALABRA_RESERVADA, "Borrar"):
            cur.consume()
            return parsear_borrar(cur)

        # ── Condicional ───────────────────────────────────────────────────
        case (TipoToken.PALABRA_RESERVADA, "Si"):
            cur.consume()
            return parsear_condicional(cur)

        # ── Bucle ─────────────────────────────────────────────────────────
        case (TipoToken.PALABRA_RESERVADA, "Mientras"):
            cur.consume()
            return parsear_bucle(cur)

        # ── Token no reconocido ───────────────────────────────────────────
        case _:
            raise ErrorSintactico(
                f"Token inesperado al inicio de sentencia: "
                f"{tipo.value!r} ('{lexema}').",
                lin, col
            )


def parsear_cuerpo(cur: Cursor) -> list[NodoAST]:
    """cuerpo → sentencia cuerpo | ε"""
    sentencias = []
    while cur.tiene_tokens() and not _es_fin_cuerpo(cur.peek()):
        nodo = parsear_sentencia(cur)
        if nodo is None:
            break
        sentencias.append(nodo)
    return sentencias


# ---------------------------------------------------------------------------
# Punto de entrada principal
# ---------------------------------------------------------------------------

def analizar_sintaxis(lista_tokens: ListaEnlazadaDobleCircular) -> NodoPrograma:
    """
    Recorre la lista enlazada de tokens y construye el AST del programa.
    programa → 'Inicio' cuerpo 'Final'

    Retorna un NodoPrograma raíz cuyas sentencias son los hijos del árbol.
    """
    if lista_tokens.esta_vacia():
        print("[Sintáctico] Lista de tokens vacía.")
        return NodoPrograma(tipo=TipoNodo.PROGRAMA, sentencias=[])

    cur = Cursor(lista_tokens)
    cur.esperar(TipoToken.PALABRA_RESERVADA, "Inicio")
    sentencias = parsear_cuerpo(cur)
    cur.esperar(TipoToken.PALABRA_RESERVADA, "Final")

    return NodoPrograma(tipo=TipoNodo.PROGRAMA, sentencias=sentencias)

