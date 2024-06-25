from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QPainterPath, QRegion, QTransform
from PySide6.QtCore import QRectF


class CustomContextMenu(QMenu):
    def __init__(self, *args, **kwargs):
        super(CustomContextMenu, self).__init__()
        self.radius = 10

        self.setStyleSheet(f'''
            QMenu {{
                background-color: #3e3e3e;
                border: 1px solid #3a3a3e;
                padding: 5px;
                border-radius: {self.radius}px;
            }}
            QMenu::item {{
                background-color: transparent;
                padding: 8px 20px;
                color: #ffffff;
                font-size: 14px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: #4d5057;
            }}
            QMenu::icon {{
                padding-right: 10px;
            }}
        ''')

    def resizeEvent(self, event):
        path = QPainterPath()
        # the rectangle must be translated and adjusted by 1 pixel in order to
        # correctly map the rounded shape
        rect = QRectF(self.rect()).adjusted(.5, .5, -1.5, -1.5)
        path.addRoundedRect(rect, self.radius, self.radius)
        # QRegion is bitmap based, so the returned QPolygonF (which uses float
        # values must be transformed to an integer based QPolygon
        region = QRegion(path.toFillPolygon(QTransform()).toPolygon())
        self.setMask(region)