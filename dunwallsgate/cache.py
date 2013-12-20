import pygame
import glob
import os.path

import data

_portrait_images = {}
_background_images = {}


def load_all():
    load_portrait_images()
    load_backgrounds()


def clear_all():
    global _portrait_images
    global _background_images
    _portrait_images = {}
    _background_images = {}


def get_portrait_image(ref, position):
    """
    Retourne l'image du portrait correspondant à un character
    ref - La reference du character
    position - "front", "back"
    """
    if not _portrait_images:
        load_portrait_images()
    if ref in _portrait_images:
        if position in _portrait_images[ref]:
            return _portrait_images[ref][position]
        elif "front" in _portrait_images[ref]:  # pragma: no cover
            return _portrait_images[ref]["front"]
    raise ValueError("Character Image (%s) not found !"
                     "(Check your images)" % ref)


def load_backgrounds():
    """
    Charge l'ensemble des backgrounds du jeu
    """
    _background_images["default"] = pygame.Surface((1024, 574))
    for image_path in glob.glob(os.path.join(
            data.get_image_path("scenes"), "*.png")):
        scene_ref = os.path.splitext(os.path.basename(image_path))[0]
        image = pygame.image.load(image_path).convert()
        image = pygame.transform.scale(
            image, (1024, 574))
        transparent = pygame.Surface((205, 25), pygame.SRCALPHA)
        transparent.fill((0, 0, 0, 140))
        image.blit(transparent, (10, 10))
        _background_images[scene_ref] = image


def load_portrait_images():
    """
    Charge l'ensemble des images des portraits des personnages du jeu
    """
    for image_path in glob.glob(os.path.join(
            data.get_image_path("characters"), "*.png")):
        filename = os.path.splitext(os.path.basename(image_path))[0]
        charact_ref, position = filename.split("_")
        image = pygame.image.load(image_path).convert_alpha()
        if not charact_ref in _portrait_images:
            _portrait_images[charact_ref] = {}
        _portrait_images[charact_ref][position] = image
