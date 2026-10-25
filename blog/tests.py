from django.test import TestCase
from django.test import SimpleTestCase

from .richtext import sanitize_rich_text

# Create your tests here.


class RichTextSanitizationTests(SimpleTestCase):
    def test_preserves_formatting_and_removes_unsafe_markup(self):
        cleaned = sanitize_rich_text(
            "<p><strong>Texto</strong><script>alert(1)</script>"
            "<img src=x onerror=alert(1)></p>"
        )

        self.assertIn("<strong>Texto</strong>", cleaned)
        self.assertNotIn("script", cleaned)
        self.assertNotIn("onerror", cleaned)
        self.assertNotIn("alert(1)", cleaned)
