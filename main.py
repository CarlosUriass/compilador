from utils.utils import PreprocesarArchivo
from analizador_lexico import analizar_archivo
import sys
import os

def main():
    """
    Script principal para probar el analizador léxico.
    Toma un archivo de texto como entrada, lo limpia (preprocesa),
    y luego ejecuta el analizador léxico sobre el resultado.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Analizador Léxico')
    parser.add_argument('archivo', nargs='?', default='prueba.txt', 
                      help='Ruta al archivo de código fuente a analizar')
    
    args = parser.parse_args()
    archivo_entrada = args.archivo
    archivo_limpio = "temp_codigo_limpio.txt"

    if not os.path.exists(archivo_entrada):
        print(f"Error: No se encontró el archivo '{archivo_entrada}'.")
        sys.exit(1)

    print(f"[Etapa de Preprocesamiento")
    try:
        PreprocesarArchivo(archivo_entrada, archivo_limpio)
        
    except Exception as e:
        print(f"Error durante el preprocesamiento: {e}")
        sys.exit(1)

    print(f"[Etapa de Análisis Léxico")
    analizar_archivo(archivo_limpio)

    if os.path.exists(archivo_limpio): 
        os.remove(archivo_limpio)
        print("\n[*] Archivos temporales eliminados.")

if __name__ == "__main__":
    main()
