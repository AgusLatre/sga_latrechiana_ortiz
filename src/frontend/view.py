import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.api import (
    readCSVFile, validateNotas, calculateNotaFinal,
    mostrarAlumnosPorEncimaDelUmbral,
    mostrarAlumnosDesaprobados, calcularAprobadosDesaprobados
)
class GradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Notas")
        self.students = []

        # Botones principales
        self.load_button = tk.Button(root, text="Cargar CSV", command=self.load_csv)
        self.load_button.pack(pady=5)

        self.validate_button = tk.Button(root, text="Validar Notas", command=self.validate)
        self.validate_button.pack(pady=5)

        self.calculate_button = tk.Button(root, text="Calcular Nota Final", command=self.calculate)
        self.calculate_button.pack(pady=5)

        self.results_frame = tk.LabelFrame(root, text="Resultados", padx=10, pady=10)
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview para mostrar estudiantes
        self.tree = ttk.Treeview(self.results_frame, columns=("Nombre", "Materia", "Nota1", "Nota2", "Nota3", "Final"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        # Botones de reportes
        self.report_frame = tk.Frame(root)
        self.report_frame.pack(pady=10)

        tk.Button(self.report_frame, text="Promedio por Materia", command=self.show_averages).grid(row=0, column=0, padx=5)
        tk.Button(self.report_frame, text="Alumnos con Promedio > 6", command=self.show_above_threshold).grid(row=0, column=1, padx=5)
        tk.Button(self.report_frame, text="Desaprobados", command=self.show_failing).grid(row=0, column=2, padx=5)
        tk.Button(self.report_frame, text="Aprobados/Desaprobados", command=self.show_pass_fail_count).grid(row=0, column=3, padx=5)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        self.students, self.columns = readCSVFile(path)
        if self.students:
            self.materias = self.columns[2:5]
            self.refresh_tree()
            messagebox.showinfo("Cargado", "Archivo CSV cargado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")

    def validate(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "Primero cargue un archivo CSV.")
            return
        self.students, errors = validateNotas(self.students)
        if not hasattr(self, 'materias') and hasattr(self, 'columns'):
            self.materias = self.columns[2:5]
        if errors:
            msg = "Errores encontrados:\n"
            for err in errors:
                fila, columna, descripcion = err
                msg += f"Fila {fila+1}, Columna {columna+1}: {descripcion}\n"
            messagebox.showerror("Errores de validación", msg)
        else:
            messagebox.showinfo("Validado", "Todas las notas son válidas.")

    def calculate(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "Primero cargue y valide un archivo.")
            return
        self.students = calculateNotaFinal(self.students)
        self.refresh_tree()
        messagebox.showinfo("Calculado", "Notas finales calculadas.")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in self.students:
            self.tree.insert("", "end", values=student)

    def show_averages(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "No hay datos.")
            return
        materias = set(student[1] for student in self.students)
        msg = ""
        for materia in materias:
            notas = [
                float(student[5]) if len(student) > 5 else (float(student[2]) + float(student[3]) + float(student[4])) / 3
                for student in self.students if student[1] == materia
            ]
            if notas:
                promedio = sum(notas) / len(notas)
                msg += f"{materia}: {promedio:.2f}\n"
        messagebox.showinfo("Promedios por materia", msg)

    def show_above_threshold(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "No hay datos.")
            return
        threshold = 6
        filtered = mostrarAlumnosPorEncimaDelUmbral(self.students, threshold)
        self.show_filtered_results(filtered, f"Alumnos con promedio > {threshold}")

    def show_failing(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "No hay datos.")
            return
        filtered = mostrarAlumnosDesaprobados(self.students)
        self.show_filtered_results(filtered, "Alumnos desaprobados")

    def show_pass_fail_count(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "No hay datos.")
            return
        stats = calcularAprobadosDesaprobados(self.students)
        messagebox.showinfo("Resumen", f"Aprobados: {stats['Aprobados']}\nDesaprobados: {stats['Desaprobados']}")

    def show_filtered_results(self, filtered_list, title):
        win = tk.Toplevel(self.root)
        win.title(title)
        tree = ttk.Treeview(win, columns=("Nombre", "Legajo", "Nota1", "Nota2", "Nota3", "Promedio"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        for student in filtered_list:
            if isinstance(student, dict):
                values = (
                    student.get("Nombre", ""),
                    student.get("Legajo", ""),
                    student.get("Notas", ["", "", ""])[0] if "Notas" in student else student.get("Nota1", ""),
                    student.get("Notas", ["", "", ""])[1] if "Notas" in student else student.get("Nota2", ""),
                    student.get("Notas", ["", "", ""])[2] if "Notas" in student else student.get("Nota3", ""),
                    student.get("Promedio", "")
                )
            else:
                values = student
            tree.insert("", "end", values=values)


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()
