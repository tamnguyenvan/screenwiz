from PySide6.QtWidgets import QWidget, QLabel


class TimeIndicator(QWidget):
    def __init__(self, color='white', parent=None):
        super().__init__(parent=parent)

        self.color = color

        width = 16
        height = 220

        self.setFixedSize(width, height)

        self.init_ui()

    def init_ui(self):

        top_label = QLabel(self)
        top_label.setFixedSize(self.width(), self.width())
        top_label.setStyleSheet(f"""
            border-radius: 8px;
            background-color: {self.color};
        """)
        top_label.move(0, 0)

        vertical_bar_width = 2
        vertical_bar = QLabel(self)
        vertical_bar.setFixedSize(vertical_bar_width, self.height())
        vertical_bar.move((self.width() - vertical_bar_width) // 2, 0)
        vertical_bar.setStyleSheet(f'background-color: {self.color};')