# encoding: utf-8
import os
import time

from sikuli import * # pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import

from .utils import *

def get_nox(config):
    nox = os.environ.get("REGION")
    if nox:
        return Region(*[int(x) for x in nox.split(",")])

    datafile = os.path.join(APP_ROOT, '.region')
    if os.path.isfile(datafile):
        with open(datafile) as fp:
            nox = fp.read().strip()
        try:
            nox = Region(*[int(x) for x in nox.split(",")])
        except:
            nox = None
    if nox:
        nox.highlight()
        q = u'前回と同じ範囲で実行します。よろしいですか？'
        response = popAsk(q)
        nox.highlightOff()
        if response:
            return nox

    nox_path = config.get('Nox', 'path')

    if Settings.isWindows() and nox_path:
        nox = Nox(nox_path)
        if nox.is_running():
            Debug.user("app: %s, running: %s, windows: %s", nox.app, nox.app.isRunning(), nox.app.windows)
            return nox
        else:
            Debug.info("Nox is not running")

    popup(u"次の画面で操作対象の範囲を選択します。ゲームを準備して最前面に出し、 OK を押してください。", u"アプリケーションを準備")
    # Sikuli sometimes varnish message very fast.
    # Add wait to avoit the issue.
    time.sleep(1)
    nox = selectRegion(u"Click and drag the game screen.")
    with open(datafile, 'w') as fp:
        fp.write('%d,%d,%d,%d' % (nox.x, nox.y, nox.w, nox.h))
    Debug.info("Nox region: %s", nox)
    return nox

class Nox(object):
    """Wrapper for NoxPlayer app"""
    TITLEBAR_HEIGHT = 32
    TOOLBAR_WIDTH_THRESHOLD = 100

    def __init__(self, nox_path, label=None):
        self.label = label
        self.app = App(nox_path) # on mac, "Nox App Player"?
        self.region = None

    def focus(self):
        if self.label:
            self.app.focus(self.label)
        else:
            self.app.focus()

    def is_running(self):
        return self.app.isRunning() and self.app.hasWindow()

    def get_region(self, update=False):
        """Get Region instance of Nox's main area.

        Nox usually has multiple windows.
        At first, need to detect the main area.
         -----------------------     A
        | Nox Player          x |    |
        |-----------------------| A  |
        |                   | - | |  |
        |                   |   | |  | window, sidebar (unmaximized)
        |                   | - | |  |
        |                   |   | |  |
        |                   | - | | sidebar (maximized)
        |                   |   | |  |
         -----------------------  V  V
        *1: When app area is enough narrower than Nox Player window
        <- window -------------->
          <-- app ------->
                            <--->
                              `sidebar

        *2: When app area is "fit" to Nox Player window
        <- window, app ---------><--> sidebar

        In maxmized mode, sidebar is located outside of the main window."""

        if self.region is None or update:
            main_window = None
            window_list = self.app.windows
            for app_window in window_list:
                if app_window.w < self.TOOLBAR_WIDTH_THRESHOLD:
                    window_list.remove(app_window)
                    break

            # Pattern 1. Nox has a container window (with titlebar)
            #            and smaller app window
            for app_window in window_list:
                if app_window.x != min([w.x for w in self.app.windows]):
                    main_window = app_window
                    break

            # Pattern 2. Nox has only the main window (with titlebar)
            if main_window is None:
                for app_window in window_list:
                    if app_window.h == max([w.h for w in self.app.windows]):
                        main_window = app_window
                        break

            region = Region(main_window)
            if region.x == min([w.x for w in self.app.windows]):
                region.setY(region.getY() + self.TITLEBAR_HEIGHT)
                region.setH(region.getH() - self.TITLEBAR_HEIGHT)
            self.region = region

        return self.region
