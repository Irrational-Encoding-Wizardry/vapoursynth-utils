import os.path
import platform


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