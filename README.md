# Mustangia

Mustangia is a computer-science student live Linux image built from Ubuntu 26.04.1 LTS packages. The first release is one amd64 ISO containing both GNOME and KDE Plasma. It uses Ubuntu's supported `linux-generic` kernel package stream; it does not ship a separately maintained upstream kernel. Mustangia is an Ubuntu remix, not a new kernel or independent distribution infrastructure.

## What is in the image

- **GNOME and KDE Plasma** are installed together. GDM is the single display manager and GNOME is the default session. At the GDM sign-in screen, use the session/gear menu to select **Plasma (X11 or Wayland, if offered)**. Log out to return to the sign-in screen and change sessions.
- Core tools cover C/C++, Python, Java, JavaScript/Node.js, Go, Rust, Git, debuggers, build systems, SQLite, and QEMU.
- A GTK welcome app provides desktop-selection guidance, student help, lab-template launchers, and optional-bundle instructions.
- `mustangia-lab` creates starter projects for Python, web, systems, and data-science coursework.
- `mustangia-bundle install web|data-science|systems` installs optional packages from Ubuntu repositories when the machine is online.

## Build the ISO

Build on an Ubuntu 26.04 amd64 host with internet access and at least 30 GB free disk space. The build uses Ubuntu repositories for the `resolute` suite and requires root for `live-build`/`debootstrap`.

```sh
sudo apt update
sudo apt install -y live-build debootstrap xorriso squashfs-tools \
  syslinux-common isolinux grub-pc-bin grub-efi-amd64-bin mtools
sudo bash ./build.sh
```

The output is `dist/mustangia-26.04.1-amd64.iso`; a SHA-256 file is written alongside it. Build intermediates are kept in `.build/live-build`. Set `MUSTANGIA_BUILD_DIR` or `MUSTANGIA_OUTPUT_DIR` to use different directories.

To validate the checksum and inspect the ISO boot catalog:

```sh
bash ./scripts/validate-iso.sh
```

To boot in QEMU:

```sh
qemu-system-x86_64 -m 6144 -cdrom dist/mustangia-26.04.1-amd64.iso -boot d
```

The live image has no installer, persistence, or upgrade service yet. Do not treat it as an installation or recovery image. For USB testing, use a trusted imaging tool such as GNOME Disks or Rufus in DD mode; writing an image erases the selected drive, so verify the target carefully.

## Hardware and compatibility

This image targets 64-bit x86 PCs and is intended to boot on BIOS and UEFI systems. Secure Boot signing is not configured or verified; disable Secure Boot if firmware rejects the image. Test in a VM before trying physical hardware. Wi-Fi, graphics, audio, suspend, and other device support depend on Ubuntu's included kernel, firmware, and drivers; no universal hardware compatibility is claimed.

The live image is not a Windows or macOS application and does not promise to eliminate issues on those platforms. It can be written to USB using tools available on Windows or macOS, but the live environment itself is Linux. Use at least 6 GB RAM for the combined desktops; 8 GB or more is recommended for development and virtual machines.

Package versions are resolved from Ubuntu's repositories at build time. The 26.04.1 label identifies the target Ubuntu point release, but rebuilds can include later package updates. Reproducible, signed release snapshots are future work.

## Development

Run the focused tests without root:

```sh
python3 -m unittest discover -s tests -v
bash -n build.sh scripts/validate-iso.sh
```

The release checklist and current test limitations are in [`docs/release-testing.md`](docs/release-testing.md). GitHub Actions runs the tests, builds the ISO, checks its checksum/boot catalog, and uploads the image artifact.

Mustangia is an independent community project and is not affiliated with or endorsed by Canonical. Ubuntu and its marks are the property of their respective owners.
