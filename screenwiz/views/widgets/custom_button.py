from PySide6.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
    QGraphicsDropShadowEffect, QSizePolicy,
)
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPainterPath, QBrush, QPen
from PySide6.QtCore import Qt, QSize


class CustomButton(QPushButton):
    def __init__(
        self,
        icon=None,
        icon_size=(26, 26),
        text='',
        orientation='horizontal',
        parent=None,
        **kwargs
    ):
        super().__init__(text, parent)

        # Ensure at least an icon or text is provided
        if not icon and not text:
            raise ValueError('Either an icon or text must be provided.')

        self.icon_size = icon_size
        self.text = text
        self.orientation = orientation

        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(*icon_size))

        self.setMinimumSize(self.calculate_minimum_size())
        self.apply_styles(kwargs)

    def calculate_minimum_size(self):
        icon_width, icon_height = self.icon_size
        text_width = self.fontMetrics().boundingRect(self.text).width()
        text_height = self.fontMetrics().height()

        if self.orientation == 'horizontal':
            min_width = icon_width + text_width + 10  # 10 for spacing
            min_height = max(icon_height, text_height)
        else:
            min_width = max(icon_width, text_width)
            min_height = icon_height + text_height + 10  # 10 for spacing

        return QSize(min_width, min_height)

    def apply_styles(self, styles):
        background_color = styles.get('background_color', '#4f46e5')
        text_color = styles.get('text_color', '#FFFFFF')
        font_size = styles.get('font_size', 14)
        padding = styles.get('padding', '0 0')
        border = styles.get('border', 'none')
        border_radius = styles.get('border_radius', 5)
        hover_style = styles.get('hover', {'background_color': '#4338ca', 'text_color': '#FFFFFF'})
        hover_background_color = hover_style.get('background_color', '#007BFF')
        hover_text_color = hover_style.get('text_color', '#FFFFFF')
        box_shadow = styles.get('box_shadow', {})

        stylesheet = f'''
        QPushButton {{
            background-color: {background_color};
            color: {text_color};
            border: {border};
            border-radius: {border_radius}px;
            font-size: {font_size}px;
            padding: {padding};
        }}
        QPushButton:hover {{
            background-color: {hover_background_color};
            color: {hover_text_color};
        }}
        QPushButton:
        '''

        self.setStyleSheet(stylesheet)

        if box_shadow:
            offset = box_shadow.get('offset', (5, 5))
            radius = box_shadow.get('radius', 20)
            color = box_shadow.get('color', (180, 180, 180, 160))
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setOffset(*offset)
            shadow.setBlurRadius(radius)
            shadow.setColor(QColor(*color))
            self.setGraphicsEffect(shadow)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def set_icon(self, icon: str):
        self.icon_path = icon if isinstance(icon, str) else None

        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(*self.icon_size))


class RoundedImageButton(QPushButton):
    def __init__(self, path, border_radius=10, size=(24, 24), parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(path)
        self.border_radius = border_radius

        # if isinstance(size, (list, tuple)):
        #     size = QSize(*size)

        # self.setFixedSize(size)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('''
        border: none;
        ''')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        painter.setBrush(QBrush(self.pixmap))
        painter.setPen(Qt.NoPen)

        # Clip path
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.border_radius, self.border_radius)
        painter.setClipPath(path)

        # Rounded pixmap
        painter.drawPixmap(0, 0, self.width(), self.height(), self.pixmap)

        # Borders
        painter.setPen(QPen(Qt.darkGray, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

    def resizeEvent(self, event):
        # Resize the pixmap when the button is resized
        self.pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()  # Trigger a repaint

    def sizeHint(self):
        # Return the preferred size of the button based on the pixmap size
        return self.pixmap.size()