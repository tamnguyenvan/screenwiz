from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from views.widgets.color_widget import ColorWidget
from views.widgets.scroll_area import SWScrollArea
from views.studio.sidebar.background_setting import BackgroundSetting
from views.studio.sidebar.shape_setting import ShapeSetting
from views.studio.sidebar.zoom_setting import ZoomSetting
from utils.context_utils import AppContext


class SideBar(ColorWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()
        self.setFixedWidth(500)

        AppContext.get('view_model').zoom_track_selected.connect(self.on_zoom_track_selected)

    def init_ui(self):
        # Main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(0)

        # Wrap content with a scroll area
        self.scroll_area = SWScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Content widget
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)

        # Set content widget for the scroll area
        self.scroll_area.setWidget(self.content_widget)

        # Add sections to the content layout
        content_layout.addWidget(BackgroundSetting())
        content_layout.addWidget(ShapeSetting())

        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.setStyleSheet('''
        background-color: #131519;
        border-radius: 20px;
        ''')

    def on_zoom_track_selected(self, index):
        self.content_widget.deleteLater()

        new_content_widget = QWidget()
        new_content_layout = QVBoxLayout(new_content_widget)

        new_content_layout.addWidget(ZoomSetting())
        self.scroll_area.setWidget(new_content_widget)