import csv
import random

# Nombre del archivo CSV
filename = 'nmil.csv'

# Generar números aleatorios del 1 al 1000
numeros_aleatorios = [random.randint(1, 900) for _ in range(900)]

# Escribir los números en el archivo CSV
try:
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escribir los números en una sola columna
        for numero in numeros_aleatorios:
            writer.writerow([numero])
    print(f"Archivo CSV '{filename}' generado exitosamente con 900 números aleatorios del 1 al 1000.")
except IOError as e:
    print(f"Error al escribir el archivo CSV: {e}")