import vapoursynth as vs


__all__ = ['retrieve_core']


_get_core = vs.get_core
def retrieve_core():
    return _get_core()



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