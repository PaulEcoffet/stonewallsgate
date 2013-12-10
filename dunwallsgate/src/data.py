"""
Ce module permet d'obtenir le chemin absolu des différents fichiers de données.
Ainsi, le fichier peut être exécuter depuis n'importe quel "working directory"
sans qu'il y ait de problème de chemin.
"""
import os.path
import sys


def _module_path():
    """Obtient le chemin absolu du module actuel, même si le fichier est
    "frozen", c'est-à-dire mis dans un exécutable."""
    if hasattr(sys, "frozen"):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


def get_data_path():
    """Donne le chemin du dossier data comlet"
    return os.path.abspath(
        os.path.join(_module_path(), '../data/'))


def get_image_path(path=""):
    """Donne le chemin absolu du data/images"""
    return os.path.abspath(
        os.path.join(get_data_path(), "images/", path))


def get_sound_path(path=""):
    """Donne le chemin absolu des sons"""
    return os.path.abspath(
        os.path.join(get_data_path(), "sounds/", path))


def get_config_path(path=""):
    """Donne le chemin absolu des config"""
    return os.path.abspath(
        os.path.join(get_data_path(), "config/", path))

def get_fonts_path(path=""):
    """Donne le chemin absolu des polices"""
    return os.path.abspath(
        os.path.join(get_data_path(), "fonts/", path))

if __name__ == "__main__":
    print(get_image_path())
    print(get_sound_path())
    print(get_config_path())
    print(get_fonts_path())
