import pytest

pytest.importorskip("pretix")

from django.utils.timezone import now  # noqa: E402
from django_scopes import scopes_disabled  # noqa: E402
from pretix.base.models import (  # noqa: E402
    Event,
    Item,
    Organizer,
    Team,
    User,
    Voucher,
    WaitingListEntry,
)

from pretix_waitinglistsms.tasks import send_waitinglist_sms  # noqa: E402


class DummyResponse:
    status_code = 200

    def raise_for_status(self):
        pass

    def json(self):
        return {"trackingId": "dummy"}


@pytest.fixture
def event():
    with scopes_disabled():
        organizer = Organizer.objects.create(name="Dummy", slug="dummy")
        event = Event.objects.create(
            organizer=organizer,
            name="Dummy event",
            slug="dummy",
            date_from=now(),
            plugins="pretix_waitinglistsms",
            live=True,
        )
        event.settings.waitinglistsms_enabled = True
        event.settings.waitinglistsms_provider = "webhook"
        event.settings.waitinglistsms_webhook_url = "https://gateway.example.com/sms"
        return event


@pytest.fixture
def entry(event):
    with scopes_disabled():
        item = Item.objects.create(event=event, name="Ticket", default_price=10)
        voucher = Voucher.objects.create(event=event, item=item, code="ABC123")
        return WaitingListEntry.objects.create(
            event=event,
            item=item,
            email="attendee@example.org",
            phone="+32470123456",
            voucher=voucher,
            locale="en",
        )


@pytest.fixture
def gateway(monkeypatch):
    calls = []

    def fake_post(*args, **kwargs):
        calls.append((args, kwargs))
        return DummyResponse()

    monkeypatch.setattr("pretix_waitinglistsms.tasks.requests.post", fake_post)
    return calls


@pytest.mark.django_db
def test_task_sends_sms_and_logs(event, entry, gateway):
    assert send_waitinglist_sms(entry.pk) is True
    assert len(gateway) == 1
    payload = gateway[0][1]["json"]
    assert payload["to"] == "+32470123456"
    assert payload["voucher_code"] == "ABC123"
    with scopes_disabled():
        assert entry.all_logentries().filter(
            action_type="pretix.plugins.waitinglistsms.sent"
        ).exists()


@pytest.mark.django_db
def test_task_does_not_send_twice(event, entry, gateway):
    assert send_waitinglist_sms(entry.pk) is True
    assert send_waitinglist_sms(entry.pk) is False
    assert len(gateway) == 1


@pytest.mark.django_db
def test_task_respects_disabled_setting(event, entry, gateway):
    event.settings.waitinglistsms_enabled = False
    assert send_waitinglist_sms(entry.pk) is False
    assert len(gateway) == 0


@pytest.mark.django_db
def test_task_respects_inactive_plugin(event, entry, gateway):
    event.plugins = ""
    event.save()
    assert send_waitinglist_sms(entry.pk) is False
    assert len(gateway) == 0


@pytest.mark.django_db
def test_task_skips_entry_without_phone(event, entry, gateway):
    with scopes_disabled():
        entry.phone = None
        entry.save()
    assert send_waitinglist_sms(entry.pk) is False
    assert len(gateway) == 0


@pytest.mark.django_db
def test_settings_view_requires_login(client, event):
    response = client.get("/control/event/dummy/dummy/waiting-list-sms/settings")
    assert response.status_code in (301, 302)


@pytest.mark.django_db
def test_settings_view_accessible_with_permission(client, event):
    user = User.objects.create_user("admin@example.org", "dummy-password")
    team = Team.objects.create(
        organizer=event.organizer,
        all_events=True,
        can_change_event_settings=True,
    )
    team.members.add(user)
    client.login(email="admin@example.org", password="dummy-password")
    response = client.get("/control/event/dummy/dummy/waiting-list-sms/settings")
    assert response.status_code == 200


@pytest.mark.django_db
def test_settings_view_denied_without_permission(client, event):
    user = User.objects.create_user("viewer@example.org", "dummy-password")
    team = Team.objects.create(
        organizer=event.organizer,
        all_events=True,
        can_change_event_settings=False,
        can_view_orders=True,
    )
    team.members.add(user)
    client.login(email="viewer@example.org", password="dummy-password")
    response = client.get("/control/event/dummy/dummy/waiting-list-sms/settings")
    assert response.status_code in (302, 403)
