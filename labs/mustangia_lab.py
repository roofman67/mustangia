#!/usr/bin/env python3
"""Create a starter directory from one of the bundled student lab templates."""

import argparse
import os
from pathlib import Path
import shutil
import sys


LAB_KINDS = ("python", "web", "systems", "data-science")
TEMPLATES_DIR = Path(
    os.environ.get("MUSTANGIA_LAB_TEMPLATES", "/usr/share/mustangia/labs")
)


def create_lab(kind, destination=None, templates_dir=TEMPLATES_DIR):
    template = Path(templates_dir) / kind
    if not template.is_dir():
        raise FileNotFoundError(f"Lab template is not installed: {kind}")

    target = Path(destination).expanduser() if destination else (
        Path.home() / "MustangiaLabs" / kind
    )
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite existing path: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target)
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mustangia-lab")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="list available starter labs")
    create = commands.add_parser("create", help="copy a starter lab")
    create.add_argument("kind", choices=LAB_KINDS)
    create.add_argument("destination", nargs="?")
    args = parser.parse_args(argv)

    if args.command == "list":
        print("\n".join(LAB_KINDS))
        return 0

    try:
        target = create_lab(args.kind, args.destination)
    except (FileExistsError, FileNotFoundError, OSError) as error:
        print(f"mustangia-lab: {error}", file=sys.stderr)
        return 1
    print(f"Created {args.kind} lab at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
