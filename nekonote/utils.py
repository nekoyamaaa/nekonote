# encoding: utf-8
import os
import time
import random
import ConfigParser

import java.awt.Toolkit
import java.io
from java.applet.Applet import newAudioClip

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(APP_ROOT, "data")
MACRO_DIR = os.path.join(APP_ROOT, "macros")

def beep():
    """Execute beep through Java"""
    java.awt.Toolkit.getDefaultToolkit().beep()

def play_sound(filename):
    filepath = os.path.join(DATA_DIR, "sounds", filename)
    if not os.path.isfile(filepath):
        raise Exception("No such file: {}".format(filepath))
    newAudioClip(java.io.File(filepath).toURL()).play()
    # Keep python running until Java load and play the sound file
    time.sleep(0.5)

def random_sec(median_or_range):
    """Generate random int suitable for time.sleep"""
    if isinstance(median_or_range, int):
        median = median_or_range
        if median >= 6:
            width = 6
        elif median <= 1:
            width = 0.2
        else:
            width = 1
        minsec = median - width
        maxsec = median + width
    else:
        try:
            minsec, maxsec = median_or_range
        except ValueError:
            raise TypeError("random_sec() takes int or sequence type")

    if minsec < 0:
        minsec = 0
    precision = 1000.0
    return random.randint(int(minsec*precision), int(maxsec*precision))/precision

def humanize_sec(t):
    minute, sec = divmod(int(t), 60)
    hour, minute = divmod(minute, 60)
    return "%dh%02dm%02ds" % (hour, minute, sec)


def load_config():
    from sikuli import Settings
    if Settings.isWindows():
        nox_path = r'C:\Program Files (x86)\Nox\bin\Nox.exe'
    else:
        nox_path = None
    config = ConfigParser.SafeConfigParser(
        allow_no_value=True,
        defaults={
            'path': nox_path,
        }
    )
    config.read([
        os.path.join(DATA_DIR, "default.ini"),
        os.path.join(APP_ROOT, "settings.ini"),
    ])

    return config
