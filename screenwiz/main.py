import sys
from PySide6.QtWidgets import QApplication
from views.studio import StudioWindow
from viewmodels.studio_viewmodel import StudioViewModel
from models.studio_model import StudioModel

from utils.context_utils import AppContext
from resources import resources_rc


def main():
    app = QApplication(sys.argv)
    model = StudioModel()
    view_model = StudioViewModel(model=model)
    AppContext.set('view_model', view_model)

    view = StudioWindow()

    view.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
