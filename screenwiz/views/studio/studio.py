from PySide6.QtWidgets import (
    QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
)

from views.studio.topbar import TopBar
from views.studio.video_preview import VideoPreview
from views.studio.sidebar import SideBar
from views.studio.video_edit import VideoEdit
from views.widgets.color_widget import ColorWidget
from utils.context_utils import AppContext
from config import config


class StudioWindow(ColorWidget):
    def __init__(self, view_model=None, parent=None):
        super().__init__(parent=parent)

        self.setObjectName('studio')

        AppContext.set('view_model', view_model)

        self.init_ui()
        self.load()

        minimum_size = (
            config['window']['minimum_width'],
            config['window']['minimum_height']
        )
        self.setWindowTitle('ScreenWiz')
        self.setMinimumSize(*minimum_size)
        self.showMaximized()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Top bar
        self.topbar = TopBar()

        # Content
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)

        self.video_preview = VideoPreview()
        self.sidebar = SideBar()

        content_layout.addWidget(self.video_preview)
        content_layout.addWidget(self.sidebar)

        # Video edit
        self.video_edit = VideoEdit()

        # Add the widgets to main layout
        main_layout.addWidget(self.topbar)
        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.video_edit)

        self.setLayout(main_layout)

    def load(self):
        # Load data and refresh the UI
        AppContext.get('view_model').load()