from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QSizePolicy
)

from views.widgets.custom_button import CustomButton
from config import config
from views.widgets.color_widget import ColorWidget


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.config = config['layout']['topbar']

        self.init_ui()
        self.setFixedHeight(self.config['height'])

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Widgets
        export_button = CustomButton(
            icon=':/icons/export.svg',
            icon_size=(24, 24),
            text='Export',
            border_radius=10,
            font_size=14,
            font_weight=400,
            padding='8px 20px',
        )
        export_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        # Add the widgets to main layout
        main_layout.addStretch(1)
        main_layout.addWidget(export_button)

        self.setLayout(main_layout)