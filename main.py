import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PySide6.QtGui import QPalette
from PySide6.QtCore import QThread, Signal, Slot
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import serial

class Serial(QThread):
    data = Signal(list)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False

    def run(self):
        try:
            self.ino = serial.Serial(self.port, self.baudrate)
            self.running = True
            while self.running:
                try:
                    line = self.ino.readline().decode('utf-8').rstrip()
                    self.data.emit([float(i) for i in line.split(',')])
                except:
                    self.data.emit([0.0 for i in range(3)])
                    return
        except serial.SerialException as e:
            print(f"[err] {e}")
        finally:
            if self.ino and self.ino.is_open:
                self.ino.close()

    def stop(self):
        self.running = False
        if self.ino and self.ino.is_open:
            self.ino.close()
        self.wait()


class VTKWidget():
    def __init__(self, parent):
        self.widget = QVTKRenderWindowInteractor(parent)

        self.ren = vtk.vtkRenderer()
        self.widget.GetRenderWindow().AddRenderer(self.ren)
        
        self.iren = self.widget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()

        self.widget.GetRenderWindow().SetAlphaBitPlanes(1)
        self.ren.SetViewport(0, 0, 1, 1)

        self.ren.SetBackground(
                QPalette().color(QPalette.Dark).redF(), 
                QPalette().color(QPalette.Dark).greenF(), 
                QPalette().color(QPalette.Dark).blueF()
        )
        
        self.ren.SetBackground2(
                QPalette().color(QPalette.Window).redF(), 
                QPalette().color(QPalette.Window).greenF(), 
                QPalette().color(QPalette.Window).blueF()
        )

        self.ren.GradientBackgroundOn()

        self.actors = []
    
    def load(self, stlf, pos=(0, 0, 0)):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(stlf)
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        transform = vtk.vtkTransform()
        transform.Translate(*pos)
        actor.SetUserTransform(transform)

        self.ren.AddActor(actor)
        self.actors.append(actor)

        self.ren.ResetCamera()
        self.widget.GetRenderWindow().Render()

    def rotate(self, rot):
        if self.actors and len(rot) == 3:
            print(rot)

            for actor in self.actors:
                actor.SetOrientation(rot[1], rot[2], rot[0])

            self.widget.GetRenderWindow().Render()
    

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

        self.board = Serial("/dev/ttyACM0", 115200)  # Reemplaza con tu puerto y baudrate

        self.board.data.connect(self.serialEvent)
        self.board.start()
    
    @Slot(str)
    def serialEvent(self, data):
        self.vtk.rotate(data)

    def closeEvent(self, event):
        self.board.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    widget.vtk.load('base.stl', (0, 0, 0))

    sys.exit(app.exec())
