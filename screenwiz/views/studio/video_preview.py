from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from views.widgets.button import SWButton
from views.widgets.aspect_ratio_image import AspectRatioImage
from views.widgets.dropdown import SWDropDown
from utils.context_utils import AppContext


class VideoPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

        self.setMinimumWidth(500)

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # Top toolbar
        top_toolbar = VideoTopToolBar()
        top_toolbar.setFixedHeight(40)

        # Frame preview
        frame_preview = FramePreview()

        # Toolbar
        toolbar = VideoToolBar()
        toolbar.setFixedHeight(50)

        # Add the widgets to main layout
        main_layout.addWidget(top_toolbar)
        main_layout.addWidget(frame_preview)
        main_layout.addWidget(toolbar)

        self.setLayout(main_layout)


class FramePreview(QWidget):
    def __init__(self, frame=None, parent=None):
        super().__init__(parent=parent)

        self.frame = frame

        # Connect the frame changed signal to the update slot
        AppContext.get('view_model').on_frame_changed.connect(self.update_frame)

        self.init_ui()

        # Grab and display first frame
        AppContext.get('view_model').current_frame()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.frame_label = QLabel()
        self.frame_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.frame_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.frame_label)

        self.setLayout(main_layout)

    def update_frame(self, frame):
        self.frame = frame
        self.update()

    def update(self):
        if self.frame is not None:
            height, width, channels = self.frame.shape
            image = QImage(self.frame.data, width, height, width * channels, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(image)
            self.frame_label.setPixmap(pixmap.scaled(
                self.frame_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()  # Ensure the frame_label is updated with the new size


class VideoTopToolBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        items = [
            'Auto',
            '16:9',
            '9:16',
            '4:3',
            '1:1',
            '3:4',
        ]
        self.drop_down = SWDropDown(items=items, parent=self)
        self.drop_down.clicked.connect(self.drop_down.show_menu)
        self.drop_down.value_changed.connect(self.change_aspect_ratio)

        layout.addWidget(self.drop_down)
        self.setLayout(layout)

    def change_aspect_ratio(self, aspect_ratio):
        AppContext.get('view_model').update_aspect_ratio(aspect_ratio)


class VideoToolBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

        AppContext.get('view_model').on_playing_changed.connect(self.update_play_button_icon)

    def init_ui(self):
        view_model = AppContext.get('view_model')

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Group 1
        group_layout_1 = QHBoxLayout()
        group_layout_1.setContentsMargins(0, 0, 0, 0)
        group_layout_1.setSpacing(5)

        self.prev_button = SWButton(
            icon=':/icons/prev.svg',
            icon_size=(30, 30),
            background_color='transparent',
            hover_background_color='transparent'
        )
        self.play_button = SWButton(
            icon=':/icons/play.svg',
            icon_size=(30, 30),
            background_color='transparent',
            hover_background_color='transparent'
        )
        self.next_button = SWButton(
            icon=':/icons/next.svg',
            icon_size=(30, 30),
            background_color='transparent',
            hover_background_color='transparent'
        )

        self.play_button.clicked.connect(view_model.toggle_playing_video)
        self.next_button.clicked.connect(view_model.next_frame)
        self.prev_button.clicked.connect(view_model.prev_frame)

        group_layout_1.addWidget(self.prev_button)
        group_layout_1.addWidget(self.play_button)
        group_layout_1.addWidget(self.next_button)

        # Group 2
        group_layout_2 = QHBoxLayout()
        group_layout_2.setContentsMargins(0, 0, 0, 0)
        group_layout_2.setSpacing(5)

        prev_button = SWButton(
            icon=':/icons/cut.svg',
            icon_size=(26, 26),
            background_color='transparent',
            hover_background_color='transparent'
        )
        play_button = SWButton(
            icon=':/icons/scale.svg',
            icon_size=(30, 30),
            background_color='transparent',
            hover_background_color='transparent'
        )

        group_layout_2.addWidget(prev_button)
        group_layout_2.addWidget(play_button)

        main_layout.addStretch(2)
        main_layout.addLayout(group_layout_1)
        main_layout.addStretch(1)
        main_layout.addLayout(group_layout_2)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def update_play_button_icon(self, is_playing):
        if is_playing:
            self.play_button.set_icon(':/icons/pause.svg')
        else:
            self.play_button.set_icon(':/icons/play.svg')