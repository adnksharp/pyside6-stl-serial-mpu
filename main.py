import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PySide6.QtGui import QPalette
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

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

    widget.vtk.load('base.stl', (0, 0, 0))

    sys.exit(app.exec())
