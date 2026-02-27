from constants.palabras_reservadas import PalabraReservada

def validar_palabra_reservada(cadena: str) -> bool:
    """
    Valida si una cadena es exactamente una de las palabras reservadas definidas.
    """
    try:
        PalabraReservada(cadena)
        return True
    except ValueError:
        return False
