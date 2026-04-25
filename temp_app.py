from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QLineEdit,QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import subprocess


class CanteenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Canteen App")
        self.resize(400, 300)

        # widgets
        self.header = QLabel("PCCOE&R Canteen")
        self.header.setFont(QFont("Comic Sans MS", 20))

        ""
        self.items = [
            "burger",
            "fries",
            "grilled sandwich",
            "veg sandwich",
            "cheese sandwich",
            "pizza",
            "brownie",
            "paneer pizza",
            "cheese pizza",
            "pasta",
            "white sauce pasta",
            "hakka noodles",
        ]

        self.buttons_dict = {item: 0 for item in self.items}

        self.cart_text = "Cart"
        self.amt_labels = {}

        self.cart = QLabel()

        # layout
        self.grid = QGridLayout()

        row = 0
        col = 0

        for item in self.items:
            food_pic = QLabel(item)
            food_pic.setPixmap(
                QPixmap(f"codes/python_mini_project/images/{item}.png").scaled(160, 160)
            )

            # + button
            plus_btn = QPushButton("+")
            plus_btn.clicked.connect(lambda _, i=item: self.update_item(i + "+"))
            amt_label = QLabel("0")
            self.amt_labels[item] = amt_label
            amt_label.setAlignment(Qt.AlignCenter)
            # - button
            minus_btn = QPushButton("-")
            minus_btn.clicked.connect(lambda _, i=item: self.update_item(i + "-"))

            amt_but = QHBoxLayout()
            amt_but.addWidget(plus_btn)
            amt_but.addWidget(amt_label)
            amt_but.addWidget(minus_btn)

            pic_but = QVBoxLayout()
            pic_but.addWidget(food_pic)
            pic_but.addLayout(amt_but)

            self.grid.addLayout(pic_but, row, col)

            col += 1

            if col > 3:
                col = 0
                row += 1

        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.master_layout = QVBoxLayout()
        self.master_layout.addWidget(self.header, 3)
        self.master_layout.addLayout(self.grid, 5)
        self.master_layout.addWidget(self.cart, 2)
        self.master_layout.setSpacing(15)

        self.setLayout(self.master_layout)

    def update_item(self, item):
        name = item[:-1]
        if item[-1] == "+":
            self.buttons_dict[name] += 1
        elif not self.buttons_dict[name] == 0:
            self.buttons_dict[name] -= 1
        self.cart_text = "Cart\n"
        for key, val in self.buttons_dict.items():
            if val > 0:
                self.cart_text += f"{key} : {val}\n"
        self.amt_labels[name].setText(str(self.buttons_dict[name]))
        self.cart.setText(self.cart_text)


if __name__ == "__main__":
    subprocess.run("clear", shell=True)
    app = QApplication([])
    window = CanteenApp()
    window.show()
    app.exec_()
