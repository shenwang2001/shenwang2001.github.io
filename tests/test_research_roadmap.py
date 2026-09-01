import hashlib
import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ABOUT = ROOT / "_pages" / "about.md"
STYLES = ROOT / "assets" / "css" / "main.scss"
ROADMAP = ROOT / "images" / "research-roadmap.png"


class ResearchRoadmapTests(unittest.TestCase):
    def test_original_high_resolution_image_is_preserved(self):
        image = ROADMAP.read_bytes()
        self.assertEqual(
            hashlib.sha256(image).hexdigest(),
            "729b22d38360a7bea7f94b144c7921a1de7d116fcbba70ea7628500ee4afa290",
        )
        self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", image[16:24])
        self.assertEqual((width, height), (3840, 846))

    def test_roadmap_is_between_about_and_education_with_complete_stage_copy(self):
        about = ABOUT.read_text(encoding="utf-8")
        about_end = about.index("</div>", about.index('<div class="about-intro"'))
        roadmap_start = about.index('<figure class="research-roadmap"')
        education_start = about.index("# Education")
        self.assertLess(about_end, roadmap_start)
        self.assertLess(roadmap_start, education_start)
        self.assertIn('src="images/research-roadmap.png"', about)
        self.assertEqual(
            len(re.findall(r'<div class="research-roadmap__stage(?:\s|\")', about)),
            4,
        )

        expected_copy = [
            "(A) Reconstruction",
            "RP-NeRF",
            "MobiCom ’24",
            "SaRF",
            "UbiComp ’24",
            "(B) Scalability",
            "SIGN-RF",
            "INFOCOM ’26",
            "MoRE",
            "MobiCom ’26",
            "(C) Generalization",
            "GenRF",
            "SenSys ’27",
            "(D) Reasoning &amp; Action",
        ]
        for text in expected_copy:
            self.assertIn(text, about)

    def test_timeline_has_desktop_alignment_and_mobile_stacking(self):
        styles = STYLES.read_text(encoding="utf-8")
        self.assertRegex(
            styles,
            re.compile(
                r"\.research-roadmap__stages\s*\{[^}]*grid-template-columns:\s*repeat\(4,\s*1fr\)",
                re.DOTALL,
            ),
        )
        self.assertRegex(
            styles,
            re.compile(r"\.research-roadmap__axis\s*\{[^}]*position:\s*relative", re.DOTALL),
        )
        self.assertRegex(
            styles,
            re.compile(
                r"@media\s*\(max-width:\s*767px\)[\s\S]*?\.research-roadmap__stages\s*\{[^}]*grid-template-columns:\s*1fr",
                re.DOTALL,
            ),
        )


if __name__ == "__main__":
    unittest.main()
