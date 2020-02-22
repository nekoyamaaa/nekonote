# encoding: utf-8

import sys

import nekonote

config = nekonote.load_config()

try:
    macroname = sys.argv[1]
except IndexError:
    macroname = None
target = nekonote.ask_macro(macroname)

if not target:
    sys.exit()

nox = nekonote.get_nox(config)
APP = target(nox, config)

nekonote.do_loop(APP)
