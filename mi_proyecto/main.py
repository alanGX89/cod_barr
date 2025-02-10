import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QMovie, QIcon

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FILE ARDISA PILAT")
        self.setGeometry(100, 100, 800, 500)

        # Variables de estado
        self.buffer = ""
        self.current_row = 0
        self.current_col = 0
        self.box_count = 0  # Contador de cajas

        # Layout principal
        layout = QVBoxLayout()

        # Título con estilo similar al de los botones
        self.title_label = QLabel("FILE ARDISA", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(""" 
            font-size: 26px; 
            font-weight: bold; 
            color: white; 
            background-color: #F9A825;
            border-radius: 12px;
            padding: 10px;
        """)
        layout.addWidget(self.title_label)

        # Línea divisoria
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Contenedor para el GIF
        gif_layout = QHBoxLayout()
        gif_layout.setAlignment(Qt.AlignCenter)  # Centra el contenido dentro del layout

        # Ruta del archivo GIF
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(BASE_DIR, "assets", "box.gif")

        # GIF
        self.gif_label = QLabel(self)
        self.movie = QMovie(gif_path)
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Añadir el GIF al layout
        gif_layout.addWidget(self.gif_label)

        # Añadir el layout del GIF al layout principal
        layout.addLayout(gif_layout)

        # Contador de cajas
        self.box_count_label = QLabel("0", self)
        self.box_count_label.setAlignment(Qt.AlignLeft)
        self.box_count_label.setStyleSheet("font-size: 26px; font-weight: bold; margin-left: 20px;")
        gif_layout.addWidget(self.box_count_label)

        # Añadir el contenedor al layout principal
        layout.addLayout(gif_layout)

        # Tabla de códigos
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(1)
        self.table.setHorizontalHeaderLabels(["ID_CAJA", "BRAFIT"])
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 400)
        self.table.setRowHeight(0, 50)
        layout.addWidget(self.table)

        # Botones en un layout horizontal centrado
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Botón de limpiar
        self.clear_table_button = QPushButton("Limpiar Todo", self)
        self.clear_table_button.setIcon(QIcon(os.path.join(BASE_DIR, "assets", "clear.ico")))
        self.clear_table_button.clicked.connect(self.clear_table)

        # Botón de copiar tabla
        self.copy_table_button = QPushButton("Copiar Tabla", self)
        self.copy_table_button.setIcon(QIcon(os.path.join(BASE_DIR, "assets", "copy.ico")))
        self.copy_table_button.clicked.connect(self.copy_table)

        # Botón de borrar el código de la celda anterior
        self.delete_previous_button = QPushButton("Borrar Código", self)
        self.delete_previous_button.setIcon(QIcon(os.path.join(BASE_DIR, "assets", "delete.ico")))
        self.delete_previous_button.clicked.connect(self.delete_previous_code)

        button_layout.addStretch()
        button_layout.addWidget(self.clear_table_button)
        button_layout.addWidget(self.copy_table_button)
        button_layout.addWidget(self.delete_previous_button)  # Añadido el botón para borrar código
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.apply_custom_style()
        self.clear_table()
        self.tab_functionality()

    def delete_previous_code(self):
        """Función para borrar el código de la celda anterior y mover el cursor allí"""
        # Comprobamos si estamos en la primera columna o fila
        if self.current_row > 0 or self.current_col > 0:
            prev_row = self.current_row
            prev_col = self.current_col - 1 if self.current_col > 0 else self.current_col - 1
            if prev_col < 0:  # Si estamos en la primera columna de la fila, retrocedemos a la fila anterior
                prev_row -= 1
                prev_col = self.table.columnCount() - 1  # Última columna de la fila anterior
            
            # Borra el contenido de la celda anterior
            self.table.setItem(prev_row, prev_col, QTableWidgetItem(""))  
            
            # Mueve el cursor a la celda anterior
            self.current_row, self.current_col = prev_row, prev_col  
            self.table.setCurrentCell(self.current_row, self.current_col)  # Mueve el selector a la celda anterior

            # Actualiza el contador de cajas
            self.update_box_count()  

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.buffer:
                self.save_code(self.buffer)
                self.buffer = ""
                self.move_cursor()
        else:
            self.buffer += event.text()

    def save_code(self, code):
        # Asigna el código a la celda correspondiente
        self.table.setItem(self.current_row, self.current_col, QTableWidgetItem(code))
        if self.table.item(self.current_row, 0) is not None and self.table.item(self.current_row, 1) is not None:
            if self.table.item(self.current_row, 0).text() != "" and self.table.item(self.current_row, 1).text() != "":
                self.increment_box_count()  # Incrementar el contador si ambas celdas están llenas
        self.update_box_count()

    def increment_box_count(self):
        self.box_count += 1

    def update_box_count(self):
        self.box_count_label.setText(str(self.box_count))

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
        self.move_cursor()

    def clear_table(self):
        self.table.clearContents()
        self.current_row = 0
        self.current_col = 0
        self.box_count = 0
        self.update_box_count()

    def update_box_count(self):
        self.box_count_label.setText(f"; {self.box_count}")

    def copy_table(self):
        clipboard = QApplication.clipboard()
        text_to_copy = ""
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
                background-color: #F4F4F4;
                color: #333333;
            }
            QLabel {
                color: #555555;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLabel#title_label {
                font-size: 26px;
                font-weight: bold;
                background-color: #2196F3;
                border-radius: 12px;
                color: white;
                padding: 10px;
            }
            QPushButton {
                background-color: #d7dc35;
                color: white;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                margin: 15px 10px;
            }
            QPushButton:hover {
                background-color: #FBC02D;
            }
            QPushButton:pressed {
                background-color: #F9A825;
            }
            QTableWidget {
                background-color: #FFFFFF;
                color: #333333;
                gridline-color: #E0E0E0;
                font-size: 14px;
                border: 1px solid #E0E0E0;  /* Reduces border size around the table */
            }
            QTableWidget::item {
                padding: 5px;  /* Reduce padding inside the cells */
                border: 1px solid #E0E0E0;  /* Adjust border for each cell */
            }
            QTableWidget::item:selected {
                background-color: #80D4FF;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.clear_table()
    window.show()
    sys.exit(app.exec_())
