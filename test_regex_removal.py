from utils.utils import PreprocesarArchivo
import os

with open("test_input.txt", "w", encoding="utf-8") as f:
    f.write('''Entero     variable_1   =    10 ;
Si ( variable_1  >   5 )  {
    Mostrar  "Hola mundo" ; 
    // comentario     1  2   
}
/* bla 
   bla */
Entero variable_2=  20;
''')

PreprocesarArchivo("test_input.txt", "test_output.txt")

print("\n--- Resultado: ---")
with open("test_output.txt", "r", encoding="utf-8") as f:
    print(f.read())
print("------------------\n")

# Limpieza
if os.path.exists("test_input.txt"): os.remove("test_input.txt")
if os.path.exists("test_output.txt"): os.remove("test_output.txt")
