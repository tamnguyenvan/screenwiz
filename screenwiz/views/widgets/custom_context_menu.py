from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QPainterPath, QRegion, QTransform
from PySide6.QtCore import QRectF


class CustomContextMenu(QMenu):
    def __init__(
        self,
        menu_color='#3e3e3e',
        menu_border='1px solid #3e3e3e',
        menu_border_radius=10,
        menu_padding=8,
        item_padding='16px 20px',
        item_color='white',
        item_font_size=14,
        item_border_radius=4,
        item_selected_color='#4d5057',
        icon_padding_right=10,
        parent=None
    ):
        super().__init__(parent=parent)

        self.menu_border_radius = menu_border_radius

        style = f'''
            QMenu {{
                background-color: {menu_color};
                border: {menu_border};
                padding: {menu_padding}px;
                border-radius: {menu_border_radius}px;
            }}
            QMenu::item {{
                background-color: transparent;
                padding: {item_padding};
                color: {item_color};
                font-size: {item_font_size}px;
                border-radius: {item_border_radius}px;
            }}
            QMenu::item:selected {{
                background-color: {item_selected_color};
            }}
            QMenu::icon {{
                padding-right: {icon_padding_right}px;
            }}
        '''
        self.setStyleSheet(style)

    def resizeEvent(self, event):
        path = QPainterPath()
        rect = QRectF(self.rect()).adjusted(.5, .5, -1.5, -1.5)
        path.addRoundedRect(rect, self.menu_border_radius, self.menu_border_radius)
        region = QRegion(path.toFillPolygon(QTransform()).toPolygon())
        self.setMask(region)