
__all__ = ['apply_theme']


def apply_theme(app, theme='dark'):
    if theme == 'dark':
        qss_file_path = 'resources/styles/dark_theme.qss'
    elif theme == 'light':
        qss_file_path = 'resources/styles/light_theme.qss'
    else:
        qss_file_path = ''

    _apply_stylesheet(app, qss_file_path)


def _apply_stylesheet(app, qss_file_path):
    with open(qss_file_path, "r") as file:
        app.setStyleSheet(file.read())