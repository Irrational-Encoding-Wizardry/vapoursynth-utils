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

from vapoursynth_utils.autoload import register_path, autoload
from vapoursynth_utils.plugins import load_local_plugin, get_local_plugin_names


__all__ = [
    'initialize', 'autoload',

    'load_local_plugin', 'get_local_plugin_names'
]


def initialize():
    register_path()
    autoload()

