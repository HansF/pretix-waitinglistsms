import unittest

from pretix_waitinglistsms.message import format_message_template


class MessageTemplateTests(unittest.TestCase):
    def test_format_message_template_accepts_known_placeholders(self):
        result = format_message_template(
            "{event}: {item} {variation} {voucher_code} {voucher_valid_until} {url}",
            event="Demo",
            item="Ticket",
            variation="VIP",
            voucher_code="ABC123",
            voucher_valid_until="2026-12-31 23:59",
            url="https://example.org/",
        )

        self.assertEqual(
            result,
            "Demo: Ticket VIP ABC123 2026-12-31 23:59 https://example.org/",
        )

    def test_format_message_template_rejects_unknown_placeholder(self):
        with self.assertRaises(KeyError):
            format_message_template(
                "{event} {phone}",
                event="Demo",
                item="Ticket",
                variation="",
                voucher_code="ABC123",
                voucher_valid_until="",
                url="https://example.org/",
            )


if __name__ == "__main__":
    unittest.main()
