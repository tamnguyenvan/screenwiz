from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap, Qt

from utils.context_utils import AppContext
from views.widgets.custom_slider import CustomSlider


class ShapeSetting(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Label
        label = QLabel('Shape')
        label.setStyleSheet('color: #888;')

        main_layout.addWidget(label)

        main_layout.addWidget(PaddingSetting())

        main_layout.addWidget(InsetSetting())
        main_layout.addWidget(RoundnessSetting())

        self.setLayout(main_layout)
        self.update_stylesheet()

    def update_stylesheet(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 12pt;
            }
        """)


class BaseShapeSetting(QWidget):
    def __init__(self, label_text, icon_path, slider_max, slider_min, slider_value):
        super().__init__()

        self.label_text = label_text
        self.icon_path = icon_path
        self.slider_max = slider_max
        self.slider_min = slider_min
        self.slider_value = slider_value

        self.init_ui()

    def init_ui(self):
        # main layout
        main_layout = QVBoxLayout()

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)

        # Label
        icon_label = QLabel()
        pixmap = QPixmap(self.icon_path)
        icon_label.setPixmap(pixmap)
        title_layout.addWidget(icon_label)

        label = QLabel(self.label_text)
        title_layout.addWidget(label)
        title_layout.addStretch(1)

        main_layout.addLayout(title_layout)

        # Slider layout
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(5)

        self.slider = CustomSlider()
        self.slider.setMaximum(self.slider_max)
        self.slider.setMinimum(self.slider_min)
        self.slider.setValue(self.slider_value)
        slider_layout.addWidget(self.slider)

        # Value Label
        self.value_label = QLabel(str(self.slider_value))
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setFixedWidth(30)
        self.value_label.setStyleSheet('color: darkgray;')
        slider_layout.addWidget(self.value_label)

        # # Reset Button
        # self.reset_button = IconButton(
        #     icon_path=ImageAssets.file('images/ui_controls/reset.svg'),
        #     icon_size=(24, 24)
        # )
        # slider_layout.addWidget(self.reset_button)

        main_layout.addLayout(slider_layout)
        self.setLayout(main_layout)

    def on_value_changed(self, value):
        self.value_label.setText(str(value))

    def reset_slider_value(self):
        self.slider.setValue(self.slider_value)


class PaddingSetting(BaseShapeSetting):
    def __init__(self):
        super().__init__('Padding', ':/icons/padding.svg', 500, 0, 50)
        view_model = AppContext.get('view_model')
        view_model.on_padding_changed.connect(self.on_value_changed)

        self.slider.valueChanged.connect(view_model.update_padding)


class InsetSetting(BaseShapeSetting):
    def __init__(self):
        super().__init__('Inset', ':/icons/padding.svg', 200, 0, 0)
        view_model = AppContext.get('view_model')
        view_model.on_inset_changed.connect(self.on_value_changed)

        self.slider.valueChanged.connect(view_model.update_inset)


class RoundnessSetting(BaseShapeSetting):
    def __init__(self):
        super().__init__('Roundness', ':/icons/border.svg', 100, 0, 10)
        view_model = AppContext.get('view_model')
        view_model.on_border_radius_changed.connect(self.on_value_changed)

        self.slider.valueChanged.connect(view_model.update_border_radius)