import os

def PreprocesarArchivo(archivo_entrada: str, archivo_salida: str):
    """
    Abre un archivo de texto y elimina:
    - Comentarios de bloque (/* */) y de línea (//)
    - Tabuladores
    - Espacios en blanco innecesarios (se conservan espacios dentro de cadenas y 
      entre palabras/números cuando es estrictamente necesario)
    - Líneas vacías
    Guarda el resultado en otro archivo.
    """
    if not os.path.exists(archivo_entrada):
        raise FileNotFoundError(f"Error: El archivo '{archivo_entrada}' no existe.")

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # 1. Eliminar comentarios de bloque /* ... */ 
    # Sustituimos por un espacio para evitar unir tokens erróneamente en caso de "A/*comentario*/B"
    resultado_sin_bloques = []
    i = 0
    while i < len(contenido):
        if i + 1 < len(contenido) and contenido[i] == '/' and contenido[i + 1] == '*':
            # Entramos a comentario de bloque
            i += 2
            while i < len(contenido) and not (i + 1 < len(contenido) and contenido[i] == '*' and contenido[i + 1] == '/'):
                i += 1
            i += 2 # Saltar el */
            resultado_sin_bloques.append(' ') # Dejar un espacio representativo
        else:
            resultado_sin_bloques.append(contenido[i])
            i += 1

    contenido = "".join(resultado_sin_bloques)

    # Helper para saber si un carácter forma parte de una "palabra" o número
    def es_alfanumerico(c):
        return c.isalnum() or c == '_'

    # 2. Procesamos línea por línea para quitar comentarios de línea // y limpiar espacios
    lineas_limpias = []
    
    for linea in contenido.split('\n'):
        # Quitar comentarios de línea (ignorando los que pudiesen estar dentro de cadenas)
        res_linea = []
        en_cadena = False
        k = 0
        while k < len(linea):
            c = linea[k]
            if c == '"':
                en_cadena = not en_cadena
                res_linea.append(c)
                k += 1
                continue
            
            # Si vemos // y no estamos en una cadena, ignoramos el resto de la línea
            if not en_cadena and k + 1 < len(linea) and c == '/' and linea[k + 1] == '/':
                break 
                
            res_linea.append(c)
            k += 1
            
        codigo_linea = "".join(res_linea)
        
        # 3. Limpiar espacios redundantes en codigo_linea
        final_linea = []
        en_cadena = False
        k = 0
        while k < len(codigo_linea):
            c = codigo_linea[k]
            if c == '"':
                en_cadena = not en_cadena
                final_linea.append(c)
                k += 1
                continue
                
            if en_cadena:
                final_linea.append(c)
                k += 1
                continue
                
            # Tratar cualquier espacio/tab como potencial candidato a ser borrado
            if c in (' ', '\t', '\r'):
                # buscar el siguiente char que NO sea espacio
                nxt = k + 1
                while nxt < len(codigo_linea) and codigo_linea[nxt] in (' ', '\t', '\r'):
                    nxt += 1
                    
                if nxt < len(codigo_linea):
                    next_char = codigo_linea[nxt]
                    prev_char = final_linea[-1] if final_linea else ''
                    
                    # Solo insertamos un espacio real si el caracter anterior es alfanumérico 
                    # Y el caracter siguiente también lo es (ej: "Entero variable").
                    # Si alguno es un símbolo (ej: "=", "(", ">"), no necesitamos el espacio.
                    if prev_char and es_alfanumerico(prev_char) and es_alfanumerico(next_char):
                        final_linea.append(' ')
                        
                k = nxt
                continue
                
            final_linea.append(c)
            k += 1
            
        linea_str = "".join(final_linea).strip()
        if linea_str:
            lineas_limpias.append(linea_str)

    # 4. Escribir archivo de salida
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas_limpias))

    print(f"Archivo preprocesado guardado en: '{archivo_salida}'")


def RecorrerArchivo(archivo: str):
    """
    Abre un archivo de texto previamente preprocesado y lo recorre
    carácter por carácter, imprimiendo cada uno en pantalla.
    """
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"Error: El archivo '{archivo}' no existe.")

    with open(archivo, 'r', encoding='utf-8') as f:
        while True:
            caracter = f.read(1)
            if not caracter:
                break
            print(caracter, end='')

    print()  # Salto de línea al final
