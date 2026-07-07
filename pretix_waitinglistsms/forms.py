from django import forms
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SecretKeySettingsField, SettingsForm

from .message import DEFAULT_MESSAGE, format_message_template


class WaitingListSmsSettingsForm(SettingsForm):
    waitinglistsms_enabled = forms.BooleanField(
        label=_("Enable SMS notifications"),
        required=False,
        help_text=_(
            "Send an SMS in addition to the regular waiting list email when a "
            "voucher is assigned."
        ),
    )
    waitinglistsms_provider = forms.ChoiceField(
        label=_("SMS gateway"),
        choices=(
            ("pingram", "Pingram"),
            ("twilio", "Twilio"),
            ("webhook", _("Generic HTTP gateway")),
        ),
        required=False,
    )
    waitinglistsms_from = forms.CharField(
        label=_("Sender"),
        required=False,
        help_text=_(
            "For Twilio, enter the Twilio phone number or messaging service "
            "sender. For Pingram and generic webhooks, this is optional."
        ),
    )
    waitinglistsms_pingram_api_key = SecretKeySettingsField(
        label=_("Pingram API key"),
        required=False,
        help_text=_("Use an API key from the Environments section of the Pingram dashboard."),
    )
    waitinglistsms_pingram_type = forms.CharField(
        label=_("Pingram notification type"),
        required=False,
        help_text=_("Create an SMS notification in Pingram and enter its Type."),
    )
    waitinglistsms_pingram_base_url = forms.URLField(
        label=_("Pingram API base URL"),
        required=False,
        help_text=_(
            "Use https://api.ca.pingram.io or https://api.eu.pingram.io for "
            "regional Pingram environments."
        ),
    )
    waitinglistsms_twilio_account_sid = forms.CharField(
        label=_("Twilio Account SID"),
        required=False,
    )
    waitinglistsms_twilio_auth_token = SecretKeySettingsField(
        label=_("Twilio Auth Token"),
        required=False,
    )
    waitinglistsms_webhook_url = forms.URLField(
        label=_("Generic gateway URL"),
        required=False,
        help_text=_(
            "The plugin will POST JSON containing to, from, body, event, item, "
            "variation, and voucher_code."
        ),
    )
    waitinglistsms_message = forms.CharField(
        label=_("Message text"),
        required=False,
        widget=forms.Textarea,
        help_text=_(
            "Available placeholders: {event}, {item}, {variation}, "
            "{voucher_code}, {voucher_valid_until}, {url}."
        ),
    )

    def clean(self):
        data = super().clean()
        if not data.get("waitinglistsms_enabled"):
            return data

        provider = data.get("waitinglistsms_provider") or "pingram"
        if provider == "pingram":
            if not data.get("waitinglistsms_pingram_api_key"):
                self.add_error(
                    "waitinglistsms_pingram_api_key",
                    _("Please enter your Pingram API key."),
                )
            if not data.get("waitinglistsms_pingram_type"):
                self.add_error(
                    "waitinglistsms_pingram_type",
                    _("Please enter your Pingram notification type."),
                )
        elif provider == "twilio":
            if not data.get("waitinglistsms_from"):
                self.add_error(
                    "waitinglistsms_from",
                    _("Please enter a Twilio sender."),
                )
            if not data.get("waitinglistsms_twilio_account_sid"):
                self.add_error(
                    "waitinglistsms_twilio_account_sid",
                    _("Please enter your Twilio Account SID."),
                )
            if not data.get("waitinglistsms_twilio_auth_token"):
                self.add_error(
                    "waitinglistsms_twilio_auth_token",
                    _("Please enter your Twilio Auth Token."),
                )
        elif provider == "webhook" and not data.get("waitinglistsms_webhook_url"):
            self.add_error(
                "waitinglistsms_webhook_url",
                _("Please enter the gateway URL."),
            )

        template = data.get("waitinglistsms_message") or str(DEFAULT_MESSAGE)
        try:
            format_message_template(
                template,
                event="Example event",
                item="Example ticket",
                variation="",
                voucher_code="ABC123",
                voucher_valid_until="2026-12-31 23:59",
                url="https://example.org/",
            )
        except (KeyError, ValueError) as exc:
            self.add_error(
                "waitinglistsms_message",
                _("The message template contains an invalid placeholder: %(error)s")
                % {"error": exc},
            )

        return data
