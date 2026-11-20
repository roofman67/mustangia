#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${MUSTANGIA_BUILD_DIR:-"${ROOT_DIR}/.build/live-build"}"
OUTPUT_DIR="${MUSTANGIA_OUTPUT_DIR:-"${ROOT_DIR}/dist"}"
ISO_NAME="mustangia-26.04.1-amd64.iso"

if [[ "${EUID}" -ne 0 ]]; then
    printf 'Run this script as root, for example: sudo bash %s\n' "$0" >&2
    exit 1
fi

if [[ "$(dpkg --print-architecture)" != "amd64" ]]; then
    printf 'Mustangia ISO builds currently require an amd64 Ubuntu build host.\n' >&2
    exit 1
fi

for command in lb debootstrap dpkg install cp sha256sum; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        printf 'Required command not found: %s\n' "${command}" >&2
        exit 1
    fi
done

mkdir -p "${BUILD_DIR}" "${OUTPUT_DIR}"
BUILD_DIR="$(cd -- "${BUILD_DIR}" && pwd)"
OUTPUT_DIR="$(cd -- "${OUTPUT_DIR}" && pwd)"
cp -R "${ROOT_DIR}/live-build-config/." "${BUILD_DIR}/config/"

INCLUDES="${BUILD_DIR}/config/includes.chroot"
install -D -m 0755 "${ROOT_DIR}/welcome/mustangia_welcome.py" \
    "${INCLUDES}/usr/local/bin/mustangia-welcome"
install -D -m 0755 "${ROOT_DIR}/labs/mustangia_lab.py" \
    "${INCLUDES}/usr/local/bin/mustangia-lab"
install -D -m 0755 "${ROOT_DIR}/labs/mustangia_bundle.py" \
    "${INCLUDES}/usr/local/bin/mustangia-bundle"
mkdir -p "${INCLUDES}/usr/share/mustangia"
cp -R "${ROOT_DIR}/labs/templates" "${INCLUDES}/usr/share/mustangia/"

ISO_PATH="${OUTPUT_DIR}/${ISO_NAME}"
rm -f -- "${ISO_PATH}" "${ISO_PATH}.sha256"

cd "${BUILD_DIR}"
if [[ -f config/common ]]; then
    lb clean --purge
    rm -f -- config/binary config/bootstrap config/chroot config/common config/source
fi

lb config \
    --architecture amd64 \
    --archive-areas "main universe restricted multiverse" \
    --apt-recommends true \
    --binary-images iso-hybrid \
    --bootappend-live "boot=casper username=mustangia hostname=mustangia locales=en_US.UTF-8 keyboard-layouts=us" \
    --bootloader grub \
    --debian-installer false \
    --distribution resolute \
    --initramfs casper \
    --iso-application "Mustangia Student Linux" \
    --iso-preparer "Mustangia ISO Builder" \
    --iso-publisher "Mustangia" \
    --iso-volume "MUSTANGIA_26_04_1_AMD64" \
    --linux-packages linux-image \
    --memtest none \
    --mirror-bootstrap "https://archive.ubuntu.com/ubuntu/" \
    --mirror-binary "https://archive.ubuntu.com/ubuntu/" \
    --mirror-binary-security "https://security.ubuntu.com/ubuntu/" \
    --mirror-chroot "https://archive.ubuntu.com/ubuntu/" \
    --mirror-chroot-security "https://security.ubuntu.com/ubuntu/" \
    --mode ubuntu

lb build

if [[ ! -s binary.hybrid.iso ]]; then
    printf 'live-build completed without creating binary.hybrid.iso\n' >&2
    exit 1
fi

cp -- binary.hybrid.iso "${ISO_PATH}"
(cd "${OUTPUT_DIR}" && sha256sum "${ISO_NAME}" > "${ISO_NAME}.sha256")
printf 'ISO created: %s\nChecksum: %s.sha256\n' "${ISO_PATH}" "${ISO_PATH}"
