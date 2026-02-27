def validar_cadena(cadena: str) -> bool:
    """
    Valida si un texto es una cadena válida.

    Reglas:
    - Debe iniciar y terminar con comillas dobles (").
    - Puede contener una secuencia de letras, dígitos y ciertos caracteres especiales 
      como: (, ), ;, _, ,, ., :

    Retorna True si es válido, False en caso contrario.
    """
    if not cadena or len(cadena) < 2:
        return False
        
    if cadena[0] != '"' or cadena[-1] != '"':
        return False
        
    caracteres_especiales = {'(', ')', ';', '_', ',', '.', ':'}
    
    for char in cadena[1:-1]:
        es_letra = ('a' <= char <= 'z') or ('A' <= char <= 'Z')
        es_digito = ('0' <= char <= '9')
        es_especial = char in caracteres_especiales
        
        if not (es_letra or es_digito or es_especial):
            return False
            
    return True
