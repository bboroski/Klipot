import json
import unittest
from pathlib import Path

from klipot.platforms import detect_platform, normalize_architecture, validate_e2k_profile


PROFILE = Path(__file__).resolve().parents[1] / "platforms" / "e2k" / "target.json"


class E2KPlatformTests(unittest.TestCase):
    def test_architecture_aliases(self):
        for value in ("e2k", "E2K", "Elbrus", "mcst-elbrus"):
            self.assertEqual(normalize_architecture(value), "e2k")

    def test_detects_native_linux_contract(self):
        result = detect_platform(machine="e2k", pointer_bits=64, byteorder="little", system="Linux")
        self.assertTrue(result["native_e2k_linux"])
        self.assertEqual(result["elf_machine"], 175)

    def test_rejects_wrong_word_size(self):
        result = detect_platform(machine="e2k", pointer_bits=32, byteorder="little", system="Linux")
        self.assertFalse(result["native_e2k_linux"])

    def test_repository_profile_is_valid(self):
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(validate_e2k_profile(profile), ())

    def test_rejects_mislabelled_limine_profile(self):
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        profile["boot"]["generic_limine"] = True
        self.assertIn("E2K profile must not claim generic Limine boot support",
                      validate_e2k_profile(profile))


if __name__ == "__main__":
    unittest.main()
