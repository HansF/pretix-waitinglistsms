from django.utils.translation import gettext_lazy as _

from . import __version__

try:
    from pretix.base.plugins import PLUGIN_LEVEL_EVENT, PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2025.7 or above to run this plugin!")


class WaitingListSmsApp(PluginConfig):
    default = True
    name = "pretix_waitinglistsms"
    verbose_name = _("Waiting list SMS notifications")

    class PretixPluginMeta:
        name = _("Waiting list SMS notifications")
        author = "Hans Fraiponts"
        version = __version__
        category = "INTEGRATION"
        level = PLUGIN_LEVEL_EVENT
        visible = True
        description = _(
            "Send SMS notifications through Pingram, Twilio, or a generic HTTP "
            "gateway when waiting list vouchers are assigned."
        )
        compatibility = "pretix>=2025.7"
        settings_links = [
            (
                (_("Communication"), _("Waiting list SMS")),
                "plugins:pretix_waitinglistsms:settings",
                {},
            ),
        ]
        navigation_links = []

    def ready(self):
        from . import signals  # NOQA
