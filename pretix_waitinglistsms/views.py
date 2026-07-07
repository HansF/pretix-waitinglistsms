from django.urls import reverse
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin

from .forms import WaitingListSmsSettingsForm


class WaitingListSmsSettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = WaitingListSmsSettingsForm
    template_name = "pretix_waitinglistsms/settings.html"
    permission = "event.settings.general:write"

    def get_success_url(self, **kwargs):
        return reverse(
            "plugins:pretix_waitinglistsms:settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
