from functools import partial

from PySide6.QtWidgets import (
    QVBoxLayout, QStackedLayout,
    QWidget, QPushButton, QHBoxLayout, QFrame
)
from PySide6.QtCore import Signal


class SWTabView(QFrame):
    def __init__(self, button_texts=[], pages=[], parent=None):
        super().__init__(parent)

        assert len(button_texts) == len(pages)

        self.pages = pages

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(10)

        # Tabbar
        self.tabbar = TabBar(button_texts=button_texts, parent=self)
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


class TabBar(QWidget):
    on_switched = Signal(int)

    def __init__(self, button_texts, parent=None):
        super().__init__(parent=parent)

        self.button_texts = button_texts

        self.init_ui()
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

        self.buttons = []
        for index, text in enumerate(self.button_texts):
            button = CustomTabButton(text)
            # button.clicked.connect(lambda index=index: self.on_switched.emit(index))
            button.clicked.connect(partial(self.on_switched.emit, index))

            if index == 0:
                button.set_active()

            self.buttons.append(button)

            layout.addWidget(button)

        self.setLayout(layout)


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
