from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QScrollArea,
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class CanteenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Food Kiosk")
        self.resize(1300, 780)
        self.setMinimumSize(1300, 680)
        self.setStyleSheet(
            """
            QWidget {
                background: #f7efe2;
                color: #2f241f;
                font-family: "Trebuchet MS";
            }
            QLabel#headerTitle {
                color: #401f12;
                font-size: 44px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            QLabel#headerTagline {
                color: #8f5d3f;
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            QFrame#itemCard {
                background: #fff8ef;
                border: 2px solid #e6c4a2;
                border-radius: 18px;
            }
            QLabel#itemName {
                color: #4c2f20;
                background: #fff8ef;
                border: none;
                font-size: 14px;
                font-weight: 700;
            }
            QLabel#foodImage {
                background: #fff8ef;
                border: none;
            }
            QLabel#qtyLabel {
                min-width: 38px;
                color: #4c2f20;
                background: #fff8ef;
                border: none;
                font-size: 18px;
                font-weight: 700;
                qproperty-alignment: AlignCenter;
            }
            QPushButton#plusButton,
            QPushButton#minusButton {
                color: #fff9f0;
                border: none;
                border-radius: 14px;
                min-height: 28px;
                max-height: 28px;
                min-width: 28px;
                max-width: 28px;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton#plusButton {
                background: #dc6d3d;
            }
            QPushButton#plusButton:hover {
                background: #c85c2f;
            }
            QPushButton#minusButton {
                background: #8a3b2c;
            }
            QPushButton#minusButton:hover {
                background: #6f2f23;
            }
            QFrame#cartPanel {
                background: #452013;
                border-radius: 20px;
            }
            QLabel#cartTitle {
                color: #ffd5b8;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 0.8px;
                background: #452013;
            }
            QLabel#cartBody {
                color: #fff6eb;
                background: #5b2d1d;
                border: 1px solid #7a4d39;
                border-radius: 12px;
                padding: 12px;
                font-family: "Consolas";
                font-size: 13px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #edd7c0;
                width: 10px;
                border-radius: 5px;
                margin: 8px 0 8px 0;
            }
            QScrollBar::handle:vertical {
                background: #c07a52;
                border-radius: 5px;
                min-height: 20px;
            }
            """
        )

        # Header widgets.
        self.header_title = QLabel("PCCOER Canteen")
        self.header_title.setObjectName("headerTitle")
        self.header_title.setAlignment(Qt.AlignCenter)

        self.header_tagline = QLabel("Give me your moneyyyy-Mr. Krabs")
        self.header_tagline.setObjectName("headerTagline")
        self.header_tagline.setAlignment(Qt.AlignCenter)

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

        self.item_prices = {
            "burger": 120,
            "fries": 80,
            "grilled sandwich": 130,
            "veg sandwich": 110,
            "cheese sandwich": 140,
            "pizza": 180,
            "brownie": 90,
            "paneer pizza": 220,
            "cheese pizza": 230,
            "pasta": 170,
            "white sauce pasta": 190,
            "hakka noodles": 160,
        }

        self.buttons_dict = {item: 0 for item in self.items}

        self.cart_text = "No items yet"
        self.amt_labels = {}

        self.cart_title = QLabel("Your Cart")
        self.cart_title.setObjectName("cartTitle")
        self.cart_body = QLabel(self.cart_text)
        self.cart_body.setObjectName("cartBody")
        self.cart_body.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.cart_body.setWordWrap(True)

        self.grid = QGridLayout()
       

        row = 0
        col = 0

        for item in self.items:
            card = self.build_item_card(item)
            self.grid.addWidget(card, row, col)

            col += 1

            if col > 3:
                col = 0
                row += 1

        menu_container = QWidget()
        menu_container.setLayout(self.grid)

        menu_scroll = QScrollArea()
        menu_scroll.setWidgetResizable(True)
        menu_scroll.setWidget(menu_container)

        cart_panel = QFrame()
        cart_panel.setObjectName("cartPanel")
        cart_layout = QVBoxLayout()
        cart_layout.setContentsMargins(18, 18, 18, 18)
        cart_layout.setSpacing(10)
        cart_layout.addWidget(self.cart_title)
        cart_layout.addWidget(self.cart_body, 1)
        cart_panel.setLayout(cart_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)
        content_layout.addWidget(menu_scroll, 7)
        content_layout.addWidget(cart_panel, 3)

        #master layout finally
        self.master_layout = QVBoxLayout()
        self.master_layout.setSpacing(14)
        self.master_layout.setContentsMargins(16, 14, 16, 16)
        self.master_layout.addWidget(self.header_title)
        self.master_layout.addWidget(self.header_tagline)
        self.master_layout.addLayout(content_layout, 1)

        self.setLayout(self.master_layout)

    def build_item_card(self, item):
        card = QFrame()
        card.setObjectName("itemCard")

        food_pic = QLabel()
        food_pic.setObjectName("foodImage")
        food_pic.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(f"fast_food_kiosk/images/{item}.png")
        food_pic.setPixmap(
            pixmap.scaled(170, 170, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        item_name = QLabel(item.title())
        item_name.setObjectName("itemName")
        item_name.setAlignment(Qt.AlignCenter)

        plus_btn = QPushButton("+")
        plus_btn.setObjectName("plusButton")
        plus_btn.clicked.connect(lambda _, i=item: self.update_item(i + "+"))

        amt_label = QLabel("0")
        amt_label.setObjectName("qtyLabel")
        self.amt_labels[item] = amt_label

        minus_btn = QPushButton("-")
        minus_btn.setObjectName("minusButton")
        minus_btn.clicked.connect(lambda _, i=item: self.update_item(i + "-"))

        amt_row = QHBoxLayout()
        amt_row.setContentsMargins(10, 0, 10, 8)
        amt_row.addStretch()
        amt_row.addWidget(minus_btn)
        amt_row.addWidget(amt_label)
        amt_row.addWidget(plus_btn)
        amt_row.addStretch()

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(12, 12, 12, 8)
        card_layout.setSpacing(6)
        card_layout.addWidget(food_pic)
        card_layout.addWidget(item_name)
        card_layout.addLayout(amt_row)
        card.setLayout(card_layout)
        return card

    def update_item(self, item):
        # Event payload uses the format "item+" or "item-".
        name = item[:-1]
        if item[-1] == "+":
            self.buttons_dict[name] += 1
        elif not self.buttons_dict[name] == 0:
            self.buttons_dict[name] -= 1

        lines = []
        total_items = 0
        total_amount = 0
        for key, val in self.buttons_dict.items():
            if val > 0:
                item_total = self.item_prices[key] * val
                lines.append(f"{key.title():<18} x {val:<2}  ₹{item_total}")
                total_items += val
                total_amount += item_total

        if lines:
            self.cart_text = "\n".join(lines)
            self.cart_text += f"\n\nTotal Items: {total_items}"
            self.cart_text += f"\nGrand Total: ₹{total_amount}"
        else:
            self.cart_text = "No items yet"

        self.amt_labels[name].setText(str(self.buttons_dict[name]))
        self.cart_body.setText(self.cart_text)


if __name__ == "__main__":
    app = QApplication([])
    window = CanteenApp()
    window.show()
    app.exec_()
