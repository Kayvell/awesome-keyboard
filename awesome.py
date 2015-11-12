from keyboard_watcher import KeyboardAndMouseWatcher
from multiprocessing import Queue
import time

debug = False

from sys import platform as _platform
if _platform.startswith("linux"):
    try:
        import pygame
    except ImportError, e:
        print 'Missing dependency:', e.message[16:]
        print 'Please look at the readme of this application to learn how to install the dependency using Pip.'
        sys.exit(1)
elif _platform == "win32":
    # Windows operating systems should use the built-in winsound module to load .wav sound files instead of .ogg files.
    import winsound
import os

path = os.path.abspath(__file__+"/../")

import random

if _platform.startswith("linux"):
    sound_files = {
        'clicks' : ["model_m/new_click_2.ogg","model_m/new_click_4.ogg","model_m/new_click_5.ogg","model_m/new_click_6.ogg","model_m/new_click_7.ogg","model_m/new_click_8.ogg"],
        'space' : ["model_m/click_6.ogg","model_m/click_1.ogg","model_m/click_2.ogg","model_m/click_3.ogg"],
        'carriage_returns' : ["model_m/carriage_return_1.ogg","model_m/carriage_return_2.ogg","model_m/carriage_return_3.ogg"],
    }
elif _platform == "win32":
    # The reason why win32 support is needed for this is because with pyHook, instead of "space" and "carriage_returns", it is "Space" and "Return".
    sound_files = {
        'clicks' : ["model_m/new_click_2.wav","model_m/new_click_4.wav","model_m/new_click_5.wav","model_m/new_click_6.wav","model_m/new_click_7.wav","model_m/new_click_8.wav"],
        'Space' : ["model_m/click_6.wav","model_m/click_1.wav","model_m/click_2.wav","model_m/click_3.wav"],
        'Return' : ["model_m/carriage_return_1.wav","model_m/carriage_return_2.wav","model_m/carriage_return_3.wav"],
    }

if _platform.startswith("linux"):
    key_roles = {
        (36,) : 'carriage_returns',
        (65,) : 'space',
    }

if __name__ == '__main__':

    print "Awesome Keyboard: Starting up and initializing Awesome Keyboard..."

    event_queue = Queue()
    watcher = KeyboardAndMouseWatcher("keyboard_and_mouse", event_queue)
    watcher.start()
    if _platform.startswith("linux"):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

    sounds = {}

    if _platform.startswith("linux"):
        mouse_down = pygame.mixer.Sound(os.path.join(path,'sounds','mouse','buttondown_1.ogg'))
        mouse_up = pygame.mixer.Sound(os.path.join(path,'sounds','mouse','buttonup_1.ogg'))
    elif _platform == "win32":
        mouse_down = 'sounds/mouse/buttondown_1.wav'
        mouse_up = 'sounds/mouse/buttonup_1.wav'

    for sound_name,filenames in sound_files.items():
        sounds[sound_name] = []
        for filename in filenames:
            if _platform.startswith("linux"):
                sound_path = os.path.join(path,'sounds',filename)
                sounds[sound_name].append(pygame.mixer.Sound(sound_path)) # Loud sound.
            elif _platform == "win32":
                sound_path = os.path.join('sounds' + '/' + filename)
                sounds[sound_name].append(sound_path) # Load sound.
    current_channel = 0

    if _platform.startswith("linux"):
        print "Awesome Keyboard: Using %d channels." % pygame.mixer.get_num_channels()

    clicks_by_keycodes = {}
    try:
        while True:
            time.sleep(0.01)
            while not event_queue.empty():
                key,value = event_queue.get()
                if value[0] == 'keys_pressed':
                    played = False
                    if _platform.startswith("linux"):
                        for keys,sound_name in key_roles.items():
                            if value[1] in keys:
                                i = random.randrange(0,len(sounds[sound_name]))
                                sounds[sound_name][i].play()
                                played = True
                                break
                        if not played:
                            i = random.randrange(0,len(sounds['clicks']))
                            sounds['clicks'][i].play()
                    elif _platform == "win32":
                        for sound_name in ["Space", "Return"]:
                            if value[1] in sound_name:
                                i = random.randrange(0,len(sounds[sound_name]))
                                winsound.PlaySound(sounds[sound_name][i], winsound.SND_FILENAME)
                                played = True
                                break
                        if not played:
                            i = random.randrange(0,len(sounds['clicks']))
                            winsound.PlaySound(sounds['clicks'][i], winsound.SND_FILENAME)
                    if debug:
                        print value[1]
                elif value == 'button_up':
                    if _platform.startswith("linux"):
                        mouse_up.play()
                    elif _platform == "win32":
                        winsound.PlaySound(mouse_up, winsound.SND_FILENAME)
                elif value == 'button_down':
                    if _platform.startswith("linux"):
                        mouse_down.play()
                    elif _platform == "win32":
                        winsound.PlaySound(mouse_down, winsound.SND_FILENAME)

    except KeyboardInterrupt:
        print "Awesome Keyboard: Terminating application."
        watcher.terminate()
        exit(1)
