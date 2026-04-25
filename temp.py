from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

# Create label
label = QLabel()

# Load image
pixmap = QPixmap("codes/python_mini_project/mule.png")  # path to your image
label.setPixmap(pixmap)

layout.addWidget(label)
window.setLayout(layout)

window.show()
app.exec_()