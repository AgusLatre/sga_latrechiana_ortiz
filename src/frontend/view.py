import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.api import (
    readCSVFile, validateNotas, calculateNotaFinal,
    mostrarAlumnosPorEncimaDelUmbral, mostrarAlumnosDesaprobados,
    calcularAprobadosDesaprobados
)

class GradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Notas")
        self.students = []
        self.columns = ["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "Promedio"]
        self.sort_states = {col: None for col in self.columns}
        self.editing = False

        # Botones principales
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Cargar CSV", command=self.load_csv).pack(side="left", padx=5)
        tk.Button(button_frame, text="Agregar Alumno", command=self.add_student).pack(side="left", padx=5)
        tk.Button(button_frame, text="Validar Notas", command=self.validate).pack(side="left", padx=5)
        tk.Button(button_frame, text="Descargar CSV", command=self.download_csv).pack(side="left", padx=5)

        # Resultados
        self.results_frame = tk.LabelFrame(root, text="Listado de Alumnos", padx=10, pady=10)
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(self.results_frame, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col))
            self.tree.column(col, anchor='center', width=100)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(fill="both", expand=True)

        # Reportes
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
        new_students, self.columns_from_csv = readCSVFile(path)
        if new_students:
            self.students += new_students  # no sobrescribas, sumalos
            self.students = calculateNotaFinal(self.students)
            self.refresh_tree()
            messagebox.showinfo("Cargado", "Archivo CSV cargado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")

    def validate(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "Primero cargue datos.")
            return
        self.students, errors = validateNotas(self.students)
        if errors:
            msg = "Errores encontrados:\n"
            for err in errors:
                fila, columna, descripcion = err
                msg += f"Fila {fila+1}, Columna {columna+1}: {descripcion}\n"
            messagebox.showerror("Errores de validación", msg)
        else:
            messagebox.showinfo("Validado", "Todas las notas son válidas.")
        self.students = calculateNotaFinal(self.students)
        self.refresh_tree()

    def calculate(self):
        self.students = calculateNotaFinal(self.students)
        self.refresh_tree()

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in self.students:
            self.tree.insert("", "end", values=student)

    def add_student(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Alumno")

        entries = []
        labels = ["Nombre", "Materia", "Nota 1", "Nota 2", "Nota 3"]
        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def save_student():
            try:
                notas = [float(entries[i].get()) for i in range(2, 5)]
                if any(n < 0 or n > 10 for n in notas):
                    raise ValueError("Notas deben ser entre 0 y 10")
                promedio = round(sum(notas) / 3, 2)
                nuevo = [entries[0].get(), entries[1].get(), *notas, promedio]
                self.students.append(nuevo)
                self.refresh_tree()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Notas inválidas")

        tk.Button(win, text="Guardar", command=save_student).grid(row=5, column=0, columnspan=2, pady=10)

    def on_double_click(self, event):
        if self.editing:
            return
        self.editing = True
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or not column:
            self.editing = False
            return

        col_index = int(column.replace('#', '')) - 1
        x, y, width, height = self.tree.bbox(item, column)
        value = self.tree.item(item, 'values')[col_index]

        entry = tk.Entry(self.tree)
        entry.insert(0, value)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()

        def on_focus_out(event):
            new_value = entry.get()
            values = list(self.tree.item(item, 'values'))
            try:
                if col_index >= 2 and col_index <= 4:
                    new_value = float(new_value)
                    if not 0 <= new_value <= 10:
                        raise ValueError
                values[col_index] = new_value
                if col_index >= 2 and col_index <= 4:
                    notas = [float(values[i]) for i in range(2, 5)]
                    values[5] = round(sum(notas) / 3, 2)
                self.tree.item(item, values=values)
                idx = self.tree.index(item)
                self.students[idx] = values
            except ValueError:
                messagebox.showerror("Error", "Valor inválido.")
            entry.destroy()
            self.editing = False

        entry.bind("<FocusOut>", on_focus_out)

    def sort_by_column(self, col):
        col_index = self.columns.index(col)
        current_order = self.sort_states[col]
        reverse = False if current_order != "asc" else True
        self.sort_states[col] = "desc" if reverse else "asc"

        for c in self.columns:
            arrow = ""
            if c == col:
                arrow = " ↓" if reverse else " ↑"
            self.tree.heading(c, text=c + arrow)

        try:
            self.students.sort(key=lambda x: float(x[col_index]), reverse=reverse)
        except ValueError:
            self.students.sort(key=lambda x: str(x[col_index]), reverse=reverse)

        self.refresh_tree()

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
        tree = ttk.Treeview(win, columns=self.columns, show='headings')
        for col in self.columns:
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
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        with open(path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            for student in self.students:
                writer.writerow(student)
        messagebox.showinfo("Éxito", f"Datos exportados a {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()
