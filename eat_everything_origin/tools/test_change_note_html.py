import unittest
from change_note_html import exact_change_note


class ChangeNoteHtmlTest(unittest.TestCase):
    def test_rendered_paragraph_br_and_entities(self):
        self.assertTrue(exact_change_note('<p id="123">[v0.2.0] A &amp; B<br><br>C</p>', '[v0.2.0] A & B\r\n\r\nC'))

    def test_inline_formatting_preserves_text(self):
        self.assertTrue(exact_change_note('<p>[v0.2.0] <b>exact</b><br/>text</p>', '[v0.2.0] exact\ntext'))

    def test_literal_escaped_tag_stays_text(self):
        self.assertTrue(exact_change_note('<p>[v0.2.0] &lt;br&gt;</p>', '[v0.2.0] <br>'))

    def test_wrong_version(self):
        self.assertFalse(exact_change_note('<p>[v0.1.0] exact</p>', '[v0.2.0] exact'))

    def test_missing_word(self):
        self.assertFalse(exact_change_note('<p>[v0.2.0] disclosure</p>', '[v0.2.0] complete disclosure'))

    def test_internal_whitespace_not_removed(self):
        self.assertFalse(exact_change_note('<p>[v0.2.0] ab</p>', '[v0.2.0] a b'))

    def test_punctuation_not_removed(self):
        self.assertFalse(exact_change_note('<p>[v0.2.0] exact.</p>', '[v0.2.0] exact'))

    def test_unrelated_page_content_not_accepted(self):
        self.assertFalse(exact_change_note('<script>[v0.2.0] exact</script>', '[v0.2.0] exact'))

    def test_duplicate_matching_paragraphs_rejected(self):
        self.assertFalse(exact_change_note('<p>[v0.2.0] exact</p><p>[v0.2.0] exact</p>', '[v0.2.0] exact'))

    def test_empty_note_rejected(self):
        self.assertFalse(exact_change_note('<p></p>', ''))


if __name__ == '__main__':
    unittest.main()
