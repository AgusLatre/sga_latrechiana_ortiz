import pandas as pd

def readCSVFile(filePath):
    try:
        data = pd.read_csv(filePath)
        studentsArrays = data.values.tolist()
        columns = list(data.columns)
        return studentsArrays, columns
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
        return None, None

def validateNotas(studentsArrays):
    errors = []
    for i, student in enumerate(studentsArrays):
        for j in range(2, 5):
            try:
                nota = float(student[j])
                if not 0 <= nota <= 10:
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

def promedioPorMateria(studentsArrays, materias=None):
    if materias is None:
        materias = ["Materia 1", "Materia 2", "Materia 3"]
    promedios = {}
    for idx, materia in enumerate(materias, start=2):
        suma = sum(float(student[idx]) for student in studentsArrays)
        promedios[materia] = round(suma / len(studentsArrays), 2)
    return promedios

def mostrarAlumnosPorEncimaDelUmbral(studentsArrays, threshold):
    return [
        {
            "Nombre": student[0],
            "Legajo": student[1],
            "Notas": [student[2], student[3], student[4]],
            "Promedio": round((float(student[2]) + float(student[3]) + float(student[4])) / 3, 2)
        }
        for student in studentsArrays
        if (float(student[2]) + float(student[3]) + float(student[4])) / 3 > threshold
    ]

def mostrarAlumnosDesaprobados(studentsArrays):
    return [
        {
            "Nombre": student[0],
            "Legajo": student[1],
            "Notas": [student[2], student[3], student[4]],
            "Promedio": round((float(student[2]) + float(student[3]) + float(student[4])) / 3, 2)
        }
        for student in studentsArrays
        if any(float(n) < 4 for n in student[2:5])
    ]

def calcularAprobadosDesaprobados(studentsArrays):
    aprobados = sum(
        1 for student in studentsArrays
        if (float(student[2]) + float(student[3]) + float(student[4])) / 3 >= 4
    )
    desaprobados = len(studentsArrays) - aprobados
    return {"Aprobados": aprobados, "Desaprobados": desaprobados}
