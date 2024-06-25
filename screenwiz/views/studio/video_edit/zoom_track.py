from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtGui import QMouseEvent, QCursor, QPainterPath, QPainter, QColor, QAction, QIcon
from PySide6.QtCore import Qt, QPoint, QRectF, Signal

from views.widgets.icon import Icon
from views.widgets.custom_context_menu import CustomContextMenu
from utils.context_utils import AppContext


class ZoomTrack(QWidget):
    on_deleted = Signal(int)
    on_deleted_all = Signal(bool)

    def __init__(self, index, size, drag_range, parent=None):
        super().__init__(parent=parent)

        self.index = index
        self.drag_range = drag_range

        self.border_radius = 10
        self.color = QColor('#3B25D1')
        self.strip_color = QColor('#5A46E2')
        self.strip_width = 12
        self.setMouseTracking(True)
        self.setFixedSize(size)

        self.init_ui()

        self.default_cursor = QCursor(Qt.ArrowCursor)
        self.strip_cursor = QCursor(Qt.SizeHorCursor)

        self.dragging = False
        self.dragging_offset = QPoint()
        self.resizing = False
        self.resizing_offset = QPoint()

    def init_ui(self):
        layout = QVBoxLayout()

        # Define the top row
        top_row_layout = QHBoxLayout()
        top_row_layout.setContentsMargins(0, 0, 0, 0)
        top_row_layout.setSpacing(5)
        top_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cursor_icon = Icon(':/icons/cursor.svg')
        top_row_layout.addWidget(cursor_icon)
        top_row_layout.addWidget(QLabel('Zoom'))

        # Define the bottom row
        bottom_row_layout = QHBoxLayout()
        bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        bottom_row_layout.setSpacing(5)
        bottom_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        zoom_icon = Icon(':/icons/zoom.svg')
        mouse_icon = Icon(':/icons/mouse.svg')

        bottom_row_layout.addWidget(zoom_icon)
        bottom_row_layout.addWidget(QLabel('2x'))
        bottom_row_layout.addWidget(mouse_icon)
        bottom_row_layout.addWidget(QLabel('Auto'))

        layout.addLayout(top_row_layout)
        layout.addLayout(bottom_row_layout)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the main rectangle with rounded corners
        painter.setBrush(self.color)
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

    def contextMenuEvent(self, event):
        # context_menu = QMenu(self)
        # context_menu.setStyleSheet("""
        #     QMenu {
        #         background-color: #2d2d30;
        #         border: 1px solid #3a3a3e;
        #         padding: 5px;
        #         border-radius: 8px;
        #     }
        #     QMenu::item {
        #         background-color: transparent;
        #         padding: 8px 20px;
        #         color: #ffffff;
        #         font-size: 14px;
        #         border-radius: 4px;
        #     }
        #     QMenu::item:selected {
        #         background-color: #4d5057;
        #     }
        #     QMenu::icon {
        #         padding-right: 10px;
        #     }
        # """)
        # delete_action = QAction(QIcon(':/icons/trash.svg'), "Delete", self)
        # delete_all_action = QAction(QIcon(':/icons/trash.svg'), "Delete all", self)

        # delete_action.triggered.connect(self.delete_track)
        # delete_all_action.triggered.connect(self.delete_all_tracks)

        # context_menu.addAction(delete_action)
        # context_menu.addAction(delete_all_action)
        # context_menu.exec(event.globalPos())
        context_menu = CustomContextMenu(self)
        delete_action = QAction(QIcon(':/icons/trash.svg'), "Delete", self)
        delete_all_action = QAction(QIcon(':/icons/trash.svg'), "Delete all", self)

        delete_action.triggered.connect(self.delete_track)
        delete_all_action.triggered.connect(self.delete_all_tracks)

        context_menu.addAction(delete_action)
        context_menu.addAction(delete_all_action)
        context_menu.exec(event.globalPos())

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if event.position().x() < self.strip_width:
                self.resizing = True
                self.resize_direction = 'left'
                self.resizing_offset = event.globalPosition().toPoint()

            elif event.position().x() > self.width() - self.strip_width:
                self.resizing = True
                self.resize_direction = 'right'
                self.resizing_offset = event.globalPosition().toPoint()
            else:
                self.dragging = True
                # self.dragging_offset = event.globalPosition().toPoint() - self.mapToGlobal(QPoint(0, 0))
                self.dragging_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QMouseEvent):
        target_rect = QRectF(self.strip_width, 0, self.width() - 2 * self.strip_width, self.height())
        if target_rect.contains(event.position()):
            self.setCursor(self.default_cursor)
        else:
            self.setCursor(self.strip_cursor)

        if self.dragging:
            new_x = (event.globalPosition().toPoint() - self.dragging_offset).x()
            updated_data = [self.index, new_x, self.width()]

            AppContext.get('view_model').update_zoom_tracks(updated_data)
        elif self.resizing:
            self.resize_rectangle(event.globalPosition().toPoint())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.resizing = False

    def resize_rectangle(self, global_pos):
        if self.resize_direction == 'left':
            diff = global_pos.x() - self.resizing_offset.x()
            new_x = self.x() + diff
            new_width = self.width() - diff

            if new_width >= 50:
                self.resizing_offset = global_pos

                updated_data = [self.index, new_x, new_width]
                AppContext.get('view_model').update_zoom_tracks(updated_data)

        elif self.resize_direction == 'right':
            diff = global_pos.x() - self.resizing_offset.x()
            new_width = self.width() + diff
            if new_width >= 50:
                # self.setFixedSize(new_width, self.height())
                self.resizing_offset = global_pos

                updated_data = [self.index, self.x(), new_width]
                AppContext.get('view_model').update_zoom_tracks(updated_data)

    def delete_track(self):
        AppContext.get('view_model').delete_track(self.index)

    def delete_all_tracks(self):
        AppContext.get('view_model').delete_all_tracks()