from PySide6.QtWidgets import (
    QVBoxLayout, QStackedLayout,
    QPushButton, QHBoxLayout, QFrame
)
from PySide6.QtCore import Signal


class CustomTabView(QFrame):
    def __init__(self, pages=[], parent=None):
        super().__init__(parent)

        self.pages = pages

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(10)

        # Tabbar
        self.tabbar = TabBar(self)
        self.tabbar.on_switched.connect(self.switch_tab)
        layout.addWidget(self.tabbar)

        # Create the stacked layout to hold pages
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_layout.setSpacing(0)
        layout.addLayout(self.stacked_layout)

        # Add pages to the stacked layout
        for page in self.pages:
            self.stacked_layout.addWidget(page)

        self.setLayout(layout)

    def switch_tab(self, index):
        self.stacked_layout.setCurrentIndex(index)

        for i, button in enumerate(self.tabbar.buttons):
            if i == index:
                self.tabbar.buttons[i].set_active()
            else:
                self.tabbar.buttons[i].update_stylesheet()


class TabBar(QFrame):
    on_switched = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()
        self.setObjectName('tabbar')
        self.setStyleSheet('''
            #tabbar {
                border: 1px solid #4d5057;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
        ''')

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.wallpaper_button = CustomTabButton('Wallpaper')
        self.wallpaper_button.clicked.connect(lambda: self.on_switched.emit(0))
        self.wallpaper_button.set_active()

        self.gradient_button = CustomTabButton('Gradient')
        self.gradient_button.clicked.connect(lambda: self.on_switched.emit(1))

        self.color_button = CustomTabButton('Color')
        self.color_button.clicked.connect(lambda: self.on_switched.emit(2))

        self.image_button = CustomTabButton('Image')
        self.image_button.clicked.connect(lambda: self.on_switched.emit(3))

        self.buttons = [
            self.wallpaper_button,
            self.gradient_button,
            self.color_button,
            self.image_button,
        ]

        layout.addWidget(self.wallpaper_button)
        # layout.addWidget(self.create_divider())
        layout.addWidget(self.gradient_button)
        # layout.addWidget(self.create_divider())
        layout.addWidget(self.color_button)
        # layout.addWidget(self.create_divider())
        layout.addWidget(self.image_button)


        self.setLayout(layout)

    def create_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setObjectName('line')
        return divider


class CustomTabButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

        self.update_stylesheet()

    def update_stylesheet(self, color='darkgray', border_bottom='none'):
        self.setStyleSheet(f'''
            CustomTabButton {{
                background-color: transparent;
                padding: 10px;
                min-width: auto;
                color: {color};
                border: none;
                border-bottom: {border_bottom};
            }}
        ''')

    def set_active(self):
        # Change the style
        self.update_stylesheet(color='#5A46E2', border_bottom='2px solid #5A46E2')
