"""The packaged skill works after being copied away from this repository."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstalledSkillTests(unittest.TestCase):
    def test_report_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "target-repo" / ".agents" / "skills" / "imozuru"
            shutil.copytree(ROOT / "skills" / "imozuru", skill)
            self.assertTrue((skill / "SKILL.md").is_file())
            self.assertTrue((skill / "references" / "theory.md").is_file())

            topic = root / "research" / "demo"
            shutil.copytree(ROOT / "examples" / "demo", topic,
                            ignore=shutil.ignore_patterns("report.html"))
            elsewhere = root / "elsewhere"
            elsewhere.mkdir()
            command = [sys.executable, "-X", "utf8", str(skill / "scripts" / "report.py"),
                       str(topic)]

            checked = subprocess.run(command + ["--check"], cwd=elsewhere,
                                     capture_output=True, encoding="utf-8", check=False)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("照合 OK", checked.stdout)
            self.assertFalse((topic / "report.html").exists())

            generated = subprocess.run(command, cwd=elsewhere,
                                       capture_output=True, encoding="utf-8", check=False)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertIn("照合 OK", generated.stdout)
            self.assertIn("<!doctype html>", (topic / "report.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
