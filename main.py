import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PySide6.QtGui import QPalette

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visor STL")
        self.setGeometry(100, 100, 1100, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.vtk = VTKWidget(self)
        layout.addWidget(self.vtk.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
