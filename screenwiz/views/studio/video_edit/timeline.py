from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget

from utils.context_utils import AppContext
from config import config


class Timeline(QWidget):
    def __init__(self, video_len=0, pixels_per_second=200, parent=None):
        super().__init__(parent=parent)

        self.config = config['objects']['timeline']

        self.video_len = video_len
        self.pixels_per_second = pixels_per_second
        self.video_len_int = int(video_len) + 1

        self.setFixedHeight(self.config['height'])
        self.init_ui()

        AppContext.get('view_model').on_video_len_changed.connect(self.update_video_len)
        # AppContext.get('view_model').on_video_len_changed.connect(self.update_pixels_per_second)

    def init_ui(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        for i in range(self.video_len_int):
            item = TimelineItem(i)
            item.setFixedWidth(self.pixels_per_second)
            self.main_layout.addWidget(item)

        self.setLayout(self.main_layout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # TODO: fix the x position
        x_pos = event.position().toPoint().x()

        # Update the frame and the slider's position
        AppContext.get('view_model').update_frame_based_on_position(x_pos)
        AppContext.get('view_model').update_slider_position(x_pos)

    def update_video_len(self, video_len):
        self.video_len = video_len
        self.video_len_int = int(video_len) + 1

        # Clear current items
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().deleteLater()

        # Add new items
        for i in range(self.video_len_int):
            item = TimelineItem(i)
            item.setFixedWidth(self.pixels_per_second)
            self.main_layout.addWidget(item)

    def update_pixels_per_second(self, pixels_per_second):
        self.pixels_per_second = pixels_per_second

        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i).widget()
            item.setFixedWidth(self.pixels_per_second)


class TimelineItem(QWidget):
    def __init__(self, second, parent=None):
        super().__init__(parent=parent)

        self.second = second

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        label = QLabel(str(self.second))
        dot = QLabel()
        dot.setFixedSize(4, 4)
        dot.setStyleSheet('background-color: darkgray; border-radius: 2px;')

        main_layout.addWidget(label)
        main_layout.addWidget(dot)

        self.setLayout(main_layout)