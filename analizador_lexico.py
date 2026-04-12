from constants.tipos_token import TipoToken
from constants.operators import Operador
from automatas.numeros import validar_numero, validar_numero_real
from automatas.ids import validar_id
from automatas.palabras_reservadas import validar_palabra_reservada
import os

def clasificar_token(lexema: str) -> TipoToken:
    """Clasifica un lexema alfanumérico en Palabra Reservada, ID o Número"""
    if validar_palabra_reservada(lexema):
        return TipoToken.PALABRA_RESERVADA
    if validar_numero(lexema):
        return TipoToken.NUMERO_ENTERO
    if validar_numero_real(lexema):
        return TipoToken.NUMERO_REAL
    if validar_id(lexema):
        return TipoToken.ID
    return TipoToken.ERROR

def clasificar_operador(op_str: str) -> TipoToken:
    """Clasifica un operador en su categoría correspondiente (Aritmético, Relacional, etc)"""
    if op_str in ("+", "-", "*", "/", "**"):
        return TipoToken.OP_ARITMETICO
    elif op_str in ("<", ">", "<=", ">=", "==", "!="):
        return TipoToken.OP_RELACIONAL
    elif op_str in ("&", "|"):
        return TipoToken.OP_LOGICO
    elif op_str == "=":
        return TipoToken.OP_ASIGNACION
    return TipoToken.ERROR

def analizar_archivo(archivo: str):
    """
    Lee un archivo preprocesado carácter por carácter,
    agrupa los lexemas y los clasifica usando constantes y autómatas.
    """
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        return

    print(f"Iniciando análisis léxico de '{archivo}'...\n")

    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    i = 0
    while i < len(contenido):
        c = contenido[i]

        # 1. Ignorar espacios en blanco
        if c.isspace():
            i += 1
            continue

        # 2. Cadenas de texto
        if c == '"':
            buffer = c
            i += 1
            while i < len(contenido) and contenido[i] != '"':
                buffer += contenido[i]
                i += 1
            if i < len(contenido):
                buffer += contenido[i] # Agregar la comilla de cierre
                i += 1
            print(f"[{TipoToken.CADENA.value}] -> {buffer}")
            continue

        # 3. Símbolos de Agrupación y Puntuación
        if c in '({[':
            print(f"[{TipoToken.SIMBOLO_APERTURA.value}] -> {c}")
            i += 1
            continue
        if c in ')}]':
            print(f"[{TipoToken.SIMBOLO_CIERRE.value}] -> {c}")
            i += 1
            continue
        if c in ';,.:':
            print(f"[{TipoToken.SIMBOLO_PUNTUACION.value}] -> {c}")
            i += 1
            continue

        # 4. Operadores (pueden ser de 1 o 2 caracteres)
        if c in '+-*/<>=!&|':
            op_str = c
            
            # Verificar si el siguiente caracter forma un operador compuesto (ej. >=, ==, **)
            if i + 1 < len(contenido):
                c_next = contenido[i+1]
                op_doble = c + c_next
                # Validamos si es una combinación válida iterando sobre los valores posibles
                es_valido = any(op_doble == op.value for op in Operador) or op_doble == "="
                
                # Excepción especial para asignación u operadores que falten en el Enum
                if op_doble == "==" or op_doble == "!=" or op_doble == "<=" or op_doble == ">=" or op_doble == "**":
                    es_valido = True

                if es_valido:
                    op_str = op_doble
                    i += 1

            tipo_op = clasificar_operador(op_str)
            print(f"[{tipo_op.value}] -> {op_str}")
            i += 1
            continue

        # 5. Palabras Reservadas, IDs, Números
        if c.isalnum() or c == '_':
            buffer = ""
            
            # Repetir lectura hasta encontrar un delimitador que parezca de otro tipo
            while i < len(contenido):
                cc = contenido[i]
                # Los delimitadores incluyen espacios, simbolos especiales y operadores
                if cc.isspace() or cc in '({[ ]});,.:"'+'+-*/<>=!&|':
                    # Permitir puntos solo si estamos ante un número real (ej. 3.14)
                    if cc == '.' and buffer.isdigit() and (i + 1 < len(contenido) and contenido[i+1].isdigit()):
                        buffer += cc
                        i += 1
                        continue
                    break # Salir si encontramos el delimitador real
                
                buffer += cc
                i += 1
            
            tipo = clasificar_token(buffer)
            print(f"[{tipo.value}] -> {buffer}")
            continue

        # 6. Cualquier otro carácter no reconocido será tratado como error
        print(f"[{TipoToken.ERROR.value}] -> {c}")
        i += 1
    
    print("Análisis léxico finalizado.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        analizar_archivo(sys.argv[1])
    else:
        print("Uso: python3 analizador_lexico.py <archivo_preprocesado>")
