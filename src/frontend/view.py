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

        self.load_button = tk.Button(root, text="Cargar CSV", command=self.load_csv)
        self.load_button.pack(pady=5)

        self.add_button = tk.Button(root, text="Agregar Alumno", command=self.add_student)
        self.add_button.pack(pady=5)

        self.validate_button = tk.Button(root, text="Validar Notas", command=self.validate)
        self.validate_button.pack(pady=5)

        self.calculate_button = tk.Button(root, text="Calcular Nota Final", command=self.calculate)
        self.calculate_button.pack(pady=5)

        self.results_frame = tk.LabelFrame(root, text="Resultados", padx=10, pady=10)
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(
            self.results_frame,
            columns=("Nombre", "Materia", "Nota1", "Nota2", "Nota3", "Final"),
            show='headings'
        )
        self.sort_direction = {}
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

        self.report_frame = tk.Frame(root)
        self.report_frame.pack(pady=10)

        tk.Button(self.report_frame, text="Promedio por Materia", command=self.show_averages).grid(row=0, column=0, padx=5)
        tk.Button(self.report_frame, text="Alumnos con Promedio > 6", command=self.show_above_threshold).grid(row=0, column=1, padx=5)
        tk.Button(self.report_frame, text="Desaprobados", command=self.show_failing).grid(row=0, column=2, padx=5)
        tk.Button(self.report_frame, text="Aprobados/Desaprobados", command=self.show_pass_fail_count).grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(root, text="Descargar CSV", command=self.download_csv)
        self.export_button.pack(pady=5)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        self.students, self.columns = readCSVFile(path)
        if self.students:
            self.students = calculateNotaFinal(self.students)
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

    def sort_by_column(self, col):
        col_index = self.tree["columns"].index(col)
        reverse = self.sort_direction.get(col, False)
        self.students.sort(key=lambda row: row[col_index], reverse=reverse)
        self.sort_direction[col] = not reverse
        self.refresh_tree()

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item_id or not column:
            return

        col_idx = int(column.replace("#", "")) - 1
        if col_idx == 5:
            messagebox.showinfo("Info", "El promedio se calcula automáticamente.")
            return

        x, y, width, height = self.tree.bbox(item_id, column)
        entry = tk.Entry(self.tree, bd=2, bg="lightyellow", justify="center", highlightthickness=1, relief="solid")
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, self.tree.set(item_id, column))
        entry.focus()

        def save_edit(event):
            new_value = entry.get()
            student_index = self.tree.index(item_id)
            try:
                if col_idx in [2, 3, 4]:
                    nota = float(new_value)
                    if not 0 <= nota <= 10:
                        raise ValueError
                    self.students[student_index][col_idx] = nota
                else:
                    self.students[student_index][col_idx] = new_value
                self.students = calculateNotaFinal(self.students)
                self.refresh_tree()
            except ValueError:
                messagebox.showerror("Error", "Entrada inválida.")
            finally:
                entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def add_student(self):
        def save_new():
            nombre = e_nombre.get()
            materia = e_materia.get()
            try:
                nota1 = float(e_nota1.get())
                nota2 = float(e_nota2.get())
                nota3 = float(e_nota3.get())
                for n in [nota1, nota2, nota3]:
                    if not 0 <= n <= 10:
                        raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Notas inválidas.")
                return

            nuevo = [nombre, materia, nota1, nota2, nota3]
            nuevo = calculateNotaFinal([nuevo])[0]
            self.students.append(nuevo)
            self.refresh_tree()
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Agregar Alumno")

        tk.Label(top, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(top, text="Materia").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(top, text="Nota 1").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(top, text="Nota 2").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(top, text="Nota 3").grid(row=4, column=0, padx=5, pady=5)

        e_nombre = tk.Entry(top)
        e_materia = tk.Entry(top)
        e_nota1 = tk.Entry(top)
        e_nota2 = tk.Entry(top)
        e_nota3 = tk.Entry(top)

        e_nombre.grid(row=0, column=1)
        e_materia.grid(row=1, column=1)
        e_nota1.grid(row=2, column=1)
        e_nota2.grid(row=3, column=1)
        e_nota3.grid(row=4, column=1)

        tk.Button(top, text="Guardar", command=save_new).grid(row=5, column=0, columnspan=2, pady=10)

    def show_averages(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "No hay datos.")
            return
        materias = set(student[1] for student in self.students)
        msg = ""
        for materia in materias:
            notas = [float(student[5]) for student in self.students if student[1] == materia]
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
        tree = ttk.Treeview(win, columns=("Nombre", "Materia", "Nota1", "Nota2", "Nota3", "Promedio"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        for student in filtered_list:
            values = (
                student.get("Nombre", ""),
                student.get("Materia", ""),
                student.get("Notas", ["", "", ""])[0] if "Notas" in student else student.get("Nota1", ""),
                student.get("Notas", ["", "", ""])[1] if "Notas" in student else student.get("Nota2", ""),
                student.get("Notas", ["", "", ""])[2] if "Notas" in student else student.get("Nota3", ""),
                student.get("Promedio", "")
            )
            tree.insert("", "end", values=values)

    def download_csv(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar como"
        )

        if not file_path:
            return

        import pandas as pd
        columns = ["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "Final"]
        df = pd.DataFrame(self.students, columns=columns)
        try:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Exportado", "CSV exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()
