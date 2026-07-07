from string import Formatter


def gettext_noop(message):
    # Marks DEFAULT_MESSAGE for extraction by makemessages (which matches the
    # call by name) without importing Django, so this module stays usable
    # without configured Django settings. Translation happens in tasks.py.
    return message


DEFAULT_MESSAGE = gettext_noop(
    "Good news! A spot opened for {event}. Use voucher {voucher_code} to book: {url}"
)
ALLOWED_PLACEHOLDERS = {
    "event",
    "item",
    "variation",
    "voucher_code",
    "voucher_valid_until",
    "url",
}


def format_message_template(template, **context):
    for _, field_name, _, _ in Formatter().parse(template):
        if field_name and field_name not in ALLOWED_PLACEHOLDERS:
            raise KeyError(field_name)
    return template.format(**context)
