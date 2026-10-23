import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit


CSV_FILE = "datos.csv"
if not os.path.exists(CSV_FILE):
    data = {
        "id_producto": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "nombre_producto": ["Laptop HP", "Teclado Mecánico", "Mouse Inalámbrico", "Monitor 24\"", "Impresora Multifuncional", "Disco Duro SSD 1TB", "Memoria RAM 16GB", "Router Wi-Fi", "Tablet Lenovo", "Audífonos Gamer"],
        "sucursal": ["San Salvador", "San Salvador", "Santa Ana", "Santa Ana", "San Miguel", "San Miguel", "La Libertad", "La Libertad", "Sonsonate", "Sonsonate"],
        "stock": [25, 50, 80, 30, 15, 40, 60, 35, 20, 45],
        "precio_unitario": [650.0, 45.5, 20.0, 180.0, 220.0, 90.0, 75.0, 50.0, 150.0, 35.0]
    }
    pd.DataFrame(data).to_csv(CSV_FILE, index=False)


df = pd.read_csv(CSV_FILE)
print("=== ESTRUCTURA DEL DATAFRAME ===")
print(df.info())
print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)
print("\n=== ESTADÍSTICAS BÁSICAS ===")
print(df.describe())


class InventarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventario - Sucursales UGB")
        self.setGeometry(100, 100, 900, 700)
        
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        
        title = QLabel("Dashboard de Inventario por Sucursal")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.generar_grafico()
        
        
        self.text_info = QTextEdit()
        self.text_info.setReadOnly(True)
        self.text_info.setPlainText(f"Resumen Estadístico:\n{df.describe().to_string()}")
        layout.addWidget(self.text_info)

    def generar_grafico(self):
       
        stock_sucursal = df.groupby('sucursal')['stock'].sum()
        
        self.ax.clear()
        stock_sucursal.plot(kind='bar', ax=self.ax, color='skyblue', edgecolor='black')
        self.ax.set_title("Stock Total por Sucursal")
        self.ax.set_xlabel("Sucursal")
        self.ax.set_ylabel("Stock Acumulado")
        self.ax.tick_params(axis='x', rotation=30)
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = InventarioApp()
    ventana.show()
    sys.exit(app.exec_())