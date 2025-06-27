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
                else:
                    student[j] = nota
            except (ValueError, IndexError):
                errors.append((i, j, "Nota no numérica"))
    return studentsArrays, errors

def calculateNotaFinal(studentsArrays):
    for student in studentsArrays:
        try:
            nota1 = float(student[2])
            nota2 = float(student[3])
            nota3 = float(student[4])
            nota_final = round((nota1 + nota2 + nota3) / 3, 2)
            if len(student) < 6:
                student.append(nota_final)
            else:
                student[5] = nota_final
        except (ValueError, IndexError):
            if len(student) < 6:
                student.append("Error")
            else:
                student[5] = "Error"
    return studentsArrays

def listaCompleta(studentsArrays):
    return [
        {
            "Nombre": student[0],
            "Materia": student[1],
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
        try:
            suma = sum(float(student[idx]) for student in studentsArrays)
            promedios[materia] = round(suma / len(studentsArrays), 2)
        except (ValueError, IndexError):
            promedios[materia] = "Error"
    return promedios

def mostrarAlumnosPorEncimaDelUmbral(studentsArrays, threshold):
    return [
        {
            "Nombre": student[0],
            "Materia": student[1],
            "Notas": [student[2], student[3], student[4]],
            "Promedio": round((float(student[2]) + float(student[3]) + float(student[4])) / 3, 2)
        }
        for student in studentsArrays
        if all(isinstance(student[i], (int, float)) for i in range(2, 5))
        and (float(student[2]) + float(student[3]) + float(student[4])) / 3 > threshold
    ]

def mostrarAlumnosDesaprobados(studentsArrays):
    return [
        {
            "Nombre": student[0],
            "Materi": student[1],
            "Notas": [student[2], student[3], student[4]],
            "Promedio": round((float(student[2]) + float(student[3]) + float(student[4])) / 3, 2)
        }
        for student in studentsArrays
        if any(isinstance(student[i], (int, float)) and float(student[i]) < 4 for i in range(2, 5))
    ]

def calcularAprobadosDesaprobados(studentsArrays):
    aprobados = sum(
        1 for student in studentsArrays
        if len(student) >= 6 and isinstance(student[5], (int, float)) and student[5] >= 4
    )
    desaprobados = len(studentsArrays) - aprobados
    return {"Aprobados": aprobados, "Desaprobados": desaprobados}
