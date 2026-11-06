# Proton VPN Accessibility for NVDA

[Baca dalam Bahasa Indonesia](docs/README.id.md)

Proton VPN Accessibility is an add-on for the [NVDA screen reader](https://www.nvaccess.org/) that makes the
Proton VPN app for Windows usable with NVDA. Proton VPN leaves many of its buttons, options and tabs without a
name, so NVDA only says "button". This add-on gives them names, reads settings with their current state, and tells
you when your protection changes.

This add-on is made by InfiArtt. It is not made or endorsed by Proton AG.

## How this add-on came about

I'm Rafli, and I use NVDA every day. When I installed Proton VPN on Windows, I found much of it hard to use:
NVDA said "button" for most of the main window, the settings options had no names, and the country tabs read out
long internal names.

So I opened [NVDA MCP](https://github.com/InfiArtt/nvda-mcp), our add-on that lets an AI assistant see what NVDA
sees, and worked through Proton VPN with Claude Code, an AI coding assistant. Through NVDA MCP it read Proton VPN's
accessibility tree, listed every control NVDA could not name, opened each settings page and flyout to see what was
missing, and wrote the fixes. We loaded each change into my running NVDA and checked what NVDA would say before
moving on, until the whole app read properly. That session became this add-on.

## What it does

- **Names unlabeled controls.** Settings, NetShield, Kill switch, Port forwarding, Split tunneling and the
  title bar Menu are read by name. Each country, city and profile has a "Connect to" button, a "Servers in" button
  and a "More options for" button.
- **Reads values with their labels.** NVDA says "VPN IP, 159.26.115.101" and "Server load, 22%" instead of
  just the number, and "Current traffic" reads the download and upload speeds without the chart's axis numbers.
- **Reads settings with their state.** In Settings, NVDA says "Kill switch, Off" and "Protocol, Smart".
- **Names options.** The protocol, NetShield level, NAT type and network driver options have names, and the
  protocols that appear twice say which group they are in, such as "WireGuard, Reliability (TCP)".
- **Adds explanations.** Options and switches get Proton VPN's explanation as their description, such as
  "Protects your IP address by disconnecting you from the internet if you lose your VPN connection".
  NVDA reads descriptions when "Report object descriptions" is on, in NVDA's Object Presentation settings.
- **Reads flyouts and messages when they open.** Pressing VPN IP, Server load or the Profiles information
  button reads the whole flyout, not just the link inside it.
- **Announces protection changes.** When Proton VPN shows Protected, Unprotected or Connecting while it is
  the active window, NVDA says so.
- **Makes settings rows work with NVDA's activate command.** Rows such as Protocol and NetShield now open when
  activated from object navigation, not only with Enter.
- **Fixes names.** The country tabs and list headings no longer read internal names such as
  "ProtonVPN.Client.UI.Main…ViewModel".

## Commands

| Command | Keys | What it does |
|---|---|---|
| Report Proton VPN status | NVDA+Shift+V | Says whether you are protected, the server you are connected to and for how long. Works while Proton VPN's window is active. |

You can change the keys in NVDA's menu: Preferences, Input gestures, Proton VPN category.

## Requirements

- NVDA 2025.1 or later. Tested with NVDA 2026.3.
- Proton VPN for Windows version 5. Tested with version 5.1.9.

## Installing

1. Download the latest `protonVpnAccess-<version>.nvda-addon` from
   [Releases](https://github.com/InfiArtt/protonvpn-nvda/releases), or install Proton VPN Accessibility from
   NVDA's Add-on Store once it is there.
2. Open the file. NVDA asks whether to install the add-on; choose Yes.
3. Restart NVDA when it asks.

## Known limits

- The add-on reads Proton VPN's own text, so names follow the language of Proton VPN. Words the add-on adds,
  such as "Connect to", follow the language of NVDA.
- Proton VPN may change its window in an update. If a control stops being read correctly after an update,
  please [open an issue](https://github.com/InfiArtt/protonvpn-nvda/issues) and say which Proton VPN version you
  use.

## Reporting problems

Open an issue at [github.com/InfiArtt/protonvpn-nvda/issues](https://github.com/InfiArtt/protonvpn-nvda/issues).
Say what you pressed, what NVDA said and what you expected it to say, and include your NVDA and Proton VPN versions.

## Building from source

On Windows, from the repository folder:

1. `python -m venv .venv`
2. `.venv\Scripts\python -m pip install -r requirements-dev.txt`
3. `.venv\Scripts\python -m pytest`
4. `.venv\Scripts\python build_addon.py`, which writes `dist\protonVpnAccess-<version>.nvda-addon`.

To try changes without installing, turn on NVDA's developer scratchpad (NVDA Settings, Advanced), copy
`addon\appModules\protonvpn_client.py` to `%APPDATA%\nvda\scratchpad\appModules\`, switch to Proton VPN and press
NVDA+Ctrl+F3 to reload. Reload while Proton VPN is the active window; otherwise NVDA keeps the previous code
for it.

## License

Copyright (C) 2026 InfiArtt. This add-on is free software under the GNU General Public License, version 2 or
later. See [COPYING.txt](COPYING.txt).
