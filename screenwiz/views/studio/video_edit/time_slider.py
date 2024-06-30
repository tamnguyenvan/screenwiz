from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QPoint, Signal

from utils.context_utils import AppContext
from config import config


class TimeSlider(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.color = '#321eba'
        self.config = config['objects']['time_slider']

        width = self.config['width']
        height = self.config['height']
        self.setFixedSize(width, height)
        self.init_ui()

        AppContext.get('view_model').on_timeslider_position_changed.connect(self.update_position)

        self.dragging = False
        self.offset = QPoint()

    def init_ui(self):
        self.setFixedSize(self.width(), self.height())

        top_label = QLabel(self)
        top_label.setFixedSize(self.width(), self.width())
        top_label.setStyleSheet(f"""
            border-radius: 8px;
            background-color: {self.color};
        """)
        top_label.move(0, 0)

        vertical_bar_width = 2
        vertical_bar = QLabel(self)
        vertical_bar.setFixedSize(vertical_bar_width, self.height())
        vertical_bar.move((self.width() - vertical_bar_width) // 2, 0)
        vertical_bar.setStyleSheet(f'background-color: {self.color};')

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            new_x = self.mapToParent(event.pos()).x() - self.width() / 2
            if new_x < 0:
                new_x = 0
            elif new_x > self.parent().width() - self.width():
                new_x = self.parent().width() - self.width()
            self.move(new_x, self.y())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            x_pos = self.mapToParent(event.pos()).x()

            # Update the time slider position
            AppContext.get('view_model').update_frame_based_on_position(x_pos)

    def update_position(self, x_pos):
        new_x = x_pos - self.width() / 2
        self.move(new_x, self.y())