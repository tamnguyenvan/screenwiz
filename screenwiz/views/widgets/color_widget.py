from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt


class ColorWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent)

        self.setAttribute(Qt.WA_StyledBackground, True)

        background_color = kwargs.get('color', 'transparent')
        self.setStyleSheet(f'background-color: {background_color}')