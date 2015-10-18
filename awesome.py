from keyboard_watcher import KeyboardAndMouseWatcher
from multiprocessing import Queue
import time
from sys import platform as _platform
import pygame
import os

path = os.path.abspath(__file__+"/../")

print path
import random

if _platform == "linux" or _platform == "linux2":
    sound_files = {
        'clicks' : ["model_m/new_click_2.ogg","model_m/new_click_4.ogg","model_m/new_click_5.ogg","model_m/new_click_6.ogg","model_m/new_click_7.ogg","model_m/new_click_8.ogg"],
        'space' : ["model_m/click_6.ogg","model_m/click_1.ogg","model_m/click_2.ogg","model_m/click_3.ogg"],
        'carriage_returns' : ["model_m/carriage_return_1.ogg","model_m/carriage_return_2.ogg","model_m/carriage_return_3.ogg"],
    }
elif _platform == "win32":
    # The reason why win32 support is needed for this is because with pyHook, instead of "space" and "carriage_returns", it is "Space" and "Return".
    sound_files = {
        'clicks' : ["model_m/new_click_2.ogg","model_m/new_click_4.ogg","model_m/new_click_5.ogg","model_m/new_click_6.ogg","model_m/new_click_7.ogg","model_m/new_click_8.ogg"],
        'Space' : ["model_m/click_6.ogg","model_m/click_1.ogg","model_m/click_2.ogg","model_m/click_3.ogg"],
        'Return' : ["model_m/carriage_return_1.ogg","model_m/carriage_return_2.ogg","model_m/carriage_return_3.ogg"],
    }

if _platform == "linux" or _platform == "linux2":
    key_roles = {
        (36,) : 'carriage_returns',
        (65,) : 'space',
    }

if __name__ == '__main__':

    print "Awesome Keyboard: Starting up and initializing Awesome Keyboard..."

    event_queue = Queue()
    watcher = KeyboardAndMouseWatcher("keyboard_and_mouse",event_queue)
    watcher.start()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    sounds = {}

    mouse_down = pygame.mixer.Sound(os.path.join(path,'sounds','mouse','buttondown_1.ogg'))
    mouse_up = pygame.mixer.Sound(os.path.join(path,'sounds','mouse','buttonup_1.ogg'))

    for sound_name,filenames in sound_files.items():
        sounds[sound_name] = []
        for filename in filenames:
            sound_path = os.path.join(path,'sounds',filename)
            sounds[sound_name].append(pygame.mixer.Sound(sound_path)) # Loud sound.
    current_channel = 0

    print "Awesome Keyboard: Using %d channels." % pygame.mixer.get_num_channels()

    clicks_by_keycodes = {}
    try:
        while True:
            time.sleep(0.01)
            while not event_queue.empty():
                key,value = event_queue.get()
                if value[0] == 'keys_pressed':
                    played = False
                    if _platform == "linux" or _platform == "linux2":
                        for keys,sound_name in key_roles.items():
                            if value[1] in keys:
                                i = random.randrange(0,len(sounds[sound_name]))
                                sounds[sound_name][i].play()
                                played = True
                                break
                    elif _platform == "win32":
                        for sound_name in ["Space", "Return"]:
                            if value[1] in sound_name:
                                i = random.randrange(0,len(sounds[sound_name]))
                                sounds[sound_name][i].play()
                                played = True
                                break
                    if not played:
                        i = random.randrange(0,len(sounds['clicks']))
                        sounds['clicks'][i].play()
                    print value[1]
                elif value == 'button_up':
                    mouse_up.play()
                elif value == 'button_down':
                    mouse_down.play()

    except KeyboardInterrupt:
        print "Awesome Keyboard: Terminating application."
        watcher.terminate()
        exit(1)
