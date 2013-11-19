import os.path

import pygame.mixer

import data

LOOP = -1


def load_music(music_ref):
    music_path = data.get_sound_path(
        os.path.join("music", music_ref + ".ogg"))
    pygame.mixer.music.load(music_path)


def play_music(music_ref=None, loops=0, start=0.0):
    if music_ref:
        load_music(music_ref)
    pygame.mixer.music.play(loops, start)


def loop_music(music_ref=None):
    play_music(music_ref, LOOP)


def stop_music(fadeout_time=0):
    if fadeout_time > 0:
        pygame.mixer.music.fadeout(fadeout_time)
    else:
        pygame.mixer.music.stop()


def toggle_music(fadeout_time=0):
    if pygame.mixer.music.get_busy():
        stop_music(fadeout_time)
    else:
        play_music()


def set_music_volume(volume):
    pygame.mixer.music.set_volume(volume)


def get_music_volume():
    return pygame.mixer.music.get_volume()


def play_sound(sound_ref, loops=0, maxtime=0, fade_ms=0):
    sound_path = data.get_sound_path(
        os.path.join("sounds", sound_ref + ".ogg"))
    sound = pygame.mixer.Sound(sound_path)
    pygame.mixer.find_channel().play(sound, loops, maxtime, fade_ms)
