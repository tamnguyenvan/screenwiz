import os
from pathlib import Path
import json


config_paths = {
    'debug': 'config_debug.json',
    'prod': 'config_prod.json',
}


def load_config():
    app_env = os.getenv('APP_ENV', 'debug')
    if app_env not in config_paths:
        app_env = 'debug'

    file_name = config_paths[app_env]
    file_path = Path(__file__).parent / file_name
    with open(file_path, 'r') as file:
        return json.load(file)


def load_theme(theme_file):
    with open(theme_file) as file:
        return json.load(file)


config = load_config()
default_theme = config['default_theme']
theme_file = config['themes'][default_theme]
config['theme'] = load_theme(theme_file)