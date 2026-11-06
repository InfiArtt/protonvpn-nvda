# Changelog

All notable changes to Proton VPN Accessibility are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-06

First release, tested with Proton VPN 5.1.9 and NVDA 2026.3.

### Added

- Names for Proton VPN's unlabeled buttons: Settings, NetShield, Kill switch, Port forwarding, Split tunneling,
  Menu, Back, Close settings, the information and close buttons of messages, and the button that shows your IP.
- "Connect to", "Disconnect from", "Servers in" and "More options for" buttons for every country, city and profile.
- Labels with values on the main page, such as "VPN IP, 159.26.115.101" and "Server load, 22%".
- The state of each settings row, such as "Kill switch, Off".
- Names for protocol, NetShield, NAT type and network driver options, with their group where a name repeats.
- Proton VPN's explanations as descriptions of options and switches.
- Flyouts and messages are read when they open.
- Protected, Unprotected and Connecting are announced when they change.
- NVDA+Shift+V reports the connection status.
- NVDA's activate command opens settings rows.
- Indonesian translation.

### Fixed

- Country tabs and list headings read their visible text instead of internal names.
