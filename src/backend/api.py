import pandas as pd
import json 

def readCSVFile(filePath):
    try:
        data = pd.read_csv(filePath)
        studentsArrays = data.values.tolist()
        return studentsArrays
    except FileNotFoundError:
        print(f"Archivo no encontrado: {filePath}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Archivo vacio: {filePath}")
        return None
    except pd.errors.ParserError:
        print(f"Error parseando el archivo: {filePath}")
        return None

def validateNotas(studentsArrays):
    for i, student in enumerate(studentsArrays):
        while True:
            try:
                nota1 = float(student[2])
                nota2 = float(student[3])
                nota3 = float(student[4])
                if nota1 < 0 or nota1 > 10 or nota2 < 0 or nota2 > 10 or nota3 < 0 or nota3 > 10:
                    print(f"Error en la nota de {student[0]} en {student[1]}. Nota debe ser entre 0 y 10.")
                    student[2] = float(input("Ingrese la nota 1 correcta: "))
                    student[3] = float(input("Ingrese la nota 2 correcta: "))
                    student[4] = float(input("Ingrese la nota 3 correcta: "))
                else:
                    break
            except ValueError:
                print(f"Error en la nota de {student[0]} en {student[1]}. Nota debe ser un número.")
                student[2] = float(input("Ingrese la nota 1 correcta: "))
                student[3] = float(input("Ingrese la nota 2 correcta: "))
                student[4] = float(input("Ingrese la nota 3 correcta: "))
    return studentsArrays

def calculateNotaFinal(studentsArrays):
    for student in studentsArrays:
        nota1 = float(student[2])
        nota2 = float(student[3])
        nota3 = float(student[4])
        nota_final = (nota1 + nota2 + nota3) / 3
        student[5] = nota_final
    return studentsArrays



def listaCompleta(studentsArrays):
    """
    Mostrar el Listado completo de alumnos con sus notas y promedio.
    """
    print("Listado completo de alumnos:")
    for student in studentsArrays:
        print(f"Nombre: {student[0]}, Notas: {student[2]}, {student[3]}, {student[4]}, Promedio: {student[5]}")
    return studentsArrays

def promedioPorMateria(studentsArrays):
    """
    Mostrar el Promedio general por materia.
    """
    nota1_sum = sum(float(student[2]) for student in studentsArrays)
    nota2_sum = sum(float(student[3]) for student in studentsArrays)
    nota3_sum = sum(float(student[4]) for student in studentsArrays)
    nota1_avg = nota1_sum / len(studentsArrays)
    nota2_avg = nota2_sum / len(studentsArrays)
    nota3_avg = nota3_sum / len(studentsArrays)
    print("Promedio general por materia:")
    print(f"Materia 1: {nota1_avg}, Materia 2: {nota2_avg}, Materia 3: {nota3_avg}")
    return {"Materia 1": nota1_avg, "Materia 2": nota2_avg, "Materia 3": nota3_avg}

def mostrarAlumnosPorEncimaDelUmbral(studentsArrays, threshold):
    """
    Mostrar todos los Alumnos con nota final mayor a un valor dado.
    """
    students_with_high_final_grade = [student for student in studentsArrays if student[5] > threshold]
    print("Alumnos con nota final mayor a", threshold)
    for student in students_with_high_final_grade:
        print(f"Nombre: {student[0]}, Notas: {student[2]}, {student[3]}, {student[4]}, Promedio: {student[5]}")
    return students_with_high_final_grade

def mostrarAlumnosDesaprobados(studentsArrays):
    """
    Mostrar todos los Alumnos con al menos una nota menor a 4.
    """
    students_with_low_note = [student for student in studentsArrays if float(student[2]) < 4 or float(student[3]) < 4 or float(student[4]) < 4]
    print("Alumnos con al menos una nota menor a 4")
    for student in students_with_low_note:
        print(f"Nombre: {student[0]}, Notas: {student[2]}, {student[3]}, {student[4]}, Promedio: {student[5]}")
    return students_with_low_note

def calcularAprobadosDesaprobados(studentsArrays):
    """
    Calcular Cantidad de aprobados y desaprobados por materia.
    """
    approved = sum(1 for student in studentsArrays if student[5] >= 4)
    disapproved = len(studentsArrays) - approved
    print("Cantidad de aprobados y desaprobados:")
    print(f"Aprobados: {approved}, Desaprobados: {disapproved}")
    return {"Aprobados": approved, "Desaprobados": disapproved}

# Example usage:
studentsArrays = [
    ["Juan", "123", 5, 4, 3, 4],
    ["Maria", "456", 4, 5, 4, 4.33],
    ["Pedro", "789", 3, 3, 3, 3],
    ["Ana", "101", 5, 5, 5, 5]
]

# Save results to JSON file
with open('results.json', 'w') as f:
    json.dump({
        "ListaCompleta": listaCompleta(studentsArrays),
        "PromedioPorMateria": promedioPorMateria(studentsArrays),
        "AlumnosPorEncimaDelUmbral": mostrarAlumnosPorEncimaDelUmbral(studentsArrays, 6),
        "AlumnosDesaprobados": mostrarAlumnosDesaprobados(studentsArrays),
        "Aprobados/Desaprobados": calcularAprobadosDesaprobados(studentsArrays)
    }, f, indent=4)


# Algo asi mete en el frontend @Nacho
# filePath = 'students.csv'
# studentsArrays = readCSVFile(filePath)
# studentsArrays = validateNotas(studentsArrays)
# studentsArrays = calculateNotaFinal(studentsArrays)
# print(studentsArrays)
