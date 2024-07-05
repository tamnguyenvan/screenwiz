from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider
from PySide6.QtGui import QWheelEvent


class SWSlider(QSlider):
    def __init__(
        self,
        orientation=Qt.Orientation.Horizontal,
        color='#3B25D1',
        handle_color='#3B25D1',
        parent=None
    ):
        super().__init__(orientation, parent)

        self.color = color
        self.handle_color = handle_color

        self.init_ui()

        self.setMinimumHeight(50)

    def init_ui(self):
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: 1px solid #4d5057;
                height: 2px;
                background-color: #4d5057;
                border-radius: 2px;
            }}

            QSlider::sub-page:horizontal {{
                background-color: {self.handle_color};
                border: 1px solid {self.handle_color};
                height: 2px;
                border-radius: 2px;
            }}

            QSlider::handle:horizontal {{
                background-color: {self.color};
                border: 1px solid {self.color};
                width: 24px;
                height: 24px;
                margin: -12px 0;
                border-radius: 12px;
            }}

            QSlider::handle:horizontal:pressed {{
                background-color: #E8EAED;
                border: 1px solid #E8EAED;
            }}
        """)

    def wheelEvent(self, event: QWheelEvent):
        event.ignore()