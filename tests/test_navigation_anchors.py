import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VisibleAnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, _tag, attrs):
        element_id = dict(attrs).get("id")
        if element_id:
            self.ids.add(element_id)


class NavigationAnchorTests(unittest.TestCase):
    def test_publications_navigation_target_is_visible_to_the_browser(self):
        parser = VisibleAnchorParser()
        parser.feed((ROOT / "_pages" / "about.md").read_text(encoding="utf-8"))

        self.assertIn("publications", parser.ids)


if __name__ == "__main__":
    unittest.main()
