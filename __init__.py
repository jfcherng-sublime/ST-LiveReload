#!/usr/bin/python

try:
    from .LiveReload import *
    from .server import *
except ValueError:
    from LiveReload import *
    from server import *
