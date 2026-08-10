import os
import re
import shutil
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "tmp" / "test-site"


class HomepageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.headings = []
        self.summaries = []
        self.recent_news_items = 0
        self._text_capture = []
        self._capture_tag = None
        self._active_link = None
        self._in_recent_news = False
        self._recent_news_depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.tags.append((tag, attributes))
        if tag == "a":
            self._active_link = {"attrs": attributes, "text": ""}
            self.links.append(self._active_link)
        if tag in {"h1", "h2", "h3", "summary"}:
            self._capture_tag = tag
            self._text_capture = []
        if tag == "ul" and "news-list--recent" in attributes.get("class", "").split():
            self._in_recent_news = True
            self._recent_news_depth = 1
        elif self._in_recent_news:
            self._recent_news_depth += 1
            if tag == "li" and self._recent_news_depth == 2:
                self.recent_news_items += 1

    def handle_endtag(self, tag):
        if tag == "a":
            self._active_link = None
        if self._capture_tag == tag:
            text = " ".join("".join(self._text_capture).split())
            if tag in {"h1", "h2", "h3"}:
                self.headings.append((tag, text))
            else:
                self.summaries.append(text)
            self._capture_tag = None
            self._text_capture = []
        if self._in_recent_news:
            self._recent_news_depth -= 1
            if self._recent_news_depth == 0:
                self._in_recent_news = False

    def handle_data(self, data):
        if self._capture_tag:
            self._text_capture.append(data)
        if self._active_link is not None:
            self._active_link["text"] += data


class HomepageAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SITE.exists():
            shutil.rmtree(SITE)
        SITE.parent.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["JEKYLL_ENV"] = "production"
        env["LANG"] = "en_US.UTF-8"
        env["LC_ALL"] = "en_US.UTF-8"
        command = ["bundle", "exec", "jekyll", "build", "--destination", str(SITE), "--quiet"]
        if sys.platform == "darwin":
            command = ["arch", "-arm64", *command]
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise AssertionError(
                "Jekyll build failed.\nSTDOUT:\n"
                + result.stdout
                + "\nSTDERR:\n"
                + result.stderr
            )
        cls.html = (SITE / "index.html").read_text(encoding="utf-8")
        cls.css = (SITE / "assets" / "css" / "main.css").read_text(encoding="utf-8")
        cls.parser = HomepageParser()
        cls.parser.feed(cls.html)

    def test_navigation_has_requested_same_tab_sections(self):
        expected = {
            "About": "/#about-me",
            "News": "/#news",
            "Publications": "/#publications",
            "Experience": "/#experience",
        }
        links_by_text = {
            " ".join(link["text"].split()): link["attrs"] for link in self.parser.links
        }
        for label, href in expected.items():
            self.assertIn(label, links_by_text)
            self.assertEqual(links_by_text[label].get("href"), href)
            self.assertNotEqual(links_by_text[label].get("target"), "_blank")
        self.assertFalse(
            any(tag == "base" and attrs.get("target") == "_blank" for tag, attrs in self.parser.tags),
            "Internal links must not inherit a global blank target",
        )

    def test_news_keeps_the_original_update_wording(self):
        self.assertNotIn("More News", self.parser.summaries)
        self.assertNotIn('class="news-list news-list--recent"', self.html)
        self.assertIn("One paper has been accepted at ACM MobiCom 2026", self.html)
        self.assertIn("One paper has been accepted at IEEE TMC", self.html)
        for paper in ["SIGN-RF", "MoRE", "GaRF", "RP-NeRF"]:
            self.assertIn(paper, self.html)

    def test_sidebar_does_not_render_the_seo_description(self):
        self.assertNotIn(
            '<li><div style="white-space: normal; margin-bottom: 1em;">Shen Wang is a Ph.D. candidate',
            self.html,
        )

    def test_about_intro_is_slightly_larger_than_the_default_body_text(self):
        self.assertIn('<div class="about-intro">', self.html)
        self.assertRegex(
            self.css,
            re.compile(
                r"\.page__content\s+\.about-intro\s*\{[^}]*font-size:\s*1\.08em",
                re.DOTALL,
            ),
        )

    def test_navigation_uses_bold_active_state_without_orange_focus_outline(self):
        self.assertIn("is-active", self.html)
        navigation_scss = (ROOT / "_sass" / "_navigation.scss").read_text(encoding="utf-8")
        self.assertIn("&:focus", navigation_scss)
        self.assertIn("&.is-active", navigation_scss)
        self.assertIn("font-weight: 700", navigation_scss)
        self.assertIn("outline: 0", navigation_scss)
        self.assertNotIn("&:first-child {\n        font-weight: bold;", navigation_scss)

    def test_document_outline_keeps_original_section_h1s_and_author_h3(self):
        h1s = [text for tag, text in self.parser.headings if tag == "h1"]
        h3s = [text for tag, text in self.parser.headings if tag == "h3"]
        self.assertEqual(h3s, ["Shen Wang(王申)"])
        for section in [
            "About me",
            "🔥 News",
            "📝 Publications",
            "Honors and Awards",
            "Education",
            "Professional Services",
            "Teaching Experience",
        ]:
            self.assertIn(section, h1s)

    def test_stale_tracking_integrations_are_not_rendered(self):
        script_sources = [attrs.get("src", "") for tag, attrs in self.parser.tags if tag == "script"]
        self.assertFalse(any("mapmyvisitors" in src for src in script_sources))
        self.assertFalse(any("googletagmanager" in src for src in script_sources))
        self.assertNotIn("gs_data.json", self.html)

    def test_search_and_social_metadata_are_complete(self):
        metas = [attrs for tag, attrs in self.parser.tags if tag == "meta"]
        description = next((m.get("content", "") for m in metas if m.get("name") == "description"), "")
        og_description = next(
            (m.get("content", "") for m in metas if m.get("property") == "og:description"), ""
        )
        og_image = next((m.get("content", "") for m in metas if m.get("property") == "og:image"), "")
        og_type = next((m.get("content", "") for m in metas if m.get("property") == "og:type"), "")
        self.assertGreater(len(description), 40)
        self.assertEqual(og_description, description)
        self.assertTrue(og_image.endswith("/images/WechatIMG1956.webp"))
        self.assertEqual(og_type, "profile")

    def test_avatar_uses_a_compact_webp_asset(self):
        avatar = SITE / "images" / "WechatIMG1956.webp"
        self.assertTrue(avatar.exists())
        self.assertLess(avatar.stat().st_size, 150 * 1024)
        profile_images = [
            attrs
            for tag, attrs in self.parser.tags
            if tag == "img" and "author__avatar" in attrs.get("class", "").split()
        ]
        self.assertEqual(len(profile_images), 1)
        self.assertEqual(profile_images[0].get("src"), "images/WechatIMG1956.webp")


if __name__ == "__main__":
    unittest.main()
