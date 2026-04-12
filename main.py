from utils.utils import PreprocesarArchivo
from analizador_lexico import analizar_archivo
from structs.lista_enlazada import ListaEnlazadaDobleCircular
import sys
import os
import argparse

ARCHIVO_TEMPORAL = "temp_codigo_limpio.txt"


def preprocesar(archivo_entrada: str) -> str:
    """
    Limpia y preprocesa el archivo fuente.
    Retorna la ruta del archivo limpio generado.
    Termina el programa si el archivo no existe o hay un error.
    """
    if not os.path.exists(archivo_entrada):
        print(f"Error: No se encontró el archivo '{archivo_entrada}'.")
        sys.exit(1)

    print("[Etapa 1] Preprocesamiento")
    try:
        PreprocesarArchivo(archivo_entrada, ARCHIVO_TEMPORAL)
        print(f"  Archivo preprocesado guardado en: '{ARCHIVO_TEMPORAL}'")
    except Exception as e:
        print(f"  Error durante el preprocesamiento: {e}")
        sys.exit(1)

    return ARCHIVO_TEMPORAL


def analizar_lexico(archivo_limpio: str) -> ListaEnlazadaDobleCircular:
    """
    Ejecuta el análisis léxico sobre el archivo preprocesado.
    Retorna la lista enlazada con todos los tokens encontrados.
    """
    print("\n[Etapa 2] Análisis Léxico")
    lista_tokens = analizar_archivo(archivo_limpio)

    print(f"\n[Resumen] {len(lista_tokens)} token(s) almacenados en la lista enlazada.")
    print("[Lista de tokens (en orden)]:")
    for tipo, lexema in lista_tokens.mostrar_adelante():
        print(f"  ({tipo.value}, '{lexema}')")

    return lista_tokens


def limpiar_temporales():
    """Elimina archivos temporales generados durante el proceso."""
    if os.path.exists(ARCHIVO_TEMPORAL):
        os.remove(ARCHIVO_TEMPORAL)
        print("\n[*] Archivos temporales eliminados.")


def main():
    """
    Punto de entrada principal del compilador.
    Orquesta las etapas: preprocesamiento → análisis léxico.
    """
    parser = argparse.ArgumentParser(description='Mini Compilador - Analizador Léxico')
    parser.add_argument('archivo', nargs='?', default='prueba.txt',
                        help='Ruta al archivo de código fuente a analizar')
    args = parser.parse_args()

    archivo_limpio = preprocesar(args.archivo)
    analizar_lexico(archivo_limpio)
    limpiar_temporales()


if __name__ == "__main__":
    main()
