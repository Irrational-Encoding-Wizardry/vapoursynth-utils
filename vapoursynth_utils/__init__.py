# -*- coding: utf-8 -*-

"""Top-level package for vapoursynth-utils."""

__author__ = """vapoursynth-utils"""
__email__ = 'wizards@encode.moe'
__version__ = '0.1.0'


import vapoursynth as vs
import platform
import weakref
import glob
import sys
import os

_get_core = vs.get_core
_KNOWN_CORES = weakref.WeakSet()


__all__ = ["autoload", "initialize", "get_local_plugin_names", "load_local_plugin"]


def get_dll_extension():
    system = platform.system()
    if system=="Windows":
        return "*.dll"
    else:
        return "*.so"


def get_autoload_path(name):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        name
    )


def perform_autoload(core):
    """
    This function actually performs the auto-load
    """
    for file in glob.glob(os.path.join(get_autoload_path('vapoursynth-plugins'), f'**/{get_dll_extension()}')):
        core.std.LoadPlugin(file)


def autoload(core=None):
    if core is None:
        core = _get_core()
    if core in _KNOWN_CORES:
        return
    try:
        perform_autoload(core)
    finally:
        _KNOWN_CORES.add(core)


def register_path():
    sys.path.insert(1, '$VAPOURSYNTH-SCRIPTS$2')
    path = get_autoload_path('vapoursynth-plugins')
    for dir in os.listdir(path):
        dir = os.path.join(path, dir)
        if not os.path.isdir(dir):
            continue
        sys.path.insert(1, dir)
    sys.path.insert(1, '$VAPOURSYNTH-SCRIPTS$1')


def initialize():
    register_path()
    autoload()


def get_local_plugin_names():
    path = get_autoload_path('vapoursynth-plugins')
    for dir in os.listdir(path):
        dir = os.path.join(path, dir)
        if not os.path.isdir(dir):
            continue
        yield os.path.split(dir)[1]


def load_local_plugin(name):
    for file in glob.glob(os.path.join(get_autoload_path('vapoursynth-plugins'), name, get_dll_extension())):
        _get_core().std.LoadPlugin(file)


if vs._using_vsscript:
    # We are using VSScript.
    # To ensure that we have autoload, we monkey-patch get_core and core.core
    class VSUtilProxy(vs.core.__class__):
        @property
        def core(self):
            core = super(self._vsutilproxy_class, self).core
            autoload(core)
            return core

    VSUtilProxy._vsutilproxy_class = VSUtilProxy
    def get_core(*args, **kwargs):
        core = _get_core(*args, **kwargs)
        autoload(core)
        return core

    vs.get_core = get_core
    vs.core = VSUtilProxy.__new__(VSUtilProxy)
    del VSUtilProxy
    del get_core
