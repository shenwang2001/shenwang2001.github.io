import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfessionalServicesTests(unittest.TestCase):
    def test_services_are_grouped_by_year(self):
        about = (ROOT / "_pages" / "about.md").read_text(encoding="utf-8")
        services = about.split("# Professional Services\n", 1)[1].split(
            "# Teaching Experience", 1
        )[0]

        expected = """- **TPC Member**
  - *2026:* ACM MobiCom (AE), IEEE IWCMC, IEEE ISPA
  - *2025:* IEEE ISPA, IEEE SpaCCS

- **Reviewer**
  - *2027:* ACM KDD, ACM CHI
  - *2026:* IEEE MASS, ACM KDD, ACM IMWUT
  - IEEE Transactions on Mobile Computing (TMC)

"""
        self.assertEqual(services, expected)


if __name__ == "__main__":
    unittest.main()
