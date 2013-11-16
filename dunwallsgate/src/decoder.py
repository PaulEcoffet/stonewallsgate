import json
import data

_characters_list = None


def get_character_data(ref):
    global _characters_list
    if not _characters_list:
        with open(
                data.get_config_path("characters.json"), "r", encoding="utf8")\
                as f:
            _characters_list = json.load(f)
    for character in _characters_list:
        if character["ref"] == ref:
            return character
