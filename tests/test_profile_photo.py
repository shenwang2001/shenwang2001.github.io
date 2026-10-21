import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfilePhotoConfigurationTests(unittest.TestCase):
    def test_homepage_uses_the_original_full_resolution_seaside_photo(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertIn('avatar           : "images/WechatIMG1956.jpg"', config)

        photo = ROOT / "images" / "WechatIMG1956.jpg"
        self.assertEqual(photo.stat().st_size, 973_095)
        self.assertEqual(
            hashlib.sha256(photo.read_bytes()).hexdigest(),
            "4e61408a38f9818114f4400fa6086c9d83ce910fa6eb7e7e4f10a502e9f82bd4",
        )


if __name__ == "__main__":
    unittest.main()
