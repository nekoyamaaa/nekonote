# encoding: utf-8
import ConfigParser
import glob
import os
import time
import traceback

from sikuli import * # pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import

from .sikulimod import MatchedImage
from .utils import *
from .nox import Nox
from .exceptions import ScreenUnknownError

# Can not name it "App" or it conflicts with sikuli.App
class Macro(object):
    APP_NAME = None
    LABEL = None

    IMAGE_ORIGINAL_WINDOW_HEIGHT = 375
    IMAGE_ORIGINAL_WINDOW_WIDTH = 667
    UNKNOWN = "unknown"
    HIGHLIGHT_SEC = 1
    CONFIG_JOINER = '.'

    @classmethod
    def app_name(self):
        if self.APP_NAME:
            return self.APP_NAME
        for part in self.__module__.split("."):
            if part == "macros":
                continue
            return part

    @classmethod
    def label(self):
        return self.LABEL

    @classmethod
    def macro_name(self):
        return self.__name__

    def __init__(self, app, config):
        self.app = None
        self.config = config
        self.scale = 1
        self.set_region(app)
        self.last_updated_at = None
        self.unknown_count = 0
        self.app_name = self.__class__.app_name()
        self.macro_name = self.__class__.macro_name()
        self.target = None
        self.scale_base = "width"

        if self.app:
            self.app.focus()
        self.prepare()
        self.default_interval = None
        if not config.has_section(self.config_key):
            self.config.add_section(self.config_key)
        try:
            self.default_interval = self.config.getint(
                self.config_key,
                "interval"
            )
        except ConfigParser.NoOptionError:
            pass
        if not self.default_interval:
            try:
                self.default_interval = self.DEFAULT_INTERVAL
            except NameError:
                self.default_interval = 10
        Debug.user("Interval: %d", self.default_interval)

        self.max_unknown = None
        try:
            self.max_unknown = self.config.getint(
                self.config_key,
                'max_unknown'
            )
        except ConfigParser.NoOptionError:
            pass
        if not self.max_unknown:
            self.max_unknown = 6
        Debug.user("MUN: %d", self.max_unknown)

        self.get_region().highlight(self.HIGHLIGHT_SEC)
        self.last_match = None

        imgdirname = os.path.join(MACRO_DIR, self.app_name, "data")

        self.screen_candidates = []
        for name in ["Common", self.macro_name]:
            appimgdirname = os.path.join(imgdirname, name)
            if os.path.isdir(appimgdirname):
                Debug.info("Loading images from %s", appimgdirname)
                addImagePath(appimgdirname)
                for image in glob.glob(os.path.join(appimgdirname, "*-*.png")):
                    self.screen_candidates.append(os.path.basename(image))
            else:
                Debug.error('%s is not a directory', appimgdirname)
        Debug.info("Loaded images: %s", " ".join(self.screen_candidates))
        if not self.screen_candidates:
            raise Exception("No images in data dir")

    @property
    def config_key(self):
        return self.CONFIG_JOINER.join([self.app_name, self.macro_name])

    def prepare(self):
        if self.app:
            if not self.app.is_running():
                raise Exception("NoxPlayer is not running")

        self.adjust_scale()

    def adjust_scale(self):
        if self.scale_base == "width":
            scale = self.get_region().w / float(self.IMAGE_ORIGINAL_WINDOW_WIDTH)
        else:
            scale = self.get_region().h / float(self.IMAGE_ORIGINAL_WINDOW_HEIGHT)
        if scale != self.scale:
            self.scale = scale
            Settings.AlwaysResize = self.scale
            Debug.info("Scale images to x%.2f", self.scale)

    def get_region(self):
        if self.app:
            return self.app.get_region()
        return self.region

    def get_target(self):
        if self.target:
            return self.target
        return self.get_region()

    def get_scaled_location(self, x, y):
        if x > 1 or y > 1:
            raise ArgumentError("Use decimal instead of percentage")
        reg = Region(self.get_region())
        loc = reg.getTopLeft()
        loc.setX(loc.getX() + (reg.getW() * x))
        loc.setY(loc.getY() + (reg.getH() * y))
        return loc

    def get_scaled_region(self, x1, y1, x2, y2):
        top_left = self.get_scaled_location(x1, y1)
        bottom_right = self.get_scaled_location(x2, y2)

        reg = Region(
            top_left.getX(),
            top_left.getY(),
            bottom_right.getX() - top_left.getX(),
            bottom_right.getY() - top_left.getY()
        )
        return reg

    def set_region(self, region):
        self.region = None
        if isinstance(region, Nox):
            self.app = region
            return

        if region:
            try:
                self.region = Region(region)
            except:
                Debug.error(
                    "Could not convert %s to Region.  Use entire screen as Region",
                    region)

        if self.region is None:
            self.region = Region(Screen())

    def detect_current(self, retry=1):
        result = None
        with self.get_target():
            for _ in range(retry):
                matches = findAnyList(self.screen_candidates)
                self.last_updated_at = time.time()
                if matches:
                    matched_images = []
                    for m in matches:
                        match = MatchedImage(m, self.screen_candidates)
                        if Settings.UserLogs:
                            match.highlight(self.HIGHLIGHT_SEC)
                        Debug.user("%s: %.2f", str(match.filename), match.get_score())
                        if match.get_score >= 0.75:
                            matched_images.append(match)
                            if result is None:
                                result = match
                            elif match.get_score() > result.get_score():
                                result = match

                    matched_images.sort(key=lambda image: image.get_score(), reverse=True)
                    if result.label is None:
                        for image in matched_images:
                            if (result.screen == image.screen) and image.label:
                                result = image
                                break
                    if result:
                        break
                wait(1)

        if result:
            msg = "Current screen: {}, matched image {}".format(
                result.screen,
                result.filename
                )
            self.unknown_count = 0
        else:
            msg = "Current screen: {}".format(self.UNKNOWN)
            self.unknown_count += 1
            if self.unknown_count and self.unknown_count > self.max_unknown:
                raise ScreenUnknownError()


        self.last_match = result
        Debug.info(msg)
        return result

    def close_dialog(self, do_wait=False, expected=True):
        """
        True - dialog found and successfully closed
        False - dialog found but failed to close it
        None - No dialogs found
        """
        pattern = Pattern("confirm.png")
        with self.get_region():
            button = self.click_button(pattern, do_wait=do_wait)
            if not button:
                if expected:
                    logger = Debug.error
                else:
                    logger = Debug.user
                logger("No dialog found.")
                return None

        try:
            return Region(button).waitVanish(pattern, 10)
        except:
            # waitVanish rarely raises error on searching pattern
            Debug.error("No changes after clicking Confirm button")
            Debug.error(str(traceback.format_exc()))
            return False

    def wait_change(self, reg, sec=60):
        Debug.info("Watch any changes in %s for %s sec", reg, sec)
        reg.highlight(3)
        # Ugg, OpenCV raises error when images are resized.
        Settings.AlwaysResize = 1
        reg.onChange(lambda e: e.stopObserver())
        reg.observe(sec)
        reg.stopObserver()
        Settings.AlwaysResize = self.scale

    def click_button(self, button, do_wait=False):
        with self.get_region():
            reg = None
            if do_wait:
                try:
                    reg = wait(button, 5)
                except FindFailed:
                    pass
            else:
                sim = 0.95
                while sim >= 0.8:
                    try:
                        reg = find(button.similar(sim))
                        break
                    except FindFailed:
                        sim -= 0.05
            if reg is None:
                return False

            Debug.user("Button %s %s", button, reg)
            reg.highlight(self.HIGHLIGHT_SEC)
            reg.click()
            self.sleep(1.5)
            return reg

    def type(self, text, force_focus=False):
        if self.app:
            self.app.focus()
        if force_focus:
            with self.get_region():
                # Set focus to the app forcefully
                # because Nox does not accept hotkey if we just switch to it with keyboard
                click()
        type(text)

    def sleep(self, duration, reason=None, log=False):
        if reason or log:
            Debug.info("sleep %ss... %s", duration, reason)
        time.sleep(duration)

    def read_message(self):
        self.sleep(1.5)
        self.get_scaled_location(0.5, 0.92).click()

    def play_error_sound(self):
        play_sound("error.wav")

    def play_notify_sound(self):
        play_sound("notify.wav")

    def ask(self, message=None, timeout=30, repeat=False):
        if repeat:
            while True:
                self.play_error_sound()
                pop_response = Do.popAsk(message, timeout)
                if pop_response is False:
                    exit()
                elif pop_response is None:
                    pass
                else:
                    break
        else:
            self.play_error_sound()
            pop_response = Do.popAsk(message)
            if pop_response is False:
                exit()

    def mapping(self, values):
        for key, value in values.items():
            values[key] = NoxButton(key, value, self)

        return values

class NoxButton:
    def __init__(self, label, region, app):
        self.app = app
        try:
            self.key = app.config.get(app.config_key, 'key_' + label)
            Debug.user('%s key = %s', label, self.key)
        except:
            self.key = None
        if self.key and self.key == self.key.upper():
            self.key = getattr(Key, self.key)
        self.region = self.app.get_scaled_region(*region)

    def click(self):
        if self.key:
            return self.app.type(self.key)
        return self.region.click()

    def highlight(self, sec=1):
        self.region.highlight(sec)

    def __repr__(self):
        return '<%s %s key=%s>' % (self.__class__, self.region, repr(self.key))

