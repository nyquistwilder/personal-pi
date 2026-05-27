#!/usr/bin/env python3
"""Scaffold the strict base repository from bundled assets."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path


PLACEHOLDERS = {
    "<PROJECT_NAME>": "project_name",
    "<ONE_PARAGRAPH_PROJECT_OVERVIEW>": "overview",
    "<SHORT_DESCRIPTION_OF_REPO_LAYOUT>": "layout",
    "<YEAR>": "year",
    "<COPYRIGHT HOLDER>": "copyright_holder",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the strict base repository assets into a new Git repository."
    )
    parser.add_argument("target_repo", type=Path, help="Path to the repository to scaffold")
    parser.add_argument("--project-name", help="Project name for README.md")
    parser.add_argument(
        "--overview",
        required=True,
        help="One-paragraph project overview for README.md",
    )
    parser.add_argument(
        "--layout",
        required=True,
        help="Short repository layout description for README.md",
    )
    parser.add_argument(
        "--copyright-holder",
        help="Copyright holder for LICENSE; defaults to git config user.name",
    )
    parser.add_argument(
        "--year",
        default=str(dt.date.today().year),
        help="Copyright year for LICENSE",
    )
    return parser.parse_args()


def run(command: list[str], cwd: Path | None = None) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"Required command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        output = exc.stdout.strip()
        details = f"\n{output}" if output else ""
        raise RuntimeError(f"Command failed: {' '.join(command)}{details}") from exc

    return completed.stdout.strip()


def git_user_name() -> str | None:
    try:
        value = run(["git", "config", "--get", "user.name"])
    except RuntimeError:
        return None
    value = value.strip()
    return value or None


def ensure_new_repo_target(target: Path) -> None:
    if target.exists() and not target.is_dir():
        raise RuntimeError(f"Target exists but is not a directory: {target}")

    target.mkdir(parents=True, exist_ok=True)
    disallowed = sorted(
        child.name for child in target.iterdir() if child.name != ".git"
    )
    if disallowed:
        joined = ", ".join(disallowed)
        raise RuntimeError(
            "Target repository is not empty. Only an existing .git directory is allowed. "
            f"Found: {joined}"
        )


def copy_assets(asset_root: Path, target: Path) -> None:
    if not asset_root.is_dir():
        raise RuntimeError(f"Missing bundled assets: {asset_root}")

    for source in sorted(asset_root.iterdir(), key=lambda path: path.name):
        destination = target / source.name
        if destination.exists():
            raise RuntimeError(f"Refusing to overwrite existing path: {destination}")
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)


def iter_template_text_files(target: Path) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(target.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(target).parts:
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        paths.append(path)
    return paths


def replace_placeholders(target: Path, values: dict[str, str]) -> None:
    replacements = {
        placeholder: values[key] for placeholder, key in PLACEHOLDERS.items()
    }
    for path in iter_template_text_files(target):
        text = path.read_text(encoding="utf-8")
        updated = text
        for placeholder, value in replacements.items():
            updated = updated.replace(placeholder, value)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def assert_placeholders_removed(target: Path) -> None:
    remaining: list[str] = []
    for path in iter_template_text_files(target):
        text = path.read_text(encoding="utf-8")
        for placeholder in PLACEHOLDERS:
            if placeholder in text:
                remaining.append(f"{path.relative_to(target)}: {placeholder}")
    if remaining:
        raise RuntimeError("Unreplaced placeholders remain: " + ", ".join(remaining))


def ensure_git_repo(target: Path) -> None:
    if (target / ".git").exists():
        return
    run(["git", "init"], cwd=target)


def stage_baseline(target: Path) -> None:
    run(["git", "add", "."], cwd=target)


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    asset_root = skill_root / "assets" / "base-repo-structure"
    target = args.target_repo.resolve()

    project_name = args.project_name or target.name
    copyright_holder = args.copyright_holder or git_user_name()
    if not copyright_holder:
        raise RuntimeError(
            "Missing --copyright-holder and git config user.name is not set."
        )

    values = {
        "project_name": project_name,
        "overview": args.overview,
        "layout": args.layout,
        "year": args.year,
        "copyright_holder": copyright_holder,
    }

    ensure_new_repo_target(target)
    copy_assets(asset_root, target)
    replace_placeholders(target, values)
    assert_placeholders_removed(target)
    ensure_git_repo(target)
    stage_baseline(target)

    print(f"Scaffolded base repository at {target}")
    print("Staged baseline files with git add .")
    print("Next required commands:")
    print("  nix flake lock")
    print("  git add flake.lock")
    print("  mise trust")
    print("  mise run install-hooks")
    print("  mise run check")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
