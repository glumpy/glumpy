# -----------------------------------------------------------------------------
# Glumpy / Qt5 integration example (c) LeMinaw, 2020
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
from glumpy import app
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton


app.use("qt5")
window = app.Window()

qwindow = QMainWindow()
widget = QWidget()
button = QPushButton("Press me!")
qwindow.setCentralWidget(widget)
widget.setLayout(QVBoxLayout())
widget.layout().addWidget(window._native_window)
widget.layout().addWidget(button)


@window.event
def on_draw(dt):
    window.clear()


@button.clicked.connect
def on_click():
    window.color = np.random.rand(4)


qwindow.show()
app.run()
