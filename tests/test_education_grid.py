import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EducationGridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.about = (ROOT / "_pages" / "about.md").read_text(encoding="utf-8")
        cls.styles = (ROOT / "assets" / "css" / "main.scss").read_text(encoding="utf-8")

    def test_education_uses_logo_details_grid_and_meta_rows(self):
        self.assertIn('<ul class="education-list">', self.about)
        self.assertEqual(self.about.count('class="education-logo"'), 2)
        self.assertEqual(self.about.count('class="education-details"'), 2)
        self.assertEqual(self.about.count('class="education-title"'), 2)
        self.assertEqual(self.about.count('class="education-meta"'), 2)
        self.assertNotIn('class="education-header"', self.about)
        self.assertNotIn('class="education-degree"', self.about)
        self.assertRegex(
            self.styles,
            re.compile(
                r"\.education-item\s*\{[^}]*display:\s*grid;[^}]*grid-template-columns:\s*48px\s+minmax\(0,\s*1fr\)[^}]*gap:\s*8px",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            self.styles,
            re.compile(
                r"\.education-logo\s*\{[^}]*width:\s*48px;[^}]*height:\s*48px",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            self.styles,
            re.compile(
                r"\.education-logo img\s*\{[^}]*width:\s*100%;[^}]*height:\s*100%;[^}]*object-fit:\s*contain",
                re.DOTALL,
            ),
        )

    def test_mobile_keeps_logo_and_text_on_the_same_row(self):
        self.assertRegex(
            self.styles,
            re.compile(
                r"@media\s*\(max-width:\s*767px\)[\s\S]*?\.education-item\s*\{[^}]*grid-template-columns:\s*48px\s+minmax\(0,\s*1fr\)[^}]*gap:\s*8px",
                re.DOTALL,
            ),
        )

    def test_research_roadmap_is_removed(self):
        self.assertNotIn('class="research-roadmap', self.about)
        self.assertNotIn('images/research-roadmap.png', self.about)
        self.assertNotIn('.research-roadmap', self.styles)


if __name__ == "__main__":
    unittest.main()
