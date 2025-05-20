"""
PROYECTO PARA LA MATERIA DE MÉTODOS NUMÉRICOS.
INTEGRANTES:
    GUSTAVO CORTÉS ORTA.
    ANGEL ALEJANDRO ALANÍS CASTILLO.
    JOSÉ EDUARDO SALMERÓN MARTÍNEZ.

DOCENTE: MC. JORGE LIMONES MAGALLANES

PROYECTO: CALCULADORA DE AJUSTES POR MINIMOS CUADRADOS.

DESCRIPCIÓN: ESTE PROYECTO ES UN CÓDIGO DESARROLLADO EN EL LENGUAJE DE PROGRAMACIÓN PYTHON QUE PERMITE AL USUARIO
INGRESAR LA CANTIDAD DE PUNTOS Y POSTERIORMENTE INGRESAR EL VALOR DE DICHOS PUNTOS PARA CALCULAR MEDIANTE EL MÉTODO
DE AJUSTE POR MINIMOS CUADRADOS (LINEAL, CUADRÁTICO Y CÚBICO) LA ECUACIÓN Y EL VALOR DE R^2, ASÍ COMO OBTENER UNA 
GRÁFICA CON LOS PUNTOS Y LAS ESTIMACIONES.

INSTRUCCIONES DE USO: ASEGÚRESE DE TENER INSTALADO EN SU ENTORNO DE PYTHON INSTALADAS LAS SIGUIENTES LIBRERÍAS:
TKINTER, NUMPY Y MATPLOTLIB. EJECUTE EL CÓDIGO E INSERTE LA CANTIDAD DE PUNTOS QUE DESEA INGRESAR PARA, POSTERIORMENTE
INGRESAR EL VALOR PARA CADA PUNTO. UNA VEZ QUE HA INGRESADO TODOS LOS VALORES CORRESPONDIENTES PARA CADA PUNTO
PRESIONE EL BOTÓN "CALCULAR AJUSTE" PARA OBTENER LOS TRES AJUSTES EN LA CAJA DE RESULTADOS Y LA GRÁFICA EN LA CAJA 
DE GRAFICACIÓN.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ajustePolinomial:
    def __init__(self, root):
        self.root = root
        self.root.title("CALCULADORA DE AJUSTE POR MÍNIMOS CUADRADOS.")
        self.root.geometry("1000x800")

        #ESTILO
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#f0f0f0')
        self.style.configure('TButton', font = ('Poppins', 10), padding = 5)
        self.style.configure('TLabel', font = ('Poppins', 15))

        #Frame Principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand = True, padx = 10, pady = 10)

        #Frame secundario para la entrada de los puntos
        self.config_frame = ttk.LabelFrame(self.main_frame, text = "Configuración", padding = 10)
        self.config_frame.pack(fill=tk.X, pady = 5)

        # Sección para número de puntos
        ttk.Label(self.config_frame, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_n = ttk.Entry(self.config_frame, width=10)
        self.entry_n.grid(row=0, column=1, padx=5, pady=5)
        self.entry_n.bind("<KeyRelease>", self.actualizar_campos_puntos)
        
        self.points_frame = ttk.Frame(self.config_frame)
        self.points_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.entries_x = []
        self.entries_y = []

        # Frame resultados + gráfico
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # Texto de resultados
        self.text_frame = ttk.LabelFrame(self.results_frame, text="Resultados", padding=10)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.text_resultado = tk.Text(self.text_frame, height=15, width=40, wrap=tk.WORD)
        self.text_resultado.pack(fill=tk.BOTH, expand=True)

        text_scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.text_resultado.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_resultado.config(yscrollcommand=text_scrollbar.set)

        # Gráfica
        self.graph_frame = ttk.LabelFrame(self.results_frame, text="Gráfica", padding=10)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Botón para calcular
        self.btn_calcular = ttk.Button(self.text_frame, text="Calcular Ajustes", command=self.calcular_ajustes)
        self.btn_calcular.pack(side=tk.BOTTOM, expand=True, padx=10, pady = 3)

    def actualizar_campos_puntos(self, event = None):
        try:
            n = int(self.entry_n.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de puntos.")
            return
        
        #limpiar widget de campos anteriores.
        for widget in self.points_frame.winfo_children():
            widget.destroy()
        self.entries_x.clear()
        self.entries_y.clear()

        #Titulos de encabezado
        ttk.Label(self.points_frame, text = "X").grid(row = 0, column = 0, padx = 5)
        ttk.Label(self.points_frame, text = "Y").grid(row = 0, column = 1, padx = 5)

        #Entradas
        for i in range(n):
            entry_x = ttk.Entry(self.points_frame, width = 10)
            entry_x.grid(row = i + 1, column = 0, padx = 5, pady = 2)
            self.entries_x.append(entry_x)

            entry_y = ttk.Entry(self.points_frame, width = 10)
            entry_y.grid(row = i + 1, column = 1, padx = 5, pady = 2)
            self.entries_y.append(entry_y)

    def calcular_ajustes(self):
        if not self.entries_x or not self.entries_y:
            messagebox.showerror("Error", "Primero defina los puntos.")
            return
        
        try:
            x = np.array([float(entry.get()) for entry in self.entries_x])
            y = np.array([float(entry.get()) for entry in self.entries_y])
        except ValueError:
            messagebox.showerror("Error", "Los valores deben de ser numéricos.")
            return
        
        self.text_resultado.delete("1.0", tk.END)
        self.ax.clear()

        grados = [1, 2, 3]
        colores = ['r', 'g', 'b']
        etiquetas = ['Lineal', 'Cuadrático', 'Cúbico']

        self.ax.scatter(x, y, color='black', label = 'Puntos', zorder = 5)

        for grado, color, etiqueta in zip(grados, colores, etiquetas):
            try:
                coef = np.polyfit(x, y, grado)
                y_fit = np.polyval(coef, x)
                
                # Graficar ajuste
                self.ax.plot(x, y_fit, color=color, label=f'Ajuste {etiqueta}', linewidth=2)
                
                # Mostrar coeficientes en el texto
                self.text_resultado.insert(tk.END, f"\nAjuste {etiqueta} (grado {grado}):\n")
                
                ecuacion = "y = "
                terminos = []
                for i, c in enumerate(coef):
                    exp = len(coef) - 1 - i
                    if exp == 0:
                        terminos.append(f"{c:.3f}")
                    elif exp == 1:
                        terminos.append(f"{c:.3f}·x")
                    else:
                        terminos.append(f"{c:.3f}·x^{exp}")
                ecuacion += " + ".join(terminos)
                
                # Calcular y mostrar error cuadrático medio
                ss_res = np.sum((y - y_fit) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r2 = 1 - (ss_res / ss_tot)

                # Mostrar resultados
                self.text_resultado.insert(tk.END, f"  Ecuación: {ecuacion}\n")
                self.text_resultado.insert(tk.END, f"  R² (coef. determinación): {r2:.6f}\n")
                
            except np.linalg.LinAlgError:
                self.text_resultado.insert(tk.END, f"\nNo se pudo calcular el ajuste {etiqueta}\n")

        self.ax.set_title("AJUSTES POR MINIMOS CUADRADOS.")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend()
        self.ax.grid(True, linestyle = '--', alpha = 0.7)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ajustePolinomial(root)
    root.mainloop()