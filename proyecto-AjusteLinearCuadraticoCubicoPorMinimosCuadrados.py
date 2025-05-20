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
        self.style.configure('Tentry', padding = 3)

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
        
        self.btn_set_points = ttk.Button(self.config_frame, text="Generar Campos", 
                                       command=self.crear_campos_puntos)
        self.btn_set_points.grid(row=0, column=2, padx=10, pady=5)
        
        # Inicializar variables para puntos
        self.entries_x = []
        self.entries_y = []
        self.n = 0
        
        # Frame para resultados y gráfica
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
        
        # Gráfica integrada
        self.graph_frame = ttk.LabelFrame(self.results_frame, text="Gráfica", padding=10)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Botón de cálculo
        self.btn_calcular = ttk.Button(self.main_frame, text="Calcular Ajustes", command=self.calcular_ajustes)
        self.btn_calcular.pack(pady=10)


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
                self.text_resultado.insert(tk.END, "Coeficientes (de mayor a menor grado):\n")
                
                for i, c in enumerate(coef):
                    self.text_resultado.insert(tk.END, f"  x^{len(coef)-1-i}: {c:.6f}\n")
                
                # Calcular y mostrar error cuadrático medio
                error = np.mean((y - y_fit)**2)
                self.text_resultado.insert(tk.END, f"  Error cuadrático medio: {error:.6f}\n")
                
            except np.linalg.LinAlgError:
                self.text_resultado.insert(tk.END, f"\nNo se pudo calcular el ajuste {etiqueta}\n")

        self.ax.title("Ajustes Polinomiales por Mínimos Cuadrados")
        self.ax.xlabel("X")
        self.ax.ylabel("Y")
        self.ax.legend()
        self.ax.grid(True, linestyle = '--', alpha = 0.7)
        
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ajustePolinomial(root)
    root.mainloop()