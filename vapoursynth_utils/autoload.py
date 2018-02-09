import os
import sys
import glob
import weakref

from vapoursynth_utils.utils import get_autoload_path, get_dll_extension
from vapoursynth_utils.vsscript import retrieve_core
from vapoursynth import core

_KNOWN_CORES = weakref.WeakSet()



def perform_autoload(core):
    """
    This function actually performs the auto-load
    """
    for file in glob.glob(os.path.join(get_autoload_path('vapoursynth-plugins'), f'**/{get_dll_extension()}')):
        core.std.LoadPlugin(file)


def autoload(core=None):
    if core is None:
        core = retrieve_core()
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
