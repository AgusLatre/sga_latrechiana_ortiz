import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from backend.api import (
    readCSVFile, validateNotas, calculateNotaFinal, listaCompleta,
    promedioPorMateria, mostrarAlumnosPorEncimaDelUmbral,
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
        self.students = readCSVFile(path)
        if self.students:
            self.refresh_tree()
            messagebox.showinfo("Cargado", "Archivo CSV cargado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")

    def validate(self):
        if not self.students:
            messagebox.showwarning("Advertencia", "Primero cargue un archivo CSV.")
            return
        self.students = validateNotas(self.students)
        messagebox.showinfo("Validado", "Notas validadas.")

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
        avg = promedioPorMateria(self.students)
        messagebox.showinfo("Promedios por materia", f"Materia 1: {avg['Materia 1']:.2f}\nMateria 2: {avg['Materia 2']:.2f}\nMateria 3: {avg['Materia 3']:.2f}")

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
        tree = ttk.Treeview(win, columns=("Nombre", "ID", "Nota1", "Nota2", "Nota3", "Final"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        for student in filtered_list:
            tree.insert("", "end", values=student)


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()
