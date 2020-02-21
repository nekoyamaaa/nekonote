# encoding: utf-8

import sys

import NoxAutomator

config = NoxAutomator.load_config()

try:
    macroname = sys.argv[1]
except IndexError:
    macroname = None
target = NoxAutomator.ask_macro(macroname)

if not target:
    sys.exit()

nox = NoxAutomator.get_nox(config)
APP = target(nox, config)

NoxAutomator.do_loop(APP)
