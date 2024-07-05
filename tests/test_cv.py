from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel)
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, Qt

class CustomColorPicker(QWidget):
    colorChanged = Signal(QColor)  # Signal to emit when the color changes

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_color = QColor(255, 255, 255)  # Default color is white

        self.color_label = QLabel(self)
        self.color_label.setAlignment(Qt.AlignCenter)
        self.color_label.setAutoFillBackground(True)
        self.update_color_label()

        self.pick_color_button = QPushButton("Pick Color", self)
        self.pick_color_button.clicked.connect(self.open_color_dialog)

        layout = QVBoxLayout(self)
        layout.addWidget(self.color_label)
        layout.addWidget(self.pick_color_button)
        self.setLayout(layout)

    def open_color_dialog(self):
        color = QColorDialog.getColor(self.selected_color, self, "Select Color")
        if color.isValid():
            self.selected_color = color
            self.update_color_label()
            self.colorChanged.emit(color)

    def update_color_label(self):
        palette = self.color_label.palette()
        palette.setColor(self.color_label.backgroundRole(), self.selected_color)
        self.color_label.setPalette(palette)

    def get_selected_color(self):
        return self.selected_color

if __name__ == "__main__":
    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout(window)

    color_picker = CustomColorPicker()
    color_label = QLabel("Selected Color: #FFFFFF")
    color_label.setAlignment(Qt.AlignCenter)

    def on_color_changed(color):
        color_label.setText(f"Selected Color: {color.name()}")

    color_picker.colorChanged.connect(on_color_changed)

    layout.addWidget(color_picker)
    layout.addWidget(color_label)
    window.setLayout(layout)
    window.setWindowTitle("Custom Color Picker")
    window.resize(300, 200)
    window.show()

    app.exec()
