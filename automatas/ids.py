def validar_id(cadena: str) -> bool:
    """
    Valida si una cadena es un identificador válido.

    Reglas:
    - Debe iniciar con una letra (a-z, A-Z).
    - Puede contener una secuencia arbitraria de letras, dígitos y/o guion bajo.

    Retorna True si es válido, False en caso contrario.
    """
    if not cadena:
        return False
        
    first_char = cadena[0]
    if not (('a' <= first_char <= 'z') or ('A' <= first_char <= 'Z')):
        return False
        
    for char in cadena[1:]:
        es_letra = ('a' <= char <= 'z') or ('A' <= char <= 'Z')
        es_digito = ('0' <= char <= '9')
        es_guion_bajo = (char == '_')
        
        if not (es_letra or es_digito or es_guion_bajo):
            return False
            
    return True