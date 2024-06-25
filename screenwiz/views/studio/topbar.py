from PySide6.QtWidgets import (
    QWidget, QHBoxLayout
)

from views.widgets.custom_button import CustomButton


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()
        self.setFixedHeight(40)

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Widgets
        export_button = CustomButton(
            icon=':/icons/export.svg',
            text='Export',
            border_radius=10,
            font_size=14,
            font_weight=400,
            padding='0px 32px',
        )

        # Add the widgets to main layout
        main_layout.addStretch(1)
        main_layout.addWidget(export_button)

        self.setLayout(main_layout)