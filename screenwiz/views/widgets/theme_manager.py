from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    theme_changed = Signal(str)

    _instance = None

    @staticmethod
    def get_instance():
        if ThemeManager._instance is None:
            ThemeManager._instance = ThemeManager()
        return ThemeManager._instance

    def __init__(self):
        super().__init__()
        if ThemeManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ThemeManager._instance = self