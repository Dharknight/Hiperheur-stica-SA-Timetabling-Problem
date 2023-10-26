import csv
#from heuristicas import *  # Importa todas las funciones de heuristicas.py

datos = []

def data():
    with open('datos.csv', newline='', encoding='iso-8859-1') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        for fila in lector_csv:
            semestre = int(fila['Semestre'])
            asignaturas = []
            for i in range(1, 6):  # Lee hasta 5 asignaturas
                asignatura = fila[f'Asignatura {i}']
                if asignatura:  # Asegúrate de que la asignatura no esté vacía
                    asignaturas.append(asignatura)
            datos.append({'Asignaturas': asignaturas})
            #print(asignaturas)
            #datos={'Semestre':semestre,'Asignaturas': asignaturas}
        #print(datos)
    return datos
