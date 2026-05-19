import json
import os
import uuid
from datetime import datetime

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
    QMessageBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


MENU_ITEMS = [
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

ITEM_PRICES = {
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

APP_STYLE = """
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
QFrame#itemCard,
QFrame#orderCard {
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
QPushButton#minusButton,
QPushButton#sendOrderButton,
QPushButton#confirmButton,
QPushButton#refreshButton {
    color: #fff9f0;
    border: none;
    border-radius: 14px;
    min-height: 32px;
    font-size: 14px;
    font-weight: 700;
}
QPushButton#plusButton {
    background: #dc6d3d;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    font-size: 18px;
}
QPushButton#plusButton:hover {
    background: #c85c2f;
}
QPushButton#minusButton {
    background: #8a3b2c;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    font-size: 18px;
}
QPushButton#minusButton:hover {
    background: #6f2f23;
}
QPushButton#sendOrderButton {
    background: #c85c2f;
}
QPushButton#sendOrderButton:hover {
    background: #a54822;
}
QPushButton#confirmButton {
    background: #8a3b2c;
    min-width: 140px;
}
QPushButton#confirmButton:hover {
    background: #6f2f23;
}
QPushButton#refreshButton {
    background: #dc6d3d;
    min-width: 120px;
}
QPushButton#refreshButton:hover {
    background: #c85c2f;
}
QFrame#cartPanel,
QFrame#queuePanel {
    background: #452013;
    border-radius: 20px;
}
QLabel#cartTitle,
QLabel#queueTitle {
    color: #ffd5b8;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.8px;
    background: #452013;
}
QLabel#cartBody,
QLabel#queueBody {
    color: #fff6eb;
    background: #5b2d1d;
    border: 1px solid #7a4d39;
    border-radius: 12px;
    padding: 12px;
    font-family: "Consolas";
    font-size: 13px;
}
QLabel#statusLabel {
    color: #ffd5b8;
    background: #452013;
    font-size: 12px;
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
QLabel#splashBanner {
    background: rgba(64, 31, 18, 225);
    color: #ffd5b8;
    border-radius: 22px;
    padding: 24px;
    font-size: 30px;
    font-weight: 700;
}
"""


def orders_file_path():
    return os.path.join(os.path.dirname(__file__), "orders.json")


def order_counter_file_path():
    return os.path.join(os.path.dirname(__file__), "order_counter.txt")


def load_orders(file_path):
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_orders(file_path, orders):
    with open(file_path, "w", encoding="utf-8") as file_handle:
        json.dump(orders, file_handle, indent=2)


def load_order_counter(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            return int(file_handle.read().strip())
    except (OSError, ValueError):
        return None


def save_order_counter(file_path, next_order_number):
    with open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(next_order_number))


def normalize_order_numbers(orders, start_number=59):
    used_numbers = set()
    changed = False
    next_number = start_number

    for order in orders:
        existing_number = order.get("order_number")
        if isinstance(existing_number, str) and existing_number.isdigit():
            number_value = int(existing_number)
            used_numbers.add(number_value)
            if number_value >= next_number:
                next_number = number_value + 1
            continue

        while next_number in used_numbers:
            next_number += 1

        order["order_number"] = f"{next_number:02d}"
        used_numbers.add(next_number)
        next_number += 1
        changed = True

    if used_numbers:
        next_number = max(used_numbers) + 1

    if next_number < start_number:
        next_number = start_number

    return orders, next_number, changed


def build_order_snapshot(items_state, item_prices, order_number):
    ordered_items = []
    total_items = 0
    total_amount = 0

    for item_name, quantity in items_state.items():
        if quantity > 0:
            item_total = item_prices[item_name] * quantity
            ordered_items.append(
                {
                    "name": item_name,
                    "quantity": quantity,
                    "price": item_prices[item_name],
                    "total": item_total,
                }
            )
            total_items += quantity
            total_amount += item_total

    if not ordered_items:
        return None

    return {
        "id": uuid.uuid4().hex,
        "order_number": f"{order_number:02d}",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": ordered_items,
        "total_items": total_items,
        "grand_total": total_amount,
    }


def format_order_text(order):
    lines = []
    for item in order.get("items", []):
        lines.append(
            f"{item['name'].title():<18} x {item['quantity']:<2}  ₹{item['total']}"
        )

    lines.append("")
    lines.append(f"Order Number: {order.get('order_number', '')}")
    lines.append(f"Order ID: {order.get('id', '')}")
    lines.append(f"Placed At: {order.get('created_at', '')}")
    lines.append(f"Total Items: {order.get('total_items', 0)}")
    lines.append(f"Grand Total: ₹{order.get('grand_total', 0)}")
    return "\n".join(lines)


class OrderQueueWindow(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setWindowTitle("Order Queue")
        self.resize(640, 760)
        self.setStyleSheet(APP_STYLE)

        self.title = QLabel("Order Queue")
        self.title.setObjectName("queueTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel("Pending orders stored in the queue file")
        self.subtitle.setObjectName("headerTagline")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.queue_body = QWidget()
        self.queue_layout = QVBoxLayout(self.queue_body)
        self.queue_layout.setContentsMargins(10, 10, 10, 10)
        self.queue_layout.setSpacing(12)
        self.queue_layout.setAlignment(Qt.AlignTop)

        self.queue_scroll = QScrollArea()
        self.queue_scroll.setWidgetResizable(True)
        self.queue_scroll.setWidget(self.queue_body)

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.clicked.connect(self.refresh_orders)

        header_row = QHBoxLayout()
        header_row.addStretch()
        header_row.addWidget(self.refresh_button)
        header_row.addStretch()

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addLayout(header_row)
        layout.addWidget(self.queue_scroll, 1)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.refresh_orders()

    def refresh_orders(self):
        orders = load_orders(self.file_path)
        normalized_orders, next_order_number, changed = normalize_order_numbers(orders)
        if changed:
            save_orders(self.file_path, normalized_orders)
        self.next_order_number = next_order_number

        while self.queue_layout.count():
            item = self.queue_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if not orders:
            empty_label = QLabel("No pending orders")
            empty_label.setObjectName("queueBody")
            empty_label.setAlignment(Qt.AlignCenter)
            self.queue_layout.addWidget(empty_label)
            self.status_label.setText("0 pending orders")
            return

        for order in orders:
            card = QFrame()
            card.setObjectName("orderCard")

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 12, 12, 12)
            card_layout.setSpacing(8)

            order_text = QLabel(format_order_text(order))
            order_text.setObjectName("queueBody")
            order_text.setWordWrap(True)

            confirm_button = QPushButton("Order Confirmed")
            confirm_button.setObjectName("confirmButton")
            confirm_button.clicked.connect(
                lambda _, order_id=order["id"]: self.confirm_order(order_id)
            )

            card_layout.addWidget(order_text)
            card_layout.addWidget(confirm_button, 0, Qt.AlignRight)
            self.queue_layout.addWidget(card)

        self.queue_layout.addStretch()
        self.status_label.setText(f"{len(orders)} pending order(s)")

    def confirm_order(self, order_id):
        orders = load_orders(self.file_path)
        remaining_orders = [order for order in orders if order.get("id") != order_id]

        if len(remaining_orders) == len(orders):
            return

        save_orders(self.file_path, remaining_orders)
        self.refresh_orders()


class CanteenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Food Kiosk")
        self.resize(1300, 780)
        self.setMinimumSize(1300, 680)
        self.setStyleSheet(APP_STYLE)

        self.order_file_path = orders_file_path()
        self.order_counter_path = order_counter_file_path()
        self.next_order_number = 59
        self.order_window = None

        self.header_title = QLabel("PCCOER Canteen")
        self.header_title.setObjectName("headerTitle")
        self.header_title.setAlignment(Qt.AlignCenter)

        self.header_tagline = QLabel("Give me your moneyyyy-Mr. Krabs")
        self.header_tagline.setObjectName("headerTagline")
        self.header_tagline.setAlignment(Qt.AlignCenter)

        self.items = list(MENU_ITEMS)
        self.item_prices = ITEM_PRICES
        self.buttons_dict = {item: 0 for item in self.items}

        self.cart_text = "No items yet"
        self.amt_labels = {}

        self.cart_title = QLabel("Your Cart")
        self.cart_title.setObjectName("cartTitle")
        self.cart_body = QLabel(self.cart_text)
        self.cart_body.setObjectName("cartBody")
        self.cart_body.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.cart_body.setWordWrap(True)

        self.send_order_button = QPushButton("Send Order")
        self.send_order_button.setObjectName("sendOrderButton")
        self.send_order_button.clicked.connect(self.send_order)

        self.order_status = QLabel("Send the current cart to the order queue.")
        self.order_status.setObjectName("statusLabel")
        self.order_status.setAlignment(Qt.AlignCenter)

        self.splash_banner = QLabel("", self)
        self.splash_banner.setObjectName("splashBanner")
        self.splash_banner.setAlignment(Qt.AlignCenter)
        self.splash_banner.hide()

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
        cart_layout.addWidget(self.send_order_button)
        cart_layout.addWidget(self.order_status)
        cart_panel.setLayout(cart_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)
        content_layout.addWidget(menu_scroll, 7)
        content_layout.addWidget(cart_panel, 3)

        self.master_layout = QVBoxLayout()
        self.master_layout.setSpacing(14)
        self.master_layout.setContentsMargins(16, 14, 16, 16)
        self.master_layout.addWidget(self.header_title)
        self.master_layout.addWidget(self.header_tagline)
        self.master_layout.addLayout(content_layout, 1)

        self.setLayout(self.master_layout)

        self.refresh_order_counter()
        QTimer.singleShot(0, self.show_order_window)

    def refresh_order_counter(self):
        orders = load_orders(self.order_file_path)
        normalized_orders, next_order_number, changed = normalize_order_numbers(orders)
        if changed:
            save_orders(self.order_file_path, normalized_orders)

        stored_counter = load_order_counter(self.order_counter_path)
        if stored_counter is None or stored_counter < next_order_number:
            stored_counter = next_order_number
            save_order_counter(self.order_counter_path, stored_counter)

        self.next_order_number = stored_counter

    def build_item_card(self, item):
        card = QFrame()
        card.setObjectName("itemCard")

        food_pic = QLabel()
        food_pic.setObjectName("foodImage")
        food_pic.setAlignment(Qt.AlignCenter)
        image_path = os.path.join(os.path.dirname(__file__), "images", f"{item}.png")
        pixmap = QPixmap(image_path)
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

    def build_cart_snapshot(self):
        return build_order_snapshot(
            self.buttons_dict,
            self.item_prices,
            self.next_order_number,
        )

    def allocate_order_number(self):
        order_number = self.next_order_number
        self.next_order_number += 1
        save_order_counter(self.order_counter_path, self.next_order_number)
        return order_number

    def clear_cart(self):
        for key in self.buttons_dict:
            self.buttons_dict[key] = 0
            self.amt_labels[key].setText("0")

        self.cart_text = "No items yet"
        self.cart_body.setText(self.cart_text)

    def show_order_window(self):
        if self.order_window is None:
            self.order_window = OrderQueueWindow(self.order_file_path)
        else:
            self.order_window.refresh_orders()

        self.order_window.show()

    def show_confirmation_splash(self, order_number):
        self.splash_banner.setText(f"Order confirmed!\nOrder number: {order_number:02d}")
        banner_width = min(820, self.width() - 80)
        banner_height = 170
        banner_x = max(40, (self.width() - banner_width) // 2)
        banner_y = max(80, (self.height() - banner_height) // 2)
        self.splash_banner.setGeometry(banner_x, banner_y, banner_width, banner_height)
        self.splash_banner.raise_()
        self.splash_banner.show()
        QTimer.singleShot(1800, self.splash_banner.hide)

    def send_order(self):
        order_number = self.allocate_order_number()
        order = self.build_cart_snapshot()

        if order is None:
            self.next_order_number -= 1
            save_order_counter(self.order_counter_path, self.next_order_number)
            QMessageBox.information(
                self,
                "No order",
                "Add at least one item before sending the order.",
            )
            return

        order["order_number"] = f"{order_number:02d}"

        orders = load_orders(self.order_file_path)
        orders.append(order)
        save_orders(self.order_file_path, orders)

        self.clear_cart()
        self.order_status.setText(f"Order sent at {order['created_at']}")
        self.show_confirmation_splash(order_number)
        self.show_order_window()

    def update_item(self, item):
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
