from constants.palabras_reservadas import PALABRAS_RESERVADAS

def validar_palabra_reservada(cadena: str) -> bool:
    """
    Valida si una cadena es exactamente una de las palabras reservadas definidas.
    """
    return cadena in PALABRAS_RESERVADAS
