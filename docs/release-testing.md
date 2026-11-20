# Mustangia release test checklist

The repository currently provides a build and checksum/ISO-catalog validation path. A successful build or ISO catalog check is **not** evidence that every desktop, device, or firmware combination has been tested. Record the image checksum, host build environment, firmware mode, and test result for each release candidate.

## Automated checks

- Run `python3 -m unittest discover -s tests -v`.
- Run `bash -n build.sh scripts/validate-iso.sh`.
- Confirm all required and optional package names are available in the Ubuntu 26.04 repositories before publishing.
- Build on Ubuntu 26.04 amd64 with the documented packages.
- Run `bash scripts/validate-iso.sh` and retain the image and `.sha256` file together.

The CI workflow runs the first three checks, verifies the checksum and El Torito catalog, and uploads the ISO as a build artifact. It does not claim a successful GUI session or physical-hardware test.

## Manual release matrix

Before calling an image release-ready, test all of the following and record results:

| Area | Required check |
| --- | --- |
| Firmware | Boot the same ISO in BIOS and UEFI VMs; confirm the live desktop appears. |
| GNOME | Sign in to the default GNOME session; check welcome app, networking, display, audio, and suspend/resume. |
| KDE Plasma | Log out, select Plasma from GDM's session menu, sign in, and check the same basics. |
| Networking | Test wired networking and at least one Wi-Fi adapter; install each optional bundle while online. |
| Graphics/audio | Test at least one Intel/AMD system and representative audio devices; document NVIDIA/proprietary-driver limitations. |
| Development | Run the compiler, interpreter, debugger, Git, and QEMU version commands listed in the welcome app. Build each lab template. |
| Application catalogs | Open GNOME Software and KDE Discover; verify Ubuntu repository packages can be browsed and installed. |
| USB | Write the ISO to a spare USB device, boot it on physical hardware, and verify checksum before distribution. |
| Persistence | Not implemented: confirm that users understand live changes may be lost; do not advertise persistence. |
| Upgrade/install | Not implemented: this ISO has no installer or supported upgrade path. Do not test or claim in-place upgrades. |
| Compatibility | Record exact hardware and firmware; never claim universal Windows/macOS or hardware compatibility. |

Do not publish an ISO as tested until the manual rows have actual results. Keep signing, secure-boot enrollment, persistence, and installation as separate future work.
