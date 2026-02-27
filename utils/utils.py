def PreprocesarArchivo(archivo_entrada: str, archivo_salida: str):
    """
    Abre un archivo de texto y elimina:
    - Espacios en blanco innecesarios
    - Líneas vacías
    - Comentarios (// y /* */)
    - Tabuladores
    Guarda el resultado en otro archivo.
    """
    import os

    if not os.path.exists(archivo_entrada):
        raise FileNotFoundError(f"Error: El archivo '{archivo_entrada}' no existe.")

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Eliminar comentarios de bloque /* ... */
    resultado = []
    i = 0
    en_bloque = False
    while i < len(contenido):
        if not en_bloque:
            if i + 1 < len(contenido) and contenido[i] == '/' and contenido[i + 1] == '*':
                en_bloque = True
                i += 2
                continue
            else:
                resultado.append(contenido[i])
                i += 1
        else:
            if i + 1 < len(contenido) and contenido[i] == '*' and contenido[i + 1] == '/':
                en_bloque = False
                i += 2
                continue
            else:
                i += 1

    contenido = ''.join(resultado)

    lineas_limpias = []
    for linea in contenido.split('\n'):
        # Eliminar comentarios de línea //
        idx_comentario = linea.find('//')
        if idx_comentario != -1:
            linea = linea[:idx_comentario]

        # Eliminar tabuladores
        linea = linea.replace('\t', '')

        # Eliminar espacios en blanco al inicio y al final
        linea = linea.strip()

        # Omitir líneas vacías
        if linea == '':
            continue

        lineas_limpias.append(linea)

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas_limpias))

    print(f"Archivo preprocesado guardado en: '{archivo_salida}'")


def RecorrerArchivo(archivo: str):
    """
    Abre un archivo de texto previamente preprocesado y lo recorre
    carácter por carácter, imprimiendo cada uno en pantalla.
    """
    import os

    if not os.path.exists(archivo):
        raise FileNotFoundError(f"Error: El archivo '{archivo}' no existe.")

    with open(archivo, 'r', encoding='utf-8') as f:
        while True:
            caracter = f.read(1)
            if not caracter:
                break
            print(caracter, end='')

    print()  # Salto de línea al final
