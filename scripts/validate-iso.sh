#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ISO_PATH="${1:-"${ROOT_DIR}/dist/mustangia-26.04.1-amd64.iso"}"

if [[ ! -s "${ISO_PATH}" ]]; then
    printf 'ISO not found or empty: %s\n' "${ISO_PATH}" >&2
    exit 1
fi
if ! command -v xorriso >/dev/null 2>&1; then
    printf 'Required command not found: xorriso\n' >&2
    exit 1
fi
if [[ ! -f "${ISO_PATH}.sha256" ]]; then
    printf 'Checksum file not found: %s.sha256\n' "${ISO_PATH}" >&2
    exit 1
fi

ISO_DIR="$(cd -- "$(dirname -- "${ISO_PATH}")" && pwd)"
ISO_BASENAME="$(basename -- "${ISO_PATH}")"
(cd "${ISO_DIR}" && sha256sum --check "${ISO_BASENAME}.sha256")

BOOT_REPORT="$(xorriso -indev "${ISO_PATH}" -report_el_torito plain 2>&1)"
printf '%s\n' "${BOOT_REPORT}"
if ! grep -qi 'BIOS' <<< "${BOOT_REPORT}"; then
    printf 'ISO boot catalog does not report a BIOS boot entry.\n' >&2
    exit 1
fi
if ! grep -qi 'UEFI' <<< "${BOOT_REPORT}"; then
    printf 'ISO boot catalog does not report a UEFI boot entry.\n' >&2
    exit 1
fi
