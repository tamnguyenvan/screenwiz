from PySide6.QtWidgets import QWidget, QPushButton, QMenu, QHBoxLayout, QLabel
from PySide6.QtGui import QAction, QPainterPath, QRegion, QTransform, QIcon, QPixmap
from PySide6.QtCore import QPoint, QRect, Signal

from views.widgets.custom_context_menu import CustomContextMenu
from views.widgets.button import SWButton


# class CustomMenu(QMenu):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setStyleSheet("""
#             QMenu::item {
#                 background-color: transparent;
#                 padding: 10px 20px;
#                 margin: 2px 0;
#             }
#             QMenu::item:selected {
#                 background-color: #4d5057;
#                 border-radius: 4px;
#             }
#             QMenu {
#                 icon-size: 24px;
#                 padding: 10px 10px;
#             }
#         """)

#     def resizeEvent(self, event):
#         path = QPainterPath()
#         rect = QRect(self.rect()).adjusted(.5, .5, -1.5, -1.5)
#         path.addRoundedRect(rect, 10, 10)
#         region = QRegion(path.toFillPolygon(QTransform()).toPolygon())
#         self.setMask(region)


class SWDropDown(SWButton):
    value_changed = Signal(str)

    def __init__(self, items, parent=None):
        super().__init__(
            icon=':/icons/ar_auto.svg',
            padding='8px 40px',
            text='Auto',
            background_color='#2e2e2e',
            hover_background_color='#212121',
            border_radius=10,
            parent=parent
        )
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

        self.menu = CustomContextMenu(
            parent=self
        )
        self.populate_menu()

    def populate_menu(self):
        for item in self.items:
            action = QAction(QIcon(self.icons.get(item, '')), item, self)
            action.triggered.connect(lambda checked, text=item: self.on_value_changed(text))
            self.menu.addAction(action)

    def on_value_changed(self, text):
        self.setIcon(QIcon(self.icons[text]))
        self.setText(text)
        self.value_changed.emit(text)

    def show_menu(self):
        button_pos = self.mapToGlobal(QPoint(0, self.height()))
        self.menu.exec(button_pos)