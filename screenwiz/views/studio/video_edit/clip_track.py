from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtGui import QMouseEvent, QCursor, QResizeEvent, QPainterPath, QPainter, QColor, QAction, QIcon
from PySide6.QtCore import Qt, QSize, QRectF

from views.widgets.icon import Icon
from views.widgets.color_widget import ColorWidget
from utils.context_utils import AppContext
from config import config


class ClipTrack(QWidget):
    def __init__(self, size=None, parent=None):
        super().__init__(parent=parent)

        self.config = config['elements']['clip_track']

        if size is None:
            size = QSize(0, 60)
        elif isinstance(size, (tuple, list)):
            size = QSize(*size)

        self.strip_width = self.config['strip_width']
        self.border_radius = self.config['border_radius']
        self.background_color = QColor('#bb86fc')
        self.color = '#ffffff'
        self.strip_color = QColor('#457b9d')

        self.setFixedSize(size)

        self.init_ui()

        AppContext.get('view_model').on_video_len_changed.connect(self.update_clip_width)

    def init_ui(self):
        layout = QVBoxLayout()

        # Define the top row
        top_row_layout = QHBoxLayout()
        top_row_layout.setContentsMargins(0, 0, 0, 0)
        top_row_layout.setSpacing(5)
        top_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        clip_icon = Icon(':/icons/clip.svg')
        top_row_layout.addWidget(clip_icon)
        top_row_layout.addWidget(QLabel('Clip'))

        # Define the bottom row
        bottom_row_layout = QHBoxLayout()
        bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        bottom_row_layout.setSpacing(5)
        bottom_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        clock_icon = Icon(':/icons/clock.svg')

        self.duration_label = QLabel()
        bottom_row_layout.addWidget(self.duration_label)
        bottom_row_layout.addWidget(clock_icon)
        bottom_row_layout.addWidget(QLabel('1x'))

        layout.addLayout(top_row_layout)
        layout.addLayout(bottom_row_layout)

        self.setLayout(layout)

        self.setStyleSheet(f'''
        QLabel {{
            color: {self.color};
        }}
        ''')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the main rectangle with rounded corners
        painter.setBrush(self.background_color)
        painter.setPen(Qt.NoPen)
        rect = QRectF(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

        # # Draw the left strip with rounded corners
        path_left = QPainterPath()
        path_left.moveTo(self.strip_width, 0)
        path_left.lineTo(0, 0)
        path_left.arcTo(QRectF(0, 0, 2 * self.border_radius, 2 * self.border_radius), 90, 90)
        path_left.lineTo(0, self.height() - self.border_radius)
        path_left.arcTo(QRectF(0, self.height() - 2 * self.border_radius, 2 * self.border_radius, 2 * self.border_radius), 180, 90)
        path_left.lineTo(self.strip_width, self.height())
        path_left.closeSubpath()
        painter.setBrush(self.strip_color)
        painter.drawPath(path_left)

        # Draw the right strip with rounded corners
        path_right = QPainterPath()
        path_right.moveTo(self.width() - self.strip_width, self.height())
        path_right.lineTo(self.width(), self.height())
        path_right.arcTo(QRectF(self.width() - 2 * self.border_radius, self.height() - 2 * self.border_radius, 2 * self.border_radius, 2 * self.border_radius), 270, 90)
        path_right.lineTo(self.width(), self.border_radius)
        path_right.arcTo(QRectF(self.width() - 2 * self.border_radius, 0, 2 * self.border_radius, 2 * self.border_radius), 0, 90)
        path_right.lineTo(self.width() - self.strip_width, 0)
        path_right.closeSubpath()
        painter.setBrush(self.strip_color)
        painter.drawPath(path_right)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x_pos = event.position().toPoint().x()

        # Update the frame and the slider's position
        AppContext.get('view_model').update_frame_based_on_position(x_pos)
        AppContext.get('view_model').update_slider_position(x_pos)

    def update_clip_width(self, video_len):
        self.duration_label.setText(f'{video_len:.1f}s')

        pixels_per_second = AppContext.get('view_model').get_pixels_per_second()

        new_width = int(video_len * pixels_per_second)
        self.setFixedWidth(new_width)
        self.init_ui()