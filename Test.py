import argparse

# Crear un objeto ArgumentParser
parser = argparse.ArgumentParser(description="Descripción de tu programa")

# Definir los argumentos esperados
parser.add_argument('-Mode', type=int, help='Modo de operación', required=True)

 # Parsear los argumentos
args = parser.parse_args()

  # Acceder al valor del parámetro Mode
mode = args.Mode

   # Realizar alguna acción basada en el valor de 'mode'
if mode == 1:
    print("Modo 1 seleccionado")
else:
    print(f"Modo {mode} seleccionado")
