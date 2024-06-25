from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent, Signal, QPoint
from PySide6.QtGui import QMouseEvent
from views.widgets.color_widget import ColorWidget


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
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        x_pos = self.mapToParent(event.position()).toPoint()
        self.on_mouse_moved.emit(x_pos)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x_pos = self.mapToParent(event.position()).toPoint()
        self.on_clicked.emit(x_pos)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.on_released.emit()

    def leaveEvent(self, event: QEvent) -> None:
        self.on_left.emit()