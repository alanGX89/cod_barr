import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

class CustomTitleBar(QWidget):
    def __init__(self):
        super().__init__()

        # Barra de título personalizada con bordes amarillos
        self.setStyleSheet("""
            QWidget {
                background-color: #F2C94C;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border: 2px solid #F2C94C;  # Borde amarillo
            }
        """)

        # Layout de los botones de la barra de título (minimizar, maximizar, cerrar)
        layout = QHBoxLayout()
        
        self.minimize_button = QPushButton("_", self)
        self.minimize_button.setStyleSheet("background-color: transparent; color: white; font-size: 20px; border: none;")
        self.minimize_button.clicked.connect(self.minimize)

        self.maximize_button = QPushButton("[]", self)
        self.maximize_button.setStyleSheet("background-color: transparent; color: white; font-size: 20px; border: none;")
        self.maximize_button.clicked.connect(self.maximize)

        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("background-color: transparent; color: white; font-size: 20px; border: none;")
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def minimize(self):
        self.window().showMinimized()

    def maximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lector de Código - Empresa File Ardis")
        self.setGeometry(100, 100, 600, 400)  # Tamaño de la ventana

        # Establecer bordes amarillos en la ventana principal
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 5px solid #F2C94C;  # Borde amarillo
                border-radius: 10px;  # Bordes redondeados
            }
        """)

        # Establecer barra de título personalizada
        self.title_bar = CustomTitleBar()

        # Layout principal
        layout = QVBoxLayout()

        # Título de la ventana
        self.title_label = QLabel("Lector de Código", self)
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #F2C94C;  # Color amarillo suave
            padding: 10px;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)

        # Subtítulo con nombre de la empresa
        self.subtitle_label = QLabel("Empresa: File Ardis", self)
        self.subtitle_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #F2C94C;  # Color amarillo suave
            padding: 5px;
        """)
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        # Crear un QTableWidget (simulando una tabla de Excel)
        self.table = QTableWidget(self)
        self.table.setRowCount(3)  # Tres filas
        self.table.setColumnCount(3)  # Tres columnas
        self.table.setHorizontalHeaderLabels(["Código", "Descripción", "Estado"])  # Cabeceras de columnas
        
        # Rellenar las celdas con valores simulados
        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(f"Fila {row+1}, Columna {col+1}")
                self.table.setItem(row, col, item)
        
        # Botón para simular la acción de leer código
        self.read_button = QPushButton("Leer Código", self)
        self.read_button.setStyleSheet("""
            background-color: #FF9800;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
        """)
        self.read_button.clicked.connect(self.on_read_code)

        # Añadir los widgets al layout
        layout.addWidget(self.title_bar)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.table)
        layout.addWidget(self.read_button)

        # Configurar el layout en la ventana principal
        self.setLayout(layout)

    def on_read_code(self):
        """Acción para leer un código, puede actualizar celdas o realizar otras acciones"""
        # Cambiar el texto de las celdas como ejemplo de lectura
        for row in range(3):
            self.table.setItem(row, 0, QTableWidgetItem(f"Código {row+1} leído"))
            self.table.setItem(row, 1, QTableWidgetItem(f"Descripción del código {row+1}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"Estado: Leído"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
