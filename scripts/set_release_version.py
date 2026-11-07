"""Align package major/minor with a tagged study release."""

import argparse
from pathlib import Path
import re
import tomllib


def parse_version(version: str) -> tuple[int, int, int]:
    """Accept canonical, non-negative X.Y.Z versions only."""
    if not isinstance(version, str) or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version
    ):
        raise ValueError(f"Expected a canonical X.Y.Z version, got {version!r}")
    return tuple(int(part) for part in version.split("."))


def select_study_version(current: str, study_tag: str, version: str = "") -> str:
    """Follow the study's major/minor while allowing independent package patches."""
    if not study_tag.startswith("v"):
        raise ValueError("Study release tag must have the form vX.Y.Z")
    study = parse_version(study_tag[1:])
    package = parse_version(current)
    if study[:2] < package[:2]:
        raise ValueError("Cannot publish an older study major/minor series")
    if version:
        requested = parse_version(version)
        if requested[:2] != study[:2]:
            raise ValueError("Package major/minor must match the study release")
        if requested < package:
            raise ValueError(f"Cannot downgrade from {current} to {version}")
        return version
    if study[:2] == package[:2]:
        return f"{package[0]}.{package[1]}.{package[2] + 1}"
    return f"{study[0]}.{study[1]}.0"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-tag", required=True)
    parser.add_argument("--version", default="")
    args = parser.parse_args()
    project = Path("pyproject.toml")
    source = project.read_text()
    current = tomllib.loads(source)["project"]["version"]
    try:
        version = select_study_version(current, args.study_tag, args.version)
    except ValueError as error:
        parser.exit(1, f"Error: {error}\n")
    # This repository has one version assignment; refuse an ambiguous edit.
    updated, count = re.subn(r'(?m)^version = "' + re.escape(current) + r'"$',
                             f'version = "{version}"', source)
    if count != 1:
        parser.exit(1, "Expected one project version assignment\n")
    project.write_text(updated)
    print(version)


if __name__ == "__main__":
    main()
