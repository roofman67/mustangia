#!/usr/bin/env python3
"""Install optional, explicitly selected packages from Ubuntu repositories."""

import argparse
import os
import subprocess
import sys


BUNDLES = {
    "web": ("nodejs", "npm", "php-cli", "php-sqlite3", "sqlite3", "nginx"),
    "data-science": (
        "python3-numpy",
        "python3-pandas",
        "python3-matplotlib",
        "python3-sklearn",
        "python3-seaborn",
    ),
    "systems": (
        "qemu-system-x86",
        "qemu-utils",
        "gdb-multiarch",
        "strace",
        "valgrind",
        "binutils",
    ),
}


def is_root():
    return hasattr(os, "geteuid") and os.geteuid() == 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mustangia-bundle")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="list optional package bundles")
    install = commands.add_parser("install", help="install one optional bundle")
    install.add_argument("name", choices=tuple(BUNDLES))
    args = parser.parse_args(argv)

    if args.command == "list":
        print("\n".join(BUNDLES))
        return 0

    if not is_root():
        command = ["sudo", sys.executable, __file__, "install", args.name]
        subprocess.run(command, check=True)
        return 0

    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(
        ["apt-get", "install", "--no-install-recommends", *BUNDLES[args.name]],
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
