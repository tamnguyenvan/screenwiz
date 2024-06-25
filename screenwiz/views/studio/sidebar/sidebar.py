from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from views.widgets.color_widget import ColorWidget
from views.widgets.custom_scrollarea import CustomScrollArea
from views.studio.sidebar.background_setting import BackgroundSetting
from views.studio.sidebar.shape_setting import ShapeSetting


class SideBar(ColorWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()
        self.setFixedWidth(500)
        self.apply_styles()

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # Wrap content with a scroll area
        scroll_area = CustomScrollArea()
        scroll_area.setWidgetResizable(True)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Set content widget for the scroll area
        scroll_area.setWidget(content_widget)

        # Add sections to the content layout
        content_layout.addWidget(BackgroundSetting())
        content_layout.addWidget(ShapeSetting())

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet('''
        background-color: #131519;
        border-radius: 20px;
        ''')