from django.urls import re_path

from .views import WaitingListSmsSettingsView

urlpatterns = [
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/waiting-list-sms/settings$",
        WaitingListSmsSettingsView.as_view(),
        name="settings",
    ),
]
