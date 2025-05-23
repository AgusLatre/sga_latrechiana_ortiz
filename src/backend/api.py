import pandas as pd

def readCSVFile(filePath):
    try:
        data = pd.read_csv(filePath)
        studentsArrays = data.values.tolist()
        return studentsArrays
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
        return None

def validateNotas(studentsArrays):
    errors = []
    for i, student in enumerate(studentsArrays):
        for j in range(2, 5):
            try:
                student[j] = float(student[j])
                if not 0 <= student[j] <= 10:
                    errors.append((i, j, "Nota fuera de rango"))
            except ValueError:
                errors.append((i, j, "Nota no numérica"))
    return studentsArrays, errors

def calculateNotaFinal(studentsArrays):
    for student in studentsArrays:
        nota1 = float(student[2])
        nota2 = float(student[3])
        nota3 = float(student[4])
        nota_final = round((nota1 + nota2 + nota3) / 3, 2)
        if len(student) < 6:
            student.append(nota_final)
        else:
            student[5] = nota_final
    return studentsArrays

def listaCompleta(studentsArrays):
    return [
        {
            "Nombre": student[0],
            "Legajo": student[1],
            "Nota1": student[2],
            "Nota2": student[3],
            "Nota3": student[4],
            "Promedio": student[5]
        }
        for student in studentsArrays
    ]

def promedioPorMateria(studentsArrays):
    nota1_sum = sum(float(student[2]) for student in studentsArrays)
    nota2_sum = sum(float(student[3]) for student in studentsArrays)
    nota3_sum = sum(float(student[4]) for student in studentsArrays)
    count = len(studentsArrays)
    return {
        "Materia 1": round(nota1_sum / count, 2),
        "Materia 2": round(nota2_sum / count, 2),
        "Materia 3": round(nota3_sum / count, 2)
    }

def mostrarAlumnosPorEncimaDelUmbral(studentsArrays, threshold):
    return [
        {
            "Nombre": student[0],
            "Legajo": student[1],
            "Notas": [student[2], student[3], student[4]],
            "Promedio": student[5]
        }
        for student in studentsArrays if student[5] > threshold
    ]

def mostrarAlumnosDesaprobados(studentsArrays):
    return [
        {
            "Nombre": student[0],
            "Legajo": student[1],
            "Notas": [student[2], student[3], student[4]],
            "Promedio": student[5]
        }
        for student in studentsArrays if any(float(n) < 4 for n in student[2:5])
    ]

def calcularAprobadosDesaprobados(studentsArrays):
    aprobados = sum(1 for student in studentsArrays if student[5] >= 4)
    desaprobados = len(studentsArrays) - aprobados
    return {"Aprobados": aprobados, "Desaprobados": desaprobados}
