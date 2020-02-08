# encoding: utf-8

import os
import signal
import time
import inspect
import importlib
import pkgutil

import org.sikuli.script.SikulixForJython
from sikuli import * # pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import

from utils import *
from nox import Nox, NoxApp

SIGINT_CALLED = False

def is_sigint_call():
    global SIGINT_CALLED
    return SIGINT_CALLED

def sigint_handler(_num=None, _frame=None):
    """Catch Ctrl-C in Jython"""
    global SIGINT_CALLED
    SIGINT_CALLED = True
    exit()

signal.signal(signal.SIGINT, sigint_handler)

def do_loop(app):
    while True:
        try:
            sleep_sec = app.run()
            if sleep_sec is None:
                sleep_sec = app.default_interval
            sleep_sec = random_sec(sleep_sec)

            app.sleep(sleep_sec, reason="", log=True)
        except KeyboardInterrupt:
            sigint_handler()

def is_debug():
    return str(os.environ.get("DEBUG")).lower() == "true"

def get_all_macros():
    all_macros = []
    for _, name, is_package in pkgutil.iter_modules(['macros']):
        plugin_path = 'macros.{}'.format(name)
        importlib.import_module(plugin_path)
        all_macros += [
                    m[1] for m in inspect.getmembers(
                sys.modules[plugin_path],
                lambda member: inspect.isclass(member) and issubclass(member, NoxApp)
                )]
    return all_macros

def ask_macro(macro):
    all_macros = get_all_macros()
    choises = ["%s %s" % (v.app_name(), v.label()) for v in all_macros]
    if macro:
        return [kls for kls in all_macros if ".".join([kls.app_name(), kls.macro_name()]) == macro][0]
    else:
        macro = select(u"実行内容を選んでください", u"作業選択", choises)
    if not macro:
        return None

    return all_macros[choises.index(macro)]

def get_nox(nox_path):
    nox = os.environ.get("REGION")
    if nox:
        return Region(*[int(x) for x in nox.split(",")])

    if Settings.isWindows() and nox_path:
        nox = Nox(nox_path)
        if nox.is_running():
            Debug.user("app: %s, running: %s, windows: %s", nox.app, nox.app.isRunning(), nox.app.windows)
            return nox
        else:
            Debug.info("Nox is not running")

    popup(u"NoxPlayer を準備し、最前面に出して OK を押してください。", u"Nox を準備")
    # Sikuli sometimes varnish message very fast.
    # Add wait to avoit the issue.
    time.sleep(1)
    nox = selectRegion(u"Nox の画面範囲をドラッグして選択")
    Debug.info("Nox region: %s", nox)
    return nox


Settings.LogTime = True
Settings.UserLogs = is_debug()
Settings.ActionLogs = is_debug()
Settings.AutoWaitTimeout = 1
Settings.WaitScanRate = 10
Settings.ObserveScanRate = 0.2
