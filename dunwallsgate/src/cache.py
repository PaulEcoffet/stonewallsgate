import pygame
from screens.text_render import TextRender
from character import Character

class CacheSystem():
    """
    Define a character and its abilities
    """
    def __init__(self, characters):
        self.characters = characters
        self.rendered_dialogues = []
    
    def get_charac(self, ref):
        for charac in self.characters:
            if charac.name == ref:
                return charac
        try:
            self.characters.append(Character(ref))
            return self.characters[-1]
        except ValueError:
            print("ok")
            pass
    def format_dialogues(self, dialogues):
        self.begin = True
        dialogues.restore_messages()
        message = dialogues.next()
        while message is not None:
            txt_object = TextRender((904,163), "larabiefont", 25, 
                (255,158,0), message["msg"])
            txt_sprite = txt_object.next()
            while txt_sprite is not None:
                self.rendered_dialogues.append({
                                                            "img_txt": txt_sprite, 
                                                            "talker": message["talker"], 
                                                            "hearer": message["hearer"],
                                                            "choices": message["choices"]
                                                            })
                txt_sprite = txt_object.next()
            message = dialogues.next()
    
    def next_panel(self):
        if len(self.rendered_dialogues) > 1 or self.begin:
            if not self.begin:
                del self.rendered_dialogues[0]
            else:
                self.begin = False
            return self.rendered_dialogues[0]
        elif len(self.rendered_dialogues) == 1:
            self.rendered_dialogues = []
        return None

    
    def clear_portraits(self):
        self.portraits = {}
    def clear_dialogues(self):
        self.rendered_dialogues = []
    def clear_all(self):
        self.clear_portraits()
        self.clear_dialogues()