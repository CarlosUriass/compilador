from constants.tipos_token import TipoToken
from constants.operators import Operador
from automatas.numeros import validar_numero, validar_numero_real
from automatas.ids import validar_id
from automatas.palabras_reservadas import validar_palabra_reservada
from structs.lista_enlazada import ListaEnlazadaDobleCircular
import os


def clasificar_token(lexema: str) -> TipoToken:
    """Clasifica un lexema alfanumérico en Palabra Reservada, ID o Número"""
    if validar_palabra_reservada(lexema):
        return TipoToken.PALABRA_RESERVADA
    if validar_numero_real(lexema):
        return TipoToken.NUMERO_REAL
    if validar_numero(lexema):
        return TipoToken.NUMERO_ENTERO
    if validar_id(lexema):
        return TipoToken.ID
    return TipoToken.ERROR


def clasificar_operador(op_str: str) -> TipoToken:
    """Clasifica un operador en su categoría correspondiente"""
    if op_str in ("+", "-", "*", "/", "**"):
        return TipoToken.OP_ARITMETICO
    elif op_str in ("<", ">", "<=", ">=", "==", "!="):
        return TipoToken.OP_RELACIONAL
    elif op_str in ("&", "|"):
        return TipoToken.OP_LOGICO
    elif op_str == "=":
        return TipoToken.OP_ASIGNACION
    return TipoToken.ERROR


def analizar_archivo(archivo: str) -> ListaEnlazadaDobleCircular:
    """
    Lee un archivo preprocesado carácter por carácter, agrupa los lexemas,
    los clasifica y los almacena en una ListaEnlazadaDobleCircular de tuplas
    (TipoToken, lexema, linea, columna).
    Retorna la lista con todos los tokens encontrados.
    """
    lista_tokens = ListaEnlazadaDobleCircular()

    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        return lista_tokens

    print(f"Iniciando análisis léxico de '{archivo}'...\n")

    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    def registrar(tipo: TipoToken, lexema: str, linea: int, columna: int):
        """Imprime el token y lo inserta al final de la lista enlazada."""
        print(f"[{tipo.value}] -> {lexema}")
        lista_tokens.insertar_final((tipo, lexema, linea, columna))

    # Rastreo de posición
    linea = 1
    ultima_newline = -1  # índice del último '\n' visto (-1 = antes del inicio)

    i = 0
    while i < len(contenido):
        c = contenido[i]

        # 1. Ignorar espacios en blanco (rastrear saltos de línea)
        if c.isspace():
            if c == '\n':
                linea += 1
                ultima_newline = i
            i += 1
            continue

        # Capturar posición del primer carácter del token actual
        tok_lin = linea
        tok_col = i - ultima_newline   # columna 1-indexada

        # 2. Cadenas de texto
        if c == '"':
            buffer = c
            i += 1
            while i < len(contenido) and contenido[i] != '"':
                buffer += contenido[i]
                i += 1
            if i < len(contenido):
                buffer += contenido[i]
                i += 1
            registrar(TipoToken.CADENA, buffer, tok_lin, tok_col)
            continue

        # 3. Símbolos de Agrupación y Puntuación
        if c in '({[':
            registrar(TipoToken.SIMBOLO_APERTURA, c, tok_lin, tok_col)
            i += 1
            continue
        if c in ')}]':
            registrar(TipoToken.SIMBOLO_CIERRE, c, tok_lin, tok_col)
            i += 1
            continue
        # El '.' puede ser puntuación O inicio de número real (.50)
        if c == '.':
            if i + 1 < len(contenido) and contenido[i + 1].isdigit():
                buffer = "."
                i += 1
                while i < len(contenido) and contenido[i].isdigit():
                    buffer += contenido[i]
                    i += 1
                registrar(clasificar_token(buffer), buffer, tok_lin, tok_col)
                continue
            registrar(TipoToken.SIMBOLO_PUNTUACION, c, tok_lin, tok_col)
            i += 1
            continue
        if c in ';,:':
            registrar(TipoToken.SIMBOLO_PUNTUACION, c, tok_lin, tok_col)
            i += 1
            continue

        # 4. Operadores (1 o 2 caracteres)
        if c in '+-*/<>=!&|':
            op_str = c
            if i + 1 < len(contenido):
                c_next = contenido[i + 1]
                op_doble = c + c_next
                es_valido = any(op_doble == op.value for op in Operador) or op_doble == "="
                if op_doble in ("==", "!=", "<=", ">=", "**"):
                    es_valido = True
                if es_valido:
                    op_str = op_doble
                    i += 1
            registrar(clasificar_operador(op_str), op_str, tok_lin, tok_col)
            i += 1
            continue

        # 5. Palabras Reservadas, IDs, Números
        if c.isalnum() or c == '_':
            buffer = ""
            while i < len(contenido):
                cc = contenido[i]
                if cc.isspace() or cc in '({[ ]});,.:\"' + '+-*/<>=!&|':
                    if cc == '.' and buffer.isdigit() and (i + 1 < len(contenido) and contenido[i + 1].isdigit()):
                        buffer += cc
                        i += 1
                        continue
                    break
                buffer += cc
                i += 1
            registrar(clasificar_token(buffer), buffer, tok_lin, tok_col)
            continue

        # 6. Carácter no reconocido → ERROR
        registrar(TipoToken.ERROR, c, tok_lin, tok_col)
        i += 1

    print("Análisis léxico finalizado.")
    return lista_tokens


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        analizar_archivo(sys.argv[1])
    else:
        print("Uso: python3 analizador_lexico.py <archivo_preprocesado>")
