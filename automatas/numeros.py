def validar_numero(cadena: str) -> bool:
    """
    Valida si una cadena es un número entero válido.

    Reglas:
    - Debe iniciar con un dígito.
    - Puede contener una secuencia arbitraria de dígitos.

    Retorna True si es válido, False en caso contrario.
    """
    if not cadena:
        return False
    
    for char in cadena:
        if not ('0' <= char <= '9'):
            return False
            
    return True

def validar_numero_real(cadena: str) -> bool:
    """
    Valida si una cadena es un número real válido.

    Reglas:
    - Debe iniciar con un dígito (uno o más).
    - Debe seguir con un punto.
    - Debe seguir con un dígito (uno o más).

    Retorna True si es válido, False en caso contrario.
    """
    if not cadena:
        return False
        
    if '.' not in cadena:
        return False
        
    partes = cadena.split('.')
    if len(partes) != 2:
        return False
        
    entera, decimal = partes
    
    if not entera or not decimal:
        return False
        
    for char in entera:
        if not ('0' <= char <= '9'):
            return False
            
    for char in decimal:
        if not ('0' <= char <= '9'):
            return False
            
    return True
