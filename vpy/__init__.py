from vapoursynth_utils import get_local_plugin_names
from vapoursynth_utils import load_local_plugin
from vapoursynth import core
import vapoursynth

import sys
from types import ModuleType
from importlib.abc import Loader, Finder


class DeferredFilter(ModuleType):

    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    @property
    def filter(self):
        """Returns the current function object"""
        return getattr(getattr(core, self.namespace), self.name)

    def __call__(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def __repr__(self):
        return "<DeferredFilter %s.%s>" % (self.namespace, self.name)


class VapoursynthExtension(ModuleType):
    
    @classmethod
    def from_name(cls, name):
        class FakeNS:
            pass
        fns = FakeNS()
        fns.name = name
        return cls(fns)

    def __init__(self, spec):
        super(VapoursynthExtension, self).__init__(spec.name)
        
        self.__package__ = "vpy"
        self._name = spec.name
        if self._name.startswith("vpy."):
            self._name = self._name[4:]

        if not hasattr(core, self._name):
            load_local_plugin(self._name)

    def __getattr__(self, name):
        if name in self.get_functions():
            return DeferredFilter(self._name, name)
        return super(VapoursynthExtension, self).__getattribute__(name)

    @property
    def __all__(self):
        return list(self.get_functions())
    
    def get_functions(self):
        data = set()
        for plugin in core.get_plugins().values():
            if plugin['namespace'] == self._name:
                data |= set(plugin['functions'].keys())
        return data

        
class VPyModuleLoader(Loader):
    """
    Loads vapoursynth-extensions as modules.
    """

    def create_module(self, spec):
        if spec.name == "vpy":
            module = VpyModule(spec)
            module.__package__ = "vpy"
            module.__path__ = None
            return module
        
        return VapoursynthExtension(spec)

    def exec_module(self, module):
        pass
        
    def module_repr(self, module):
        return "<VapourSynthNamespace %s>"%(module._name)


class VapoursynthPluginImporter(Finder):

    def __init__(self):
        self.loader = VPyModuleLoader()

    @property
    def known_namespaces(self):
        namespaces = set()
        for plugin in core.get_plugins().values():
            namespaces.add(plugin['namespace'])
        return namespaces

    @property
    def namespaces(self):
        return self.known_namespaces | set(get_local_plugin_names())

    def find_module(self, fullname, path=None):
        if not fullname.startswith("vpy."):
            return None

        fullname = fullname[4:]
        
        if fullname in self.namespaces:
            return self.loader
        return None


importer = VapoursynthPluginImporter()
sys.meta_path.append(importer)
