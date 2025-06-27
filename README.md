Sistema de Gestión de Notas con Interfaz Gráfica (Tkinter)
==================================================

Aplicación de escritorio en Python para gestionar, editar, validar y exportar calificaciones de estudiantes desde archivos CSV o ingresándolas manualmente.

Características
------------------

*   Cargar datos desde archivo CSV
    
*   Agregar nuevos alumnos manualmente
    
*   Validar que las notas estén en el rango \[0–10\]
    
*   Calcular automáticamente el promedio final (nota final)
    
*   Editar datos con doble clic
    
*   Reportes:
    
    *   Promedio por materia
        
    *   Alumnos con promedio > 6
        
    *   Alumnos desaprobados
        
    *   Estadísticas de aprobados/desaprobados
        
*   Descargar archivo CSV generado
    
*   Ordenamiento ascendente/descendente por columna con íconos ↑ ↓
    


Cómo ejecutar
----------------

```
cd src
python3 -m frontend.view 
```

> Requiere Python 3.7+ y pandas.

Formato del CSV
------------------

Debe contener las siguientes columnas (sin encabezado obligatorio):

` Nombre, Materia, Nota1, Nota2, Nota3   `

La nota final se calculará automáticamente al cargar el archivo.

Lógica del backend (api.py)
------------------------------

### readCSVFile(filePath)

Lee el CSV con pandas y devuelve una lista de listas.

### validateNotas(studentsArrays)

Convierte los campos de notas a float y verifica que estén entre 0 y 10.

### calculateNotaFinal(studentsArrays)

Calcula el promedio de Nota1, Nota2 y Nota3. Agrega o actualiza el campo "Promedio" como un float redondeado.

### mostrarAlumnosPorEncimaDelUmbral(studentsArrays, threshold)

Filtra y devuelve solo aquellos alumnos cuyo promedio sea mayor al umbral (ej. 6).

### mostrarAlumnosDesaprobados(studentsArrays)

Devuelve alumnos que tengan alguna nota menor a 4.

### calcularAprobadosDesaprobados(studentsArrays)

Cuenta y retorna la cantidad de aprobados (Promedio ≥ 4) y desaprobados.

Interfaz gráfica (view.py)
------------------------------

### TreeView

*   Se muestra una tabla con columnas: **Nombre, Materia, Nota1, Nota2, Nota3, Promedio**
    
*   Se puede hacer **doble clic** sobre una celda para editarla.
    
*   Las celdas de notas se validan automáticamente al editar.
    

### Botones

*   **Cargar CSV**: Abre un file dialog para importar un CSV. No sobrescribe datos existentes.
    
*   **Agregar Alumno**: Abre una ventana con formularios de entrada manual.
    
*   **Validar Notas**: Ejecuta la validación de todas las notas cargadas.
    
*   **Descargar CSV**: Exporta todos los datos a un nuevo archivo.
    
*   **Reportes**: Genera estadísticas y filtrados en ventanas secundarias.
    

Ordenamiento
---------------

*   **Algoritmo utilizado**: [list.sort()](https://docs.python.org/3/library/stdtypes.html#list.sort), que utiliza **Timsort** (estable, O(n log n))
    
*   **Visualización**: Al hacer clic en los encabezados de columna, se alterna el orden:
    
    *   Primero ascendente ↑
        
    *   Luego descendente ↓
        
*   El ícono se muestra al lado del título de la columna activa.
    

Estructuras de Datos
-----------------------

*   students: Lista de listas, donde cada estudiante es
    ```
    ["Juan", "Matemática", 7.5, 8.0, 9.0, 8.17]
    ```
    
*   Reportes intermedios: listas de diccionarios {Nombre, Materia, Notas, Promedio}
    

Requisitos
-------------

*   Python ≥ 3.7
    
*   pandas
    
*   tkinter (incluido por defecto en instalaciones estándar)
