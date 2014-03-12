#Awesome-Keyboard!

Do you also miss the good ole days of clunky, **clicky** computer keyboards ([like this one](http://en.wikipedia.org/wiki/Model_M_keyboard))? Use this script to make your laptop keyboard sound awesome again!

##What is it?

A small Python script that simulates the sound of classic computer keyboards under **Ubuntu**. Currently, the only available "*sound theme*"" is a simulation of the **IBM Model M** (the quality of the sound files is still far from ideal though, I hope to improve this soon).

##Installation & Usage

Installation and usage is pretty easy (provided you're on Ubuntu, otherwise it's impossible ;))

    #Download code and sound files
    git clone git@github.com:adewes/awesome-keyboard.git
    cd awesome-keyboard

    #Install dependencies
    pip install -R requirements.txt #install pygame and xlib

    #Run it
    python awesome.py

    #Enjoy :)

##Why on Earth!?

Here at Hacker School people are quite passionate about keyboards, so there is a lot of clacking noise in the background (not that I would be disturbed by this ;)). Personally, I work on a Thinkpad T430 and love its [*island-style keyboard*](http://blog.laptopmag.com/thinkpad-type-off-is-lenovos-new-island-style-keyboard-better-or-worse), so I don't want to replace it with a different one. Hence I thought it might be interesting to see if I could produce a convincing simulation of "real" keyboard sounds using some Python magic :)

##How This Works

The script creates a watcher process that uses the Xlib to listen to keyboard and mouse events. Whenever it encounters a keyboard event, it sends the key code to main process, which then picks out an adequate sound for the key that has been pressed and plays it using **pygame**.

##Planned Improvements

Currently I used a sound file from [Wikimedia](http://commons.wikimedia.org/wiki/File:Modelm.ogg) from which I extracted various samples. The quality of these is not great and for some of the clicks there is a noticeable lag between the key stroke and the sound. Since we have an actual Model M keyboard here I will probably write a small script to record and store the sounds of individual keys using a microphone, which should yield a much better and more convincing auditory experience than this prototype.

Armed with that script, people could start recording the sounds of their own keyboards and share them with others through Github, thus creating a database of keyboard sounds. Who know, maybe our grandchildren, only used  will find this fascinating

##Limitations

Measuring the *intensity* with which the user hits a given key is impossible in most cases, although on laptops one could possibly use the microphone to measure the vibration caused by each stroke and determine the intensity from this (or even use the built-in vibration sensors that exist e.g. in Thinkpads).