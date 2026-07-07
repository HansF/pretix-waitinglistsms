__version__ = "0.1.0"


def __getattr__(name):
    if name == "PretixPluginMeta":
        from .apps import WaitingListSmsApp

        return WaitingListSmsApp
    raise AttributeError(name)
