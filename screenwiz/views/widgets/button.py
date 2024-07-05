from PySide6.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
    QGraphicsDropShadowEffect, QSizePolicy,
)
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPainterPath, QBrush, QPen
from PySide6.QtCore import Qt, QSize

from config import config


class SWButton(QPushButton):
    def __init__(self, text=None, icon=None, icon_size=None, background_color=None,
                 text_color=None, hover_background_color=None,
                 hover_text_color=None, padding=None, border=None,
                 border_radius=None, box_shadow=None, parent=None):
        super().__init__(text, parent)

        button_configs = config['theme']['button']
        self.text = text
        self.icon = icon
        self.icon_size = icon_size or button_configs['icon_size']
        self.background_color = background_color or button_configs['background_color']
        self.text_color = text_color or button_configs['text_color']
        self.hover_background_color = hover_background_color or button_configs['hover_background_color']
        self.hover_text_color = hover_text_color or button_configs['hover_text_color']
        self.padding = padding or button_configs['padding']
        self.border = border or button_configs['border']
        self.border_radius = border_radius or button_configs['border_radius']
        self.box_shadow = box_shadow or button_configs['box_shadow']

        self.init_ui()

    def init_ui(self):
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if self.icon:
            self.setIcon(QIcon(self.icon))
            self.setIconSize(QSize(*self.icon_size))  # Adjust icon size if needed

        # Set style
        stylesheet = f"""
        QPushButton {{
            background-color: {self.background_color};
            color: {self.text_color};
            border: {self.border};
            border-radius: {self.border_radius}px;
            padding: {self.padding};
        }}
        QPushButton:hover {{
            background-color: {self.hover_background_color};
            color: {self.hover_text_color};
        }}
        """
        self.setStyleSheet(stylesheet)

    def set_icon(self, icon):
        self.icon_path = icon if isinstance(icon, str) else None
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(*self.icon_size))


# class SWButton(QPushButton):
#     def __init__(
#         self,
#         icon=None,
#         icon_size=None,
#         text=None,
#         orientation=None,
#         background_color=None,
#         text_color=None,
#         font_size=None,
#         padding=None,
#         border=None,
#         border_radius=None,
#         hover_background_color=None,
#         hover_text_color=None,
#         box_shadow=None,
#         parent=None,
#         **kwargs
#     ):
#         self.button_configs = config['theme']['button']
#         super().__init__(text or self.button_configs['text'], parent)

#         # Ensure at least an icon or text is provided
#         if not icon and not text:
#             raise ValueError('Either an icon or text must be provided.')

#         self.icon_size = icon_size or self.button_configs['icon_size']
#         self.text = text or self.button_configs['text']
#         self.orientation = orientation or self.button_configs['orientation']
#         self.font_size = font_size or self.button_configs['font_size']
#         self.padding = padding or self.button_configs['padding']
#         self.border = border or self.button_configs['border']
#         self.border_radius = border_radius or self.button_configs['border_radius']

#         if icon:
#             self.setIcon(QIcon(icon))
#             self.setIconSize(QSize(*self.icon_size))

#         self.setMinimumSize(self.calculate_minimum_size())

#         self.stylesheet_template = '''
#         QPushButton {{
#             background-color: {background_color};
#             color: {text_color};
#             border: {border};
#             border-radius: {border_radius}px;
#             font-size: {font_size}px;
#             padding: {padding};
#         }}
#         QPushButton:hover {{
#             background-color: {hover_background_color};
#             color: {hover_text_color};
#         }}
#         '''

#         self.apply_style(
#             background_color=background_color or self.button_configs['background_color'],
#             text_color=text_color or self.button_configs['text_color'],
#             font_size=font_size,
#             padding=padding,
#             border=border,
#             border_radius=border_radius,
#             hover_background_color=hover_background_color or self.button_configs['hover_background_color'],
#             hover_text_color=hover_text_color or self.button_configs['hover_text_color'],
#             box_shadow=box_shadow or self.button_configs['box_shadow'],
#         )

#         ThemeManager.get_instance().theme_changed.connect(self.on_theme_changed)

#     def calculate_minimum_size(self):
#         icon_width, icon_height = self.icon_size
#         text_width = self.fontMetrics().boundingRect(self.text).width()
#         text_height = self.fontMetrics().height()

#         if self.orientation == 'horizontal':
#             min_width = icon_width + text_width + 10  # 10 for spacing
#             min_height = max(icon_height, text_height)
#         else:
#             min_width = max(icon_width, text_width)
#             min_height = icon_height + text_height + 10  # 10 for spacing

#         return QSize(min_width, min_height)

#     def apply_style(
#         self,
#         background_color,
#         text_color,
#         font_size,
#         padding,
#         border,
#         border_radius,
#         hover_background_color,
#         hover_text_color,
#         box_shadow,
#     ):
#         stylesheet = self.stylesheet_template.format(
#             background_color=background_color,
#             text_color=text_color,
#             font_size=font_size,
#             padding=padding,
#             border=border,
#             border_radius=border_radius if border_radius is not None else 0,
#             hover_background_color=hover_background_color,
#             hover_text_color=hover_text_color,
#         )
#         self.setStyleSheet(stylesheet)

#         if box_shadow:
#             offset = box_shadow.get('offset', (5, 5))
#             radius = box_shadow.get('radius', 20)
#             color = box_shadow.get('color', (180, 180, 180, 160))
#             shadow = QGraphicsDropShadowEffect(self)
#             shadow.setOffset(*offset)
#             shadow.setBlurRadius(radius)
#             shadow.setColor(QColor(*color))
#             self.setGraphicsEffect(shadow)

#         self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

#     def set_icon(self, icon: str):
#         self.icon_path = icon if isinstance(icon, str) else None
#         self.setIcon(QIcon(icon))
#         self.setIconSize(QSize(*self.icon_size))

#     def on_theme_changed(self, theme='light'):
#         self.button_configs = config['theme']['button']
#         self.apply_style(
#             background_color=self.button_configs['background_color'],
#             text_color=self.button_configs['text_color'],
#             font_size=self.font_size or self.button_configs['font_size'],
#             padding=self.padding or self.button_configs['padding'],
#             border=self.border or self.button_configs['border'],
#             border_radius=self.border_radius or self.button_configs['border_radius'],
#             hover_background_color=self.button_configs['hover_background_color'],
#             hover_text_color=self.button_configs['hover_text_color'],
#             box_shadow=self.button_configs['box_shadow']
#         )


class RoundedImageButton(QPushButton):
    def __init__(self, path, border_radius=8, size=(24, 24), parent=None):
        super().__init__(parent)

        self.path = path
        self.border_radius = border_radius
        self.pixmap = QPixmap(path)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('''
        border: none;
        ''')

    def paintEvent(self, event):
        self.border_radius = self.border_radius

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
        # painter.setPen(QPen(Qt.lightGray, 4))
        # painter.setBrush(Qt.NoBrush)
        # painter.drawPath(path)

    def resizeEvent(self, event):
        # Resize the pixmap when the button is resized
        self.pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()  # Trigger a repaint

    def sizeHint(self):
        # Return the preferred size of the button based on the pixmap size
        return self.pixmap.size()