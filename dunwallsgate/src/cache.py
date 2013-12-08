import pygame
import glob
import os.path

from screens.text_render import TextRender
from character import Character
import data

class CacheSystem():
    """
    Define a character and its abilities
    """
    def __init__(self):
        self.image_portraits = {}
        self.image_backgrounds = {}
        self.rendered_dialogues = []
        self.load_image_portraits()
        self.load_backgrounds()
        
    def get_portrait_image(self, ref, position):
        try:
            return self.image_portraits[ref][position]
        except KeyError:
            return self.image_portraits[ref]["front"]

    def load_backgrounds(self):
        self.image_backgrounds["default"] = pygame.Surface((1024, 574)) #Default BG
        for image_path in glob.glob(os.path.join(
                data.get_image_path("scenes"), "*.png")):
            scene_ref = os.path.splitext(os.path.basename(image_path))[0]
            image = pygame.image.load(image_path).convert()
            image = pygame.transform.scale(
                image, (1024, 574))
            transparent = pygame.Surface((205, 25), pygame.SRCALPHA)
            transparent.fill((0, 0, 0, 140))
            note = TextRender((320, 50), "joystix", 16, (255, 50, 10),
                              "ALPHA version 2")
            transparent.blit(note.next(), (5, 3))
            image.blit(transparent, (10, 10))
            self.image_backgrounds[scene_ref] = image
            
    def load_image_portraits(self):
        for image_path in glob.glob(os.path.join(
                data.get_image_path("characters"), "*.png")):
            filename = os.path.splitext(os.path.basename(image_path))[0]
            charact_ref, position = filename.split("_")
            image = pygame.image.load(image_path).convert_alpha()
            if not charact_ref in self.image_portraits:
                self.image_portraits[charact_ref] = {}
            self.image_portraits[charact_ref][position] = image
    
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
            self.clear_dialogues()
        return None


    def clear_dialogues(self):
        self.rendered_dialogues = []

    def clear_all(self):
        self.clear_dialogues()
