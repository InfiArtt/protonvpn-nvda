# Instructions for AI coding agents

Proton VPN Accessibility is an NVDA add-on (Python 3, NVDA 2025.1 or later) that makes Proton VPN for Windows
work with NVDA. Its users are mostly blind or low vision. The code is one app module,
`addon/appModules/protonvpn_client.py`, and follows NVDA's coding standards: tabs, camelCase, user-facing strings
wrapped in `_()` with `# Translators:` comments. `build_addon.py` and the tests follow PEP 8.

## Commands

On Windows, from the repository root:

- Install: `python -m venv .venv`, then `.venv\Scripts\python -m pip install -r requirements-dev.txt`.
- Test: `.venv\Scripts\python -m pytest`.
- Lint: `.venv\Scripts\ruff check .` and `.venv\Scripts\ruff format --check .`.
- Build: `.venv\Scripts\python build_addon.py` (writes `dist\protonVpnAccess-<version>.nvda-addon`).

## Rules

- **No AI attribution.** Don't add `Co-Authored-By` trailers, "generated with" footers or similar lines to
  commits, pull requests or documentation. The README's "How this add-on came about" section is the one place
  that tells the story, in the maintainer's words.
- **Accessibility first.** Names should say what a control does; messages should say what happened and what to do.
- **Don't push to `main`** and **ask first** before releases, tags or anything that publishes.
- **Never post in other people's repositories.** Submissions to the NV Access Add-on Store are made by a person;
  never open issues or pull requests in `nvaccess/addon-datastore`.
- Every translatable string needs an Indonesian translation in `addon/locale/id/LC_MESSAGES/nvda.po`; a test checks.
- The version lives in `addon/manifest.ini`; record changes in `CHANGELOG.md`. Pushing a `v*` tag publishes a
  GitHub release.
- Keep `docs/README.id.md` in step with `README.md`; both become the add-on's help pages.

## Trying changes

Turn on NVDA's developer scratchpad, copy the app module to `%APPDATA%\nvda\scratchpad\appModules\`, make Proton
VPN the active window, then reload plugins (NVDA+Ctrl+F3). Reloading while another app is active leaves Proton VPN
on the old code until the next reload. With NVDA MCP, `nvda_preview_speech` with target `window` shows what NVDA
says for every control; `nvda_find_objects` with `window` works while Proton VPN is in the background.
