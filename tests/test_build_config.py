from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BuildConfigurationTests(unittest.TestCase):
    def test_targets_ubuntu_resolute_and_ubuntu_kernel(self):
        build_script = (ROOT / "build.sh").read_text()
        self.assertIn("--distribution resolute", build_script)
        self.assertIn("--linux-packages linux-image-generic", build_script)
        self.assertIn("--binary-images iso-hybrid", build_script)

    def test_one_image_contains_both_desktops_and_gdm_default(self):
        packages = (
            ROOT
            / "live-build-config"
            / "config"
            / "package-lists"
            / "mustangia.list.chroot"
        ).read_text().splitlines()
        names = {line.strip() for line in packages if line.strip() and not line.startswith("#")}
        self.assertIn("ubuntu-desktop-minimal", names)
        self.assertIn("plasma-desktop", names)
        self.assertEqual(len(names), len([line for line in packages if line.strip() and not line.startswith("#")]))
        preseed = (
            ROOT / "live-build-config" / "config" / "preseed" / "desktop.cfg"
        ).read_text()
        self.assertIn("gdm3 shared/default-x-display-manager select gdm3", preseed)

    def test_core_language_and_debugger_packages_are_present(self):
        packages_file = (
            ROOT
            / "live-build-config"
            / "config"
            / "package-lists"
            / "mustangia.list.chroot"
        )
        names = {
            line.strip()
            for line in packages_file.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        }
        self.assertTrue(
            {
                "build-essential",
                "python3",
                "default-jdk-headless",
                "nodejs",
                "golang-go",
                "rustc",
                "git",
                "gdb",
                "lldb",
            }.issubset(names)
        )


if __name__ == "__main__":
    unittest.main()
