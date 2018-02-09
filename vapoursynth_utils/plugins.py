import os, os.path
import glob
from vapoursynth_utils.utils import get_autoload_path, get_dll_extension

from vapoursynth_utils.vsscript import retrieve_core


def get_local_plugin_names():
    path = get_autoload_path('vapoursynth-plugins')
    for dir in os.listdir(path):
        dir = os.path.join(path, dir)
        if not os.path.isdir(dir):
            continue
        yield os.path.split(dir)[1]


def load_local_plugin(name):
    for file in glob.glob(os.path.join(get_autoload_path('vapoursynth-plugins'), name, get_dll_extension())):
        retrieve_core().std.LoadPlugin(file)
