import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

from labs.mustangia_bundle import BUNDLES, main as bundle_main
from labs.mustangia_lab import LAB_KINDS, create_lab


class LabCreationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.templates = self.root / "templates"
        (self.templates / "python").mkdir(parents=True)
        (self.templates / "python" / "main.py").write_text("print('hello')\n")

    def tearDown(self):
        self.temp.cleanup()

    def test_create_copies_template_without_modifying_source(self):
        destination = self.root / "coursework" / "python"
        result = create_lab("python", destination, self.templates)
        self.assertEqual(result, destination)
        self.assertEqual((destination / "main.py").read_text(), "print('hello')\n")
        self.assertTrue((self.templates / "python" / "main.py").exists())

    def test_refuses_to_overwrite_existing_destination(self):
        destination = self.root / "python"
        destination.mkdir()
        marker = destination / "keep.txt"
        marker.write_text("keep\n")
        with self.assertRaises(FileExistsError):
            create_lab("python", destination, self.templates)
        self.assertEqual(marker.read_text(), "keep\n")

    def test_known_lab_kinds_are_present(self):
        self.assertEqual(
            LAB_KINDS, ("python", "web", "systems", "data-science")
        )

    def test_python_templates_compile(self):
        project_templates = Path(__file__).resolve().parents[1] / "labs" / "templates"
        for template in project_templates.glob("**/*.py"):
            with self.subTest(template=template.relative_to(project_templates)):
                compile(template.read_text(), str(template), "exec")

    def test_optional_bundle_installs_only_the_selected_packages(self):
        with patch("labs.mustangia_bundle.is_root", return_value=True):
            with patch("labs.mustangia_bundle.subprocess.run") as run:
                self.assertEqual(bundle_main(["install", "web"]), 0)

        self.assertEqual(
            run.call_args_list,
            [
                call(["apt-get", "update"], check=True),
                call(
                    [
                        "apt-get",
                        "install",
                        "--no-install-recommends",
                        *BUNDLES["web"],
                    ],
                    check=True,
                ),
            ],
        )

    def test_non_root_bundle_install_reexecutes_through_sudo(self):
        with patch("labs.mustangia_bundle.is_root", return_value=False):
            with patch("labs.mustangia_bundle.subprocess.run") as run:
                self.assertEqual(bundle_main(["install", "systems"]), 0)

        command = run.call_args.args[0]
        self.assertEqual(command[0], "sudo")
        self.assertEqual(command[-2:], ["install", "systems"])
        self.assertTrue(run.call_args.kwargs["check"])

    def test_optional_bundle_names_are_explicit(self):
        self.assertEqual(
            tuple(BUNDLES), ("web", "data-science", "systems")
        )


if __name__ == "__main__":
    unittest.main()
