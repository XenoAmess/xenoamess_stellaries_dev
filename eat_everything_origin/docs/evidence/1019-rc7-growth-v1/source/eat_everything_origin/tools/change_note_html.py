"""Compare the exact Change Note against Steam's rendered paragraph text."""
from html.parser import HTMLParser


class _Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current = None
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.current = []
        elif tag == "br" and self.current is not None:
            self.current.append("\n")

    def handle_endtag(self, tag):
        if tag == "p" and self.current is not None:
            self.paragraphs.append("".join(self.current))
            self.current = None

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)


def exact_change_note(page, expected):
    parser = _Paragraphs()
    parser.feed(page)
    normalize = lambda text: text.replace("\r\n", "\n").replace("\r", "\n").strip()
    target = normalize(expected)
    return bool(target) and sum(normalize(text) == target for text in parser.paragraphs) == 1
