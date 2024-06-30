from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent, Signal, QPoint, QSize
from PySide6.QtGui import QMouseEvent
from views.widgets.color_widget import ColorWidget

from utils.context_utils import AppContext
from config import config


class MouseArea(ColorWidget):
    on_mouse_moved = Signal(QPoint)
    on_left = Signal()
    on_clicked = Signal(QPoint)
    on_released = Signal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.on_mouse_moved.emit(event.position().toPoint())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.on_clicked.emit(event.position().toPoint())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.on_released.emit()

    def leaveEvent(self, event: QEvent) -> None:
        self.on_left.emit()


class ZoomTrackMouseArea(MouseArea):
    def __init__(self, size=QSize(), visible=True, parent=None):
        super().__init__(parent=parent)

        self.config = config['objects']['zoom_track_mouse_area']
        self.hover_zoom_track_duration = config['objects']['hover_zoom_track']['duration']

        pixels_per_seconds = AppContext.get('view_model').get_pixels_per_second()
        self.minimum_width = int(self.hover_zoom_track_duration * pixels_per_seconds)

        if isinstance(size, (list, tuple)):
            size = QSize(*size)

        self.setFixedSize(size)
        self.setVisible(visible)
        self.enabled = self.width() > self.minimum_width

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.enabled:
            x_pos = event.position().toPoint()
            remain_x = self.width() - x_pos.x()
            if remain_x < self.minimum_width:
                x_pos = QPoint(self.width() - self.minimum_width, event.y())

            x_pos = self.mapToParent(x_pos)
            self.on_mouse_moved.emit(x_pos)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.enabled:
            x_pos = event.position().toPoint()
            remain_x = self.width() - x_pos.x()
            print('remain', remain_x)
            if remain_x < self.minimum_width:
                x_pos = QPoint(self.width() - self.minimum_width, event.y())

            x_pos = self.mapToParent(x_pos)
            self.on_clicked.emit(x_pos)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.enabled:
            self.on_released.emit()

    def leaveEvent(self, event: QEvent) -> None:
        if self.enabled:
            self.on_left.emit()