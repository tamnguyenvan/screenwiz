from PySide6.QtWidgets import (
    QGridLayout, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy
)
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import QSize

from views.widgets.tabview import SWTabView
from views.widgets.button import SWButton, RoundedImageButton
from utils.context_utils import AppContext


class BackgroundSetting(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)

        # Label
        icon_label = QLabel()
        icon_path = ':/icons/background.svg'
        pixmap = QPixmap(icon_path)
        icon_label.setPixmap(pixmap)
        title_layout.addWidget(icon_label)

        label = QLabel('Background')
        title_layout.addWidget(label)

        title_layout.addStretch(1)

        # custom tabview
        button_texts = ['Wallpaper', 'Gradient', 'Color', 'Image']
        pages = [
            WallpaperPage(),
            GradientPage(),
            ColorPage(),
            ImagePage(),
        ]
        tabview = SWTabView(
            button_texts=button_texts,
            pages=pages)

        main_layout.addLayout(title_layout)
        main_layout.addWidget(tabview)

        self.setLayout(main_layout)
        self.update_stylesheet()

    def update_stylesheet(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 12pt;
            }
        """)


class WallpaperPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

    def init_ui(self):
        # layout
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setHorizontalSpacing(8)
        main_layout.setVerticalSpacing(5)

        items_per_row = 7
        for i in range(20):
            row = i // items_per_row
            col = i % items_per_row
            main_layout.addWidget(WallpaperThumbnailButton(index=i+1), row, col)

        self.setLayout(main_layout)


class WallpaperThumbnailButton(RoundedImageButton):
    def __init__(self, index, size=None, parent=None):
        self.path = f'/home/tamnv/Projects/exp/screenwiz/screenwiz/resources/images/wallpaper/thumbnail/gradient-wallpaper-{index:04d}.png'
        super().__init__(path=self.path, size=size, parent=parent)

        self.index = index
        self.clicked.connect(self.update_wallpaper)

    def update_wallpaper(self):
        updated_data = {'type': 'wallpaper', 'value': self.index}
        AppContext.get('view_model').update_wallpaper(updated_data)


class GradientPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

    def init_ui(self):
        pass


class ColorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.colors = [
            '#FF3131', '#FF5757', '#FF66C4', '#CB6CE6', '#8C52FF', '#5E17EB', '#0097B2',
            '#0CC0DF', '#5CE1E6', '#38B6FF', '#5271FF', '#004AAD', '#00BF63', '#7ED957',
            '#C1FF72', '#FFDE59', '#FFBD59', '#FF914D', '#FA7420', '#5E17EB',
        ]
        self.num_columns = 7

        self.init_ui()

    def init_ui(self):
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(8)
        grid_layout.setVerticalSpacing(5)
        self.setLayout(grid_layout)

        for i, color in enumerate(self.colors):
            color_button = ColorButton(i, color)
            row = i // self.num_columns
            col = i % self.num_columns
            grid_layout.addWidget(color_button, row, col)


class ColorButton(QPushButton):
    def __init__(self, index, color, size=(30, 30), parent=None):
        super().__init__(parent=parent)

        self.index = index
        self.color = color

        if isinstance(size, (list, tuple)):
            size = QSize(*size)

        # self.setFixedSize(size)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.init_ui()

        self.clicked.connect(self.update_wallpaper)

    def init_ui(self):
        self.setStyleSheet(f'''
        background-color: {self.color};
        border-radius: 8px;
        ''')

    def update_wallpaper(self):
        updated_data = {'type': 'color', 'value': self.color}
        AppContext.get('view_model').update_wallpaper(updated_data)


class ImagePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.button = SWButton(
            text='Upload',
            icon=':/icons/add.svg',
            icon_size=(30, 30),
            border='2px dotted #cccccc',
            background_color='transparent',
            hover_background_color='transparent',
            border_radius=4
        )
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        layout.addWidget(self.button)

        self.setLayout(layout)