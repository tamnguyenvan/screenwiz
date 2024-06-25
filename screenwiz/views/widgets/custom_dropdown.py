from PySide6.QtWidgets import QWidget, QPushButton, QMenu, QHBoxLayout, QLabel
from PySide6.QtGui import QAction, QPainterPath, QRegion, QTransform, QIcon, QPixmap
from PySide6.QtCore import QPoint, QRect, Signal

from views.widgets.custom_context_menu import CustomContextMenu


class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenu::item {
                background-color: transparent;
                padding: 10px 80px;
                margin: 2px 0;
            }
            QMenu::item:selected {
                background-color: #4d5057;
                border-radius: 4px;
            }
            QMenu {
                icon-size: 24px;
                padding: 10px 10px;
            }
        """)

    def resizeEvent(self, event):
        path = QPainterPath()
        rect = QRect(self.rect()).adjusted(.5, .5, -1.5, -1.5)
        path.addRoundedRect(rect, 10, 10)
        region = QRegion(path.toFillPolygon(QTransform()).toPolygon())
        self.setMask(region)


class DropDown(QPushButton):
    value_changed = Signal(str)

    def __init__(self, items, icon_path=None, parent=None):
        super().__init__(parent)
        self.items = items
        self.icons = {
            'Auto': ':/icons/ar_auto.svg',
            '16:9': ':/icons/ar_16_9.svg',
            '9:16': ':/icons/ar_9_16.svg',
            '4:3': ':/icons/ar_4_3.svg',
            '1:1': ':/icons/ar_1_1.svg',
            '3:4': ':/icons/ar_3_4.svg'
        }
        self.setObjectName('dropdown')

        self.menu = CustomMenu(self)
        self.populate_menu()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.icon_label = QLabel()
        pixmap = QPixmap(self.icons['Auto'])
        self.icon_label.setPixmap(pixmap)
        layout.addWidget(self.icon_label)

        self.text_label = QLabel(self.items[0])
        layout.addWidget(self.text_label)

        container = QWidget()
        container.setLayout(layout)

        self.setLayout(layout)

        self.setStyleSheet("""
            QPushButton#dropdown {
                padding: 20px 100px;
                border: none;
            }
        """)

    def populate_menu(self):
        for item in self.items:
            action = QAction(QIcon(self.icons.get(item, '')), item, self)
            action.triggered.connect(lambda checked, text=item: self.on_value_changed(text))
            self.menu.addAction(action)

    def on_value_changed(self, text):
        pixmap = QPixmap(self.icons[text])
        self.icon_label.setPixmap(QPixmap(pixmap))
        self.text_label.setText(text)
        self.value_changed.emit(text)

    def show_menu(self):
        button_pos = self.mapToGlobal(QPoint(0, self.height()))
        self.menu.exec(button_pos)