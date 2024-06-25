from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize


class Icon(QLabel):
    def __init__(self, icon_path, size=(24, 24), parent=None):
        super().__init__(parent=parent)

        self.icon_path = icon_path
        if isinstance(size, (tuple, list)):
            self.size = QSize(*size)

        pixmap = QPixmap(icon_path)
        self.setPixmap(pixmap.scaled(self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))