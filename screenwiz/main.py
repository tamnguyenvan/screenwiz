import sys
from PySide6.QtWidgets import QApplication

from views.studio import StudioWindow
from viewmodels.studio_viewmodel import StudioViewModel
from models.studio_model import StudioModel
from utils.style_utils import apply_theme
from resources import resources_rc


def main():
    app = QApplication(sys.argv)
    model = StudioModel()
    view_model = StudioViewModel(model=model)

    view = StudioWindow(view_model=view_model)
    apply_theme(view, 'dark')

    view.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
