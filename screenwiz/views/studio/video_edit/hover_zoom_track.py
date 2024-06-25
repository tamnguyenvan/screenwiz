from PySide6.QtWidgets import QHBoxLayout, QLabel
from PySide6.QtCore import Qt

from views.widgets.color_widget import ColorWidget
from views.widgets.icon import Icon


class HoverZoomTrack(ColorWidget):
    def __init__(self, color='#5A46E2', border_radius=12, parent=None):
        super().__init__(parent=parent)

        self.color = color
        self.border_radius = border_radius
        self.setFixedSize(200, 60)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = Icon(':/icons/add.svg')
        layout.addWidget(icon)
        self.setLayout(layout)

        self.setStyleSheet(f'''
        background-color: {self.color};
        border-radius: {self.border_radius};
        ''')