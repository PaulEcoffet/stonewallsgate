import os.path

import pygame.mixer

import data

LOOP = -1


def load_music(music_ref):
    """
    Charge une musique en mémoire mais ne la joue pas
    music_ref - La référence de la musique
    """
    music_path = data.get_sound_path(
        os.path.join("music", music_ref + ".ogg"))
    pygame.mixer.music.load(music_path)


def play_music(music_ref=None, loops=0, start=0.0):
    """
    Joue la musique `music_ref`, la répète `loops` fois
    en commençant à la seconde `start`.
    Si loops = -1, alors la musique est jouée indéfiniment
    """
    if music_ref:
        load_music(music_ref)
    pygame.mixer.music.play(loops, start)


def loop_music(music_ref=None):
    """
    Joue en boucle infinie la musique `music_ref`.
    """
    play_music(music_ref, LOOP)


def stop_music(fadeout_time=0):
    """
    Stop la musique en train d'être jouée.
    Si fadeout_time > 0, alors la musique disparaît
    en fondu qui dure `fadeout_time` ms.
    """
    if fadeout_time > 0:
        pygame.mixer.music.fadeout(fadeout_time)
    else:
        pygame.mixer.music.stop()


def toggle_music(fadeout_time=0):
    """
    Active la musique si elle est éteinte, sinon,
    il la stoppe
    """
    if pygame.mixer.music.get_busy():
        stop_music(fadeout_time)
    else:
        play_music()


def set_music_volume(volume):
    """
    Defini le volume de la musique
    """
    pygame.mixer.music.set_volume(volume)


def get_music_volume():
    """
    Retourne le volume de la musique
    """
    return pygame.mixer.music.get_volume()


def play_sound(sound_ref, loops=0, maxtime=0, fade_ms=0):
    """
    Joue le son avec la référence `sound_ref` et le rejoue
    `loops` fois
    """
    sound_path = data.get_sound_path(
        os.path.join("sounds", sound_ref + ".ogg"))
    sound = pygame.mixer.Sound(sound_path)
    pygame.mixer.find_channel().play(sound, loops, maxtime, fade_ms)
