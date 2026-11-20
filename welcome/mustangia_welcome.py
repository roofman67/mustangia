#!/usr/bin/env python3
import subprocess
import platform

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class MustangiaWelcome(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to Mustangia")
        self.set_default_size(760, 560)
        self.set_border_width(18)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(root)

        heading = Gtk.Label()
        heading.set_markup("<big><b>Mustangia Student Linux</b></big>")
        heading.set_xalign(0)
        root.pack_start(heading, False, False, 0)

        notebook = Gtk.Notebook()
        root.pack_start(notebook, True, True, 0)
        notebook.append_page(
            self.make_text_page(
                "A computer-science learning environment built on Ubuntu 26.04.1 LTS. "
                "Start a lab, explore the tools, or open the help pages below."
            ),
            Gtk.Label(label="Welcome"),
        )
        notebook.append_page(
            self.make_components_page(), Gtk.Label(label="System components")
        )
        notebook.append_page(self.make_desktop_page(), Gtk.Label(label="Desktops"))
        notebook.append_page(self.make_apps_page(), Gtk.Label(label="Applications"))
        notebook.append_page(self.make_labs_page(), Gtk.Label(label="Lab starters"))
        notebook.append_page(self.make_bundles_page(), Gtk.Label(label="Optional bundles"))
        notebook.append_page(self.make_help_page(), Gtk.Label(label="Help"))

    @staticmethod
    def make_text_page(text):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        page.set_border_width(18)
        label = Gtk.Label(label=text)
        label.set_line_wrap(True)
        label.set_xalign(0)
        page.pack_start(label, False, False, 0)
        return page

    @classmethod
    def make_desktop_page(cls):
        page = cls.make_text_page(
            "This ISO includes GNOME and KDE Plasma. GNOME is the default session. "
            "To switch, log out to the GDM sign-in screen, choose the session/gear "
            "menu, select Plasma or Ubuntu (GNOME), then sign in again. The available "
            "session names can vary slightly with Ubuntu package updates."
        )
        return page

    @classmethod
    def make_components_page(cls):
        return cls.make_text_page(
            "Bootloader: GRUB on UEFI, Syslinux on legacy BIOS\n"
            f"Linux kernel: Ubuntu linux-generic ({platform.release()})\n"
            "Init system: systemd\n"
            "Background services: NetworkManager for networking, PipeWire and "
            "WirePlumber for audio, CUPS for printing\n"
            "Graphics: Wayland desktop sessions with X.Org compatibility\n"
            "Desktop environments: GNOME (default) and KDE Plasma\n"
            "Application catalogs: GNOME Software and KDE Discover"
        )

    @classmethod
    def make_apps_page(cls):
        return cls.make_text_page(
            "Included development tools\n"
            "GCC/G++, Clang, Python 3, Java, Node.js, Go, Rust, Git, GitHub CLI, "
            "GDB, LLDB, CMake, SQLite, and QEMU.\n\n"
            "Available as optional Ubuntu packages\n"
            "Study: LibreOffice, Anki, Foliate, KBruch, Kig, and Kalzium.\n"
            "Media: VLC, MPV, OBS Studio, MComix, Lollypop, Clementine, and Conky.\n"
            "Terminals/editors: Konsole is included; Neovim, Alacritty, and Kitty "
            "are optional.\n\n"
            "Firefox is supplied by the Ubuntu desktop. Brave, VS Code, Zotero, "
            "Obsidian, and ONLYOFFICE use vendor distribution channels and are "
            "not silently added as third-party repositories. Install them only "
            "from their official publishers if needed."
        )

    @classmethod
    def make_labs_page(cls):
        page = cls.make_text_page(
            "Create a starter project in ~/MustangiaLabs. The command refuses to "
            "overwrite an existing destination."
        )
        for kind in ("python", "web", "systems", "data-science"):
            button = Gtk.Button(label=f"Create {kind} lab")
            button.connect("clicked", cls.on_create_lab, kind)
            page.pack_start(button, False, False, 0)
        return page

    @classmethod
    def make_bundles_page(cls):
        page = cls.make_text_page(
            "Optional bundles install from Ubuntu repositories and require an "
            "internet connection. Select a command to copy it, then run it in a "
            "terminal and review the packages before confirming."
        )
        bundle_labels = {
            "web": "Web development",
            "data-science": "Data science",
            "systems": "Systems",
            "study": "Study and office",
            "media": "Media and local manga reading",
            "terminals": "Extra terminals and editor",
        }
        for slug, label in bundle_labels.items():
            button = Gtk.Button(label=f"Copy install command for {label}")
            button.connect("clicked", cls.on_copy_bundle, slug)
            page.pack_start(button, False, False, 0)
        return page

    @classmethod
    def make_help_page(cls):
        page = cls.make_text_page(
            "Quick help\n"
            "• Python: python3 --version\n"
            "• C/C++: gcc --version and g++ --version\n"
            "• Git: git --help\n"
            "• List lab types: mustangia-lab list\n"
            "• List optional packages: mustangia-bundle list\n"
            "• Install a bundle: mustangia-bundle install <name>\n\n"
            "This is a live system. Save coursework to another drive or network location; "
            "changes may be lost when you shut down."
        )
        link = Gtk.LinkButton.new_with_label(
            "https://ubuntu.com/tutorials", "Ubuntu tutorials"
        )
        link.set_halign(Gtk.Align.START)
        page.pack_start(link, False, False, 0)
        return page

    @staticmethod
    def show_message(parent, title, message, message_type=Gtk.MessageType.INFO):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            flags=Gtk.DialogFlags.MODAL,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    @classmethod
    def on_create_lab(cls, _button, kind):
        command = ["mustangia-lab", "create", kind]
        try:
            result = subprocess.run(
                command, check=True, text=True, capture_output=True
            )
        except subprocess.CalledProcessError as error:
            cls.show_message(
                _button.get_toplevel(),
                "Could not create lab",
                error.stderr.strip() or str(error),
                Gtk.MessageType.ERROR,
            )
            return
        except OSError as error:
            cls.show_message(
                _button.get_toplevel(),
                "Could not create lab",
                str(error),
                Gtk.MessageType.ERROR,
            )
            return
        cls.show_message(
            _button.get_toplevel(),
            "Lab created",
            result.stdout.strip(),
        )

    @classmethod
    def on_copy_bundle(cls, _button, slug):
        command = f"mustangia-bundle install {slug}"
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(command, -1)
        clipboard.store()
        cls.show_message(
            _button.get_toplevel(),
            "Command copied",
            f"{command}\n\nOpen a terminal to review and run it.",
        )


def main():
    window = MustangiaWelcome()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
