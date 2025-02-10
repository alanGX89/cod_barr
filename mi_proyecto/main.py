import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QClipboard

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FILE ARDISA PILAT")
        self.setGeometry(100, 100, 700, 500)

        # Variables de estado
        self.buffer = ""
        self.current_row = 0
        self.current_col = 0

        # Layout principal
        layout = QVBoxLayout()

        # Título con separación
        self.title_label = QLabel("Escanea un código de barras", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_label)
        
        # Línea divisoria
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # En el layout
        self.counter_label = QLabel("Códigos escaneados: 0", self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("font-size: 16px; font-weight: normal; color: #FF5722;")
        layout.addWidget(self.counter_label)

        # Tabla de códigos
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  # 2 columnas: Código y Descripción
        self.table.setRowCount(1)  # Comenzamos con 1 fila
        self.table.setHorizontalHeaderLabels(["ID_CAJA", "BRAFIT"])
        
        # Aumentar el tamaño de las celdas
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 400)
        self.table.setRowHeight(0, 50)
        
        layout.addWidget(self.table)

        # Botones en un layout horizontal centrado
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.clear_table_button = QPushButton("🗑 Limpiar Tabla", self)
        self.clear_table_button.clicked.connect(self.clear_table)
        
        self.help_button = QPushButton("📖 Instrucciones", self)
        self.help_button.clicked.connect(lambda: self.title_label.setText("📌 Escanea un código de barras..."))
        
        self.copy_table_button = QPushButton("📋 Copiar Tabla", self)
        self.copy_table_button.clicked.connect(self.copy_table)


        button_layout.addStretch()
        button_layout.addWidget(self.clear_table_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.copy_table_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Aplicar estilo personalizado
        self.apply_custom_style()

        # Iniciar el programa con "Limpiar Tabla"
        self.clear_table()

        # Funcionalidad tabulada permanente
        self.tab_functionality()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.buffer:
                self.save_code(self.buffer)
                self.buffer = ""
                self.move_cursor()
        else:
            self.buffer += event.text()

    def save_code(self, code):
        self.table.setItem(self.current_row, self.current_col, QTableWidgetItem(code))
        self.update_box_count()
        self.update_counter()

    def update_counter(self):
        # Contador de códigos escaneados
        self.counter_label.setText(f"Códigos escaneados: {self.current_row + 1}")

    def move_cursor(self):
        total_cols = self.table.columnCount()
        
        if self.current_col < total_cols - 1:
            self.current_col += 1
        else:
            self.current_col = 0
            self.current_row += 1
            if self.current_row >= self.table.rowCount():
                self.table.insertRow(self.table.rowCount())
        
        self.table.setCurrentCell(self.current_row, self.current_col)
        self.update_box_count()

    def tab_functionality(self):
        """Función permanente para la funcionalidad tabulada"""
        self.move_cursor()

    def clear_table(self):
        self.table.clearContents()
        self.current_row = 0
        self.current_col = 0
        self.update_box_count()

    def update_box_count(self):
        filled_columns = sum(1 for col in range(self.table.columnCount()) if any(self.table.item(row, col) for row in range(self.table.rowCount())))
        # Solo cambiar la lógica si es necesario, en este caso la cuenta de filas se deja igual
        self.title_label.setText(f"Escanea un código de barras")

    def copy_table(self):
        """Función para copiar todo el contenido de la tabla al portapapeles"""
        clipboard = QApplication.clipboard()
        text_to_copy = ""
        
        # Recorre todas las filas y columnas de la tabla
        for row in range(self.table.rowCount()):
            row_text = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_text.append(item.text() if item else "")
            text_to_copy += "\t".join(row_text) + "\n"
        
        clipboard.setText(text_to_copy)
    def apply_custom_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #333333;
                border: none;
            }
            QLabel {
                color: #FFC107;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLabel#title_label {
                text-align: center;
            }
            QLabel#counter_label {
                color: #FF5722;
                font-size: 14px;
                text-align: center;
                font-weight: normal;
            }
            QPushButton {
                background-color: #FFC107;
                color: #FFFFFF;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #FFB300;
            }
            QTableWidget {
                background-color: #FFFFFF;
                color: #333333;
                gridline-color: #333333;
                font-size: 14px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
