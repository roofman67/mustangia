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
        self.assertIn("xserver-xorg", names)
        self.assertIn("gnome-software", names)
        self.assertIn("plasma-discover", names)
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

    def test_welcome_gui_describes_system_components_and_apps(self):
        welcome = (ROOT / "welcome" / "mustangia_welcome.py").read_text()
        for component in ("GRUB", "Syslinux", "systemd", "PipeWire", "GNOME", "KDE Plasma"):
            with self.subTest(component=component):
                self.assertIn(component, welcome)
        for app in ("LibreOffice", "Anki", "VLC", "Neovim", "Brave", "Zotero"):
            with self.subTest(app=app):
                self.assertIn(app, welcome)


if __name__ == "__main__":
    unittest.main()
