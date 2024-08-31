import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class SudokuGUI(QWidget):
    def __init__(self, solver_class):
        super().__init__()
        self.solver_class = solver_class
        self.solver = solver_class()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Soldoku - Ädus Sudoku Solver")
        self.grid_layout = QGridLayout()
        self.cells = []
        self.cell_labels = []

        # Create 9x9 grid of QLineEdit widgets with QLabel underneath
        for i in range(9):
            row = []
            label_row = []
            for j in range(9):
                vbox = QVBoxLayout()

                # QLineEdit for user input
                cell = QLineEdit(self)
                cell.setFont(QFont("Arial", 22))
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFixedSize(80, 80)
                cell.setMaxLength(1)
                cell.textChanged.connect(self.create_text_change_callback(i, j))

                # QLabel for displaying set values in smaller font and grayscale
                cell_label = QLabel(self)
                small_font = QFont("Arial", 8)  # Smaller font size
                cell_label.setFont(small_font)
                cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell_label.setFixedSize(80, 15)

                # Set the grayscale color for the label text
                palette = cell_label.palette()
                palette.setColor(QPalette.ColorRole.WindowText, QColor(150, 150, 150))  # Grayscale color
                cell_label.setPalette(palette)

                # Add QLineEdit and QLabel to the layout
                vbox.addWidget(cell)
                vbox.addWidget(cell_label)

                self.grid_layout.addLayout(vbox, i, j)
                row.append(cell)
                label_row.append(cell_label)

            self.cells.append(row)
            self.cell_labels.append(label_row)

        # Create the Solve button
        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setFont(QFont("Arial", 18))
        self.solve_button.clicked.connect(self.solve_sudoku)

        # Layout setup
        vbox = QVBoxLayout()
        vbox.addLayout(self.grid_layout)
        vbox.addWidget(self.solve_button)
        self.setLayout(vbox)

        # Initialize the display
        self.update_grid()

    def create_text_change_callback(self, row, col):
        def callback():
            text = self.cells[row][col].text()
            if text.isdigit():
                self.solver.grid[row][col] = {int(text)}
                self.solver.reduce_all()
            else:
                self.solver.grid[row][col] = self.solver_class.full_set.copy()
            self.update_grid()
        return callback

    def solve_sudoku(self):
        self.solver.solve()
        self.update_grid()

    def update_grid(self):
        for i in range(9):
            for j in range(9):
                cell_set = self.solver.grid[i][j]
                if len(cell_set) == 1:
                    self.cells[i][j].setText(str(list(cell_set)[0]))
                else:
                    self.cells[i][j].setText("")

                # Update the QLabel with the current set of possible values
                self.cell_labels[i][j].setText("{" + ",".join(map(str, sorted(cell_set))) + "}")

if __name__ == '__main__':
    from soldoku import Soldoku  # Replace with the actual module name

    app = QApplication(sys.argv)
    ex = SudokuGUI(Soldoku)
    ex.show()
    sys.exit(app.exec())
