from PySide6.QtWidgets import (
    QGridLayout, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy
)
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import QSize

from views.widgets.tabview import SWTabView
from views.widgets.button import SWButton, RoundedImageButton
from utils.context_utils import AppContext


class ZoomSetting(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Back button
        back_button = SWButton(
            icon=':/icons/back.svg',
            icon_size=(30, 30),
            border_radius=15,
            background_color='transparent',
            hover_background_color='#222222'
        )

        main_layout.addWidget(back_button)
        main_layout.addStretch(1)

        self.setLayout(main_layout)