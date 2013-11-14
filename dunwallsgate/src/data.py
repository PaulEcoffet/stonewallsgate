import os.path
import sys


def _module_path():
    if hasattr(sys, "frozen"):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


def get_data_path():
    return os.path.abspath(
        os.path.join(_module_path(), '../data/'))


def get_image_path(path=""):
    return os.path.abspath(
        os.path.join(get_data_path(), "images/", path))


def get_sound_path(path=""):
    return os.path.abspath(
        os.path.join(get_data_path(), "sounds/", path))


def get_config_path(path=""):
    return os.path.abspath(
        os.path.join(get_data_path(), "config/", path))

if __name__ == "__main__":
    print(get_image_path())
    print(get_sound_path())
    print(get_config_path())
