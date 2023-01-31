# Note: This was written by chatgpt...I haven't had a chance to run it yet. It will also require a csv file with timestamps and x,y,z positions.
# If this actually runs, that will be rather insane

import sys
import csv
from PyQt6 import QtWidgets
from PyQt6.Qt3DCore import Qt3DCore
from PyQt6.Qt3DExtras import Qt3DExtras
from PyQt6.QtCore import QTimer, QPropertyAnimation, QSequentialAnimationGroup
from PyQt6.QtGui import QVector3D

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = Qt3DExtras.Qt3DWindow()
        self.view.defaultFrameGraph().setClearColor(QtGui.QColor(0, 0, 0))
        self.container = Qt3DCore.QEntity()
        self.view.setRootEntity(self.container)

        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
        self.camera.setPosition(QVector3D(0.0, 0.0, 40.0))
        self.camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))

        self.light = Qt3DCore.QPointLight(self.container)
        self.light.setColor("white")
        self.light.setIntensity(1)

        self.sphere = Qt3DExtras.QSphereMesh()
        self.sphere.setRadius(5)

        self.sphere_transform = Qt3DCore.QTransform()
        self.sphere_entity = Qt3DCore.QEntity(self.container)
        self.sphere_entity.addComponent(self.sphere)
        self.sphere_entity.addComponent(self.sphere_transform)

        self.read_positions()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)

    def read_positions(self):
        self.positions = []
        with open("positions.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                self.positions.append(QVector3D(float(row[1]), float(row[2]), float(row[3])))
        self.current_frame = 0

    def update_position(self):
        self.current_position = self.positions[self.current_frame % len(self.positions)]
        self.current_frame += 1
        self.sphere_transform.setTranslation(self.current_position)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
