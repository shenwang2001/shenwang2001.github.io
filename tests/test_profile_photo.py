import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfilePhotoConfigurationTests(unittest.TestCase):
    def test_homepage_uses_the_latest_requested_photo(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertIn('avatar           : "images/profile-2026.png"', config)

        photo = ROOT / "images" / "profile-2026.png"
        self.assertEqual(photo.stat().st_size, 312_332)
        self.assertEqual(
            hashlib.sha256(photo.read_bytes()).hexdigest(),
            "f0594d53ea0fbb48d4823a9144b4ed009544820fe0eaa98d4f9c2e7260ce432c",
        )


if __name__ == "__main__":
    unittest.main()
