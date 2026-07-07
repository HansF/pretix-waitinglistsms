import logging

import requests
from django.utils.formats import date_format
from django.utils.timezone import localtime
from django.utils.translation import gettext as _
from django_scopes import scopes_disabled
from pretix.base.i18n import language
from pretix.base.models import WaitingListEntry
from pretix.celery_app import app
from pretix.multidomain.urlreverse import build_absolute_uri

from .message import DEFAULT_MESSAGE, format_message_template

logger = logging.getLogger(__name__)


def build_message(entry):
    voucher = entry.voucher
    event = entry.event
    with language(entry.locale, event.settings.region):
        url = build_absolute_uri(event, "presale:event.index")
        valid_until = (
            date_format(localtime(voucher.valid_until), "SHORT_DATETIME_FORMAT")
            if voucher.valid_until
            else ""
        )
        template = str(event.settings.waitinglistsms_message or _(DEFAULT_MESSAGE))
        return format_message_template(
            template,
            event=event.name,
            item=entry.item.name,
            variation=entry.variation.value if entry.variation else "",
            voucher_code=voucher.code,
            voucher_valid_until=valid_until,
            url=url,
        )


def send_twilio(entry, body):
    event = entry.event
    sid = event.settings.waitinglistsms_twilio_account_sid
    response = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
        data={
            "To": str(entry.phone),
            "From": event.settings.waitinglistsms_from,
            "Body": body,
        },
        auth=(sid, event.settings.waitinglistsms_twilio_auth_token),
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("sid")


def send_pingram(entry, body):
    event = entry.event
    sms = {"message": body}
    if event.settings.waitinglistsms_from:
        sms["from"] = event.settings.waitinglistsms_from
    response = requests.post(
        (event.settings.waitinglistsms_pingram_base_url or "https://api.pingram.io").rstrip("/")
        + "/sender",
        json={
            "type": event.settings.waitinglistsms_pingram_type or "waiting_list_sms",
            "to": {
                "id": f"pretix-waitinglist-{entry.pk}",
                "number": str(entry.phone),
            },
            "sms": sms,
        },
        headers={
            "Authorization": f"Bearer {event.settings.waitinglistsms_pingram_api_key}",
            "Content-Type": "application/json",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("trackingId") or data.get("id")


def send_webhook(entry, body):
    event = entry.event
    response = requests.post(
        event.settings.waitinglistsms_webhook_url,
        json={
            "to": str(entry.phone),
            "from": event.settings.waitinglistsms_from,
            "body": body,
            "event": event.slug,
            "item": entry.item_id,
            "variation": entry.variation_id,
            "voucher_code": entry.voucher.code,
        },
        timeout=10,
    )
    response.raise_for_status()
    return str(response.status_code)


@app.task(bind=True, max_retries=4, throws=(WaitingListEntry.DoesNotExist,))
@scopes_disabled()
def send_waitinglist_sms(self, entry_id):
    entry = WaitingListEntry.objects.select_related(
        "event",
        "event__organizer",
        "item",
        "variation",
        "voucher",
    ).get(pk=entry_id)
    if (
        not entry.voucher_id
        or not entry.phone
        or "pretix_waitinglistsms" not in entry.event.get_plugins()
        or not entry.event.settings.waitinglistsms_enabled
    ):
        return False
    if entry.all_logentries().filter(
        action_type="pretix.plugins.waitinglistsms.sent"
    ).exists():
        return False

    body = build_message(entry)
    try:
        provider = entry.event.settings.waitinglistsms_provider or "pingram"
        if provider == "webhook":
            provider_id = send_webhook(entry, body)
        elif provider == "twilio":
            provider_id = send_twilio(entry, body)
        else:
            provider_id = send_pingram(entry, body)
    except requests.RequestException as exc:
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        logger.exception("Could not send waiting list SMS for entry %s", entry.pk)
        entry.log_action(
            "pretix.plugins.waitinglistsms.failed",
            {"error": str(exc)[:500]},
        )
        raise
    except Exception as exc:
        logger.exception("Could not send waiting list SMS for entry %s", entry.pk)
        entry.log_action(
            "pretix.plugins.waitinglistsms.failed",
            {"error": str(exc)[:500]},
        )
        raise

    entry.log_action(
        "pretix.plugins.waitinglistsms.sent",
        {"provider": provider, "provider_id": provider_id},
    )
    return True
