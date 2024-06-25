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
        super().__init__(parent)

        # Ensure at least an icon or text is provided
        if not icon and not text:
            raise ValueError('Either an icon or text must be provided.')

        self.icon_path = icon if isinstance(icon, str) else None
        self.icon_size = icon_size
        self.text = text
        self.orientation = orientation

        self.init_ui(icon, text)

        # Apply custom styles
        self.apply_styles(kwargs)

    def init_ui(self, icon, text):
        if self.orientation == 'horizontal':
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()

        self.spacing = 5
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.spacing)

        self.icon_label = None
        self.text_label = None

        if icon:
            # TODO:
            self.icon_label = QLabel()
            if isinstance(icon, str):
                pixmap = QPixmap(icon)
                self.icon_label.setPixmap(pixmap.scaled(self.icon_size[0], self.icon_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.icon_label.setPixmap(icon.pixmap(self.icon_size[0], self.icon_size[1]))
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.icon_label)

        if text:
            self.text_label = QLabel(text)
            layout.addWidget(self.text_label)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def apply_styles(self, styles):
        background_color = styles.get('background_color', '#4f46e5')
        text_color = styles.get('text_color', '#FFFFFF')
        padding = styles.get('padding', '0')
        font_size = styles.get('font_size', 14)
        font_weight = styles.get('font_weight', 400)
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
        QLabel {{
            color: {text_color};
            font-size: {font_size}px;
            font-weight: {font_weight};
        }}
        '''

        self.setStyleSheet(stylesheet)

        # shadow
        # Create drop shadow effect
        if box_shadow:
            offset = box_shadow.get('offset', (5, 5))
            radius = box_shadow.get('radius', 20)
            color = box_shadow.get('color', (180, 180, 180, 160))
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setOffset(*offset)
            shadow.setBlurRadius(radius)
            shadow.setColor(QColor(*color))

            # Apply drop shadow effect to the button
            self.setGraphicsEffect(shadow)

        # Set size policy to MinimumExpanding to allow the button to grow as needed
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        icon_size = 26
        if self.icon_label:
            self.icon_label.setPixmap(QIcon(self.icon_path).pixmap(icon_size, icon_size))

        if self.icon_label:
            icon_size_hint = self.icon_label.sizeHint()
            icon_label_size = (icon_size_hint.width(), icon_size_hint.height())
        else:
            icon_label_size = (0, 0)

        if self.text_label:
            text_size_hint = self.text_label.sizeHint()
            text_label_size = (text_size_hint.width(), text_size_hint.height())
        else:
            text_label_size = (0, 0)

        if self.orientation == 'horizontal':
            self.setMinimumSize(
                icon_label_size[0] + text_label_size[0] + self.spacing,
                max(icon_label_size[1], text_label_size[1])
            )
        else:
            self.setMinimumSize(
                max(icon_label_size[0], text_label_size[0]),
                icon_label_size[1] + text_label_size[1] + self.spacing
            )

    def set_icon(self, icon: str):
        self.icon_path = icon if isinstance(icon, str) else None
        if self.icon_label:
            if isinstance(icon, str):
                pixmap = QPixmap(icon)
                self.icon_label.setPixmap(pixmap.scaled(self.icon_size[0], self.icon_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.icon_label.setPixmap(icon.pixmap(self.icon_size[0], self.icon_size[1]))


class RoundedImageButton(QPushButton):
    def __init__(self, path, border_radius=10, size=(24, 24), parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(path)
        self.border_radius = border_radius

        if isinstance(size, (list, tuple)):
            size = QSize(*size)

        self.setFixedSize(size)

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
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)