"""Checks that run without NVDA: translations, versions and the built package."""

import ast
import configparser
import re
import zipfile
from pathlib import Path

import build_addon

ROOT = Path(__file__).resolve().parent.parent
ADDON_DIR = ROOT / "addon"


def translatable_strings() -> set[str]:
    """Every literal string passed to _() in the add-on's code."""
    strings = set()
    for path in ADDON_DIR.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_"
                and node.args
                and isinstance(node.args[0], ast.Constant)
            ):
                strings.add(node.args[0].value)
    return strings


def test_every_string_has_an_indonesian_translation():
    catalog = build_addon.parse_po(ADDON_DIR / "locale" / "id" / "LC_MESSAGES" / "nvda.po")
    missing = sorted(text for text in translatable_strings() if not catalog.get(text))
    assert not missing, f"Add these to addon/locale/id/LC_MESSAGES/nvda.po: {missing}"


def test_translations_keep_their_placeholders():
    catalog = build_addon.parse_po(ADDON_DIR / "locale" / "id" / "LC_MESSAGES" / "nvda.po")
    for msgid, msgstr in catalog.items():
        if msgid:
            assert sorted(re.findall(r"{\w+}", msgid)) == sorted(re.findall(r"{\w+}", msgstr)), msgid


def test_every_translatable_string_has_a_translators_comment():
    for path in ADDON_DIR.rglob("*.py"):
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines):
            if re.search(r"\b_\(\s*\"", line):
                before = "\n".join(lines[max(0, number - 3) : number + 1])
                assert "# Translators:" in before, f"{path.name}:{number + 1} needs a # Translators: comment"


def test_changelog_has_the_manifest_version():
    version = build_addon.read_manifest()["version"].strip('"')
    assert f"## [{version}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_build_contains_the_add_on(tmp_path, monkeypatch):
    monkeypatch.setattr(build_addon, "DIST_DIR", tmp_path)
    with zipfile.ZipFile(build_addon.build()) as archive:
        names = set(archive.namelist())
        manifest = configparser.ConfigParser()
        manifest.read_string("[m]\n" + archive.read("manifest.ini").decode("utf-8"))
    assert {
        "manifest.ini",
        "appModules/protonvpn_client.py",
        "locale/id/manifest.ini",
        "locale/id/LC_MESSAGES/nvda.mo",
        "doc/en/readme.html",
        "doc/id/readme.html",
        "COPYING.txt",
    } <= names
    assert not any(name.endswith((".po", ".pyc")) or "__pycache__" in name for name in names)
    assert manifest["m"]["name"].strip('"') == "protonVpnAccess"
