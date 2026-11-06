# Proton VPN Accessibility: makes Proton VPN for Windows work well with NVDA.
# Copyright (C) 2026 Rafli
# This file is covered by the GNU General Public License, version 2 or later.
# See the file COPYING for more details.
#
# Proton VPN 5 (WinUI 3) leaves many controls without an accessible name and keeps their state and
# explanation in separate text blocks. This app module builds names and descriptions from those
# text blocks, reads flyouts and dialogs when they open and announces when the protection changes.

import re

import addonHandler
import api
import appModuleHandler
import controlTypes
import core
import ui
import UIAHandler
from comtypes import COMError
from keyboardHandler import KeyboardInputGesture
from logHandler import log
from NVDAObjects.UIA import UIA
from scriptHandler import script

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	# Running from NVDA's developer scratchpad rather than an installed add-on.
	pass

# Texts up to this long are a label or a state ("Off", "RECOMMENDED"); longer ones are explanations.
SHORT_TEXT = 25

# Buttons whose name should be built from all of their visible text.
JOIN_TEXT_IDS = {
	"NetShieldWidgetButton",
	"KillSwitchWidgetButton",
	"PortForwardingWidgetButton",
	"SplitTunnelingWidgetButton",
	"SettingsButton",
	"ShowIpFlyoutButton",
	"ShowServerLoadFlyoutButton",
	"ShowProtocolFlyoutButton",
	"ShowVolumeFlyoutButton",
}

FIXED_NAMES = {
	# Translators: Name of the menu button in Proton VPN's title bar.
	"TitleBarMenuButton": _("Menu"),
	# Translators: Name of the button that goes back to the previous Proton VPN settings page.
	"GoBackButton": _("Back"),
	# Translators: Name of the button that closes Proton VPN's settings.
	"CloseSettingsButton": _("Close settings"),
	# Translators: Name of the button that closes a Proton VPN message.
	"CloseContentDialogButton": _("Close"),
	# Translators: Name of the button that explains a Proton VPN list, such as Profiles.
	"TabInfoButton": _("More information"),
	# Translators: Name of the grip that changes the width of Proton VPN's sidebar.
	"SidebarSizeGrip": _("Resize sidebar"),
}

COUNTRY_TABS = {
	# Translators: Name of the tab listing all countries in Proton VPN.
	"All": _("All countries"),
	# Translators: Name of the Secure Core countries tab in Proton VPN.
	"SecureCore": _("Secure Core"),
	# Translators: Name of the P2P countries tab in Proton VPN.
	"P2P": _("P2P"),
	# Translators: Name of the Tor countries tab in Proton VPN.
	"Tor": _("Tor"),
}

# Controls that get a name when Proton VPN leaves it empty.
NAMED_ROLES = {
	controlTypes.Role.BUTTON,
	controlTypes.Role.TOGGLEBUTTON,
	controlTypes.Role.RADIOBUTTON,
	controlTypes.Role.CHECKBOX,
	controlTypes.Role.COMBOBOX,
	controlTypes.Role.LISTITEM,
	controlTypes.Role.TAB,
	controlTypes.Role.MENUITEM,
}

SPEED_TEXT = re.compile(r"/s$")
MASKED_TEXT = re.compile(r"^[*.]+$")
TYPE_NAME = re.compile(r"^ProtonVPN\.Client\.")
LEARN_MORE = re.compile(r"\s*Learn more\s*$")


def _condition(propertyId, value):
	return UIAHandler.handler.clientObject.CreatePropertyCondition(propertyId, value)


def _texts(element, children=False):
	"""Names of the text blocks inside a UIA element, in order, without empty ones."""
	scope = UIAHandler.TreeScope_Children if children else UIAHandler.TreeScope_Descendants
	found = element.FindAll(scope, _condition(UIAHandler.UIA_ControlTypePropertyId, UIAHandler.UIA_TextControlTypeId))
	texts = []
	for index in range(found.Length):
		name = found.GetElement(index).CurrentName
		if name and name.strip():
			texts.append(name.strip())
	return texts


def _clean(text):
	"""Drops the trailing "Learn more" link text from an explanation; the link is its own control."""
	return LEARN_MORE.sub("", text).strip()


def _speakable(text):
	# Translators: Said instead of an IP address that Proton VPN hides with asterisks.
	return _("hidden") if MASKED_TEXT.match(text) else text


def _humanize(automationId):
	"""Turns an AutomationId such as "GoBackButton" into "Go back"."""
	words = re.sub(r"(Button|Toggle|Switch)$", "", automationId)
	words = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|_", " ", words).strip()
	return words[:1].upper() + words[1:].lower() if words else ""


def _rawWalker():
	return UIAHandler.handler.clientObject.RawViewWalker


def _nearbyExplanation(element):
	"""The explanation text just before a toggle or combo box, in its card or the card around it."""
	walker = _rawWalker()
	for _level in range(2):
		sibling = walker.GetPreviousSiblingElement(element)
		steps = 0
		while sibling and steps < 4:
			if sibling.CurrentControlType == UIAHandler.UIA_TextControlTypeId:
				text = _clean(sibling.CurrentName or "")
				if len(text) > SHORT_TEXT:
					return text
			sibling = walker.GetPreviousSiblingElement(sibling)
			steps += 1
		element = walker.GetParentElement(element)
		if not element:
			break
	return None


def _sectionHeading(element):
	"""The text heading above a radio button, such as "Reliability (TCP)", skipping other radio buttons."""
	walker = _rawWalker()
	sibling = walker.GetPreviousSiblingElement(element)
	while sibling:
		controlType = sibling.CurrentControlType
		if controlType == UIAHandler.UIA_TextControlTypeId:
			return sibling.CurrentName
		if controlType != UIAHandler.UIA_RadioButtonControlTypeId:
			return None
		sibling = walker.GetPreviousSiblingElement(sibling)
	return None


class ProtonControl(UIA):
	"""A Proton VPN control whose name and description are completed from its visible text."""

	def _get_protonClassName(self):
		return self._getUIACacheablePropertyValue(UIAHandler.UIA_ClassNamePropertyId) or ""

	def _get_name(self):
		name = super().name or ""
		try:
			better = self._betterName(name)
		except Exception:
			log.debugWarning("Proton VPN Accessibility could not name a control", exc_info=True)
			return name
		return better if better else name

	def _get_description(self):
		description = super().description or ""
		if description:
			return description
		try:
			return self._betterDescription() or ""
		except Exception:
			log.debugWarning("Proton VPN Accessibility could not describe a control", exc_info=True)
			return ""

	def _betterName(self, name):
		automationId = self.UIAAutomationId or ""
		if automationId in FIXED_NAMES and (not name or name.startswith("ms-resource:")):
			return FIXED_NAMES[automationId]
		if automationId in JOIN_TEXT_IDS:
			# Words before numbers, so "40 NetShield" is read as "NetShield, 40".
			texts = sorted(_texts(self.UIAElement), key=lambda text: text[:1].isdigit())
			return ", ".join(texts)
		if automationId.startswith("Connect_to_") or automationId.startswith("Disconnect_from_"):
			return self._connectionName(automationId)
		if automationId == "ListViewHeaderItem" or TYPE_NAME.match(name):
			return self._nameFromTypeName(name)
		if automationId in ("ExpanderButton", "SecondaryButton") and not name:
			return self._rowButtonName(automationId)
		if automationId == "E" and self.role == controlTypes.Role.BUTTON:
			return self._trafficName()
		if self.protonClassName == "Popup" and name == "Popup":
			# Flyouts are all called "Popup"; use their first line, such as "VPN IP", instead.
			texts = _texts(self.UIAElement)
			return texts[0] if texts else None
		if self.role not in NAMED_ROLES:
			return None
		texts = _texts(self.UIAElement)
		if not name:
			return self._nameForUnlabeled(automationId, texts)
		isRow = self.protonClassName == "Button" or self.protonClassName.endswith("SettingsCard")
		if isRow and texts and texts[0] == name:
			# Settings rows: add the state shown next to the label, such as "Kill switch, Off".
			states = [text for text in texts[1:] if len(text) <= SHORT_TEXT and text != name]
			if states:
				return ", ".join([name] + states)
		return None

	def _nameForUnlabeled(self, automationId, texts):
		if texts:
			extras = [text for text in texts[1:] if len(text) <= SHORT_TEXT]
			name = ", ".join([texts[0]] + extras)
			if self.role == controlTypes.Role.RADIOBUTTON:
				heading = _sectionHeading(self.UIAElement)
				if heading:
					# Translators: A Proton VPN option and the group it belongs to, e.g. "WireGuard, Reliability (TCP)".
					name = _("{option}, {group}").format(option=name, group=heading)
			return name
		parent = self.parent
		if isinstance(parent, UIA) and parent.role == controlTypes.Role.GROUPING and parent.name:
			if not parent.name.endswith("Content") and not TYPE_NAME.match(parent.name):
				return parent.name
		if self._isRevealIpButton():
			# Translators: Name of the Proton VPN button that shows or hides your real IP address.
			return _("Show or hide your IP")
		return _humanize(automationId) or None

	def _isRevealIpButton(self):
		sibling = _rawWalker().GetPreviousSiblingElement(self.UIAElement)
		return bool(sibling) and bool(MASKED_TEXT.match(sibling.CurrentName or ""))

	def _connectionName(self, automationId):
		texts = _texts(self.UIAElement)
		if not texts:
			return None
		place = ", ".join(texts)
		if automationId.startswith("Disconnect_from_"):
			# Translators: Proton VPN button that disconnects from a place, e.g. "Disconnect from Singapore".
			return _("Disconnect from {place}").format(place=place)
		# Translators: Proton VPN button that connects to a place, e.g. "Connect to Singapore".
		return _("Connect to {place}").format(place=place)

	def _rowButtonName(self, automationId):
		parent = self.parent
		place = parent.name if parent else ""
		if not place:
			return None
		if automationId == "ExpanderButton":
			# Translators: Proton VPN button that shows or hides the servers of a place, e.g. "Servers in Singapore".
			return _("Servers in {place}").format(place=place)
		# Translators: Proton VPN button that opens a menu for a connection or profile, e.g. "More options for Gaming".
		return _("More options for {place}").format(place=place)

	def _nameFromTypeName(self, name):
		"""Controls whose name is an internal .NET type name, such as the country tabs and list headings."""
		match = re.search(r"\.(\w+)CountriesComponentViewModel$", name)
		if match and match.group(1) in COUNTRY_TABS:
			return COUNTRY_TABS[match.group(1)]
		texts = _texts(self.UIAElement, children=True)
		return ", ".join(texts) if texts else ""

	def _trafficName(self):
		"""The current traffic graph: keep the title and the speeds, drop the axis numbers."""
		texts = _texts(self.UIAElement)
		if not texts:
			return None
		return ", ".join([texts[0]] + [text for text in texts[1:] if SPEED_TEXT.search(text)])

	def _betterDescription(self):
		if self.role not in NAMED_ROLES:
			return None
		if (self.UIAAutomationId or "").startswith(("Connect_to_", "Disconnect_from_")):
			return None
		texts = [_clean(text) for text in _texts(self.UIAElement)[1:]]
		explanations = [text for text in texts if len(text) > SHORT_TEXT]
		if explanations:
			return " ".join(explanations)
		if self.role in (controlTypes.Role.TOGGLEBUTTON, controlTypes.Role.COMBOBOX, controlTypes.Role.BUTTON):
			if self.protonClassName in ("ToggleSwitch", "ComboBox"):
				return _nearbyExplanation(self.UIAElement)
		return None

	def doAction(self, index=None):
		# Proton VPN's settings rows report that they can be invoked, then fail with "No such interface
		# supported"; Enter works, so press it on the row instead.
		try:
			super().doAction(index)
		except COMError:
			if self.role != controlTypes.Role.BUTTON:
				raise
			self.setFocus()
			# Give the row a moment to take focus before Enter reaches it.
			core.callLater(100, KeyboardInputGesture.fromName("enter").send)


class AppModule(appModuleHandler.AppModule):
	# Translators: Category of Proton VPN Accessibility's commands in NVDA's Input Gestures dialog.
	scriptCategory = _("Proton VPN")

	_lastPopup = None
	_lastProtection = None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA):
			clsList.insert(0, ProtonControl)

	def event_gainFocus(self, obj, nextHandler):
		nextHandler()
		if not isinstance(obj, UIA):
			return
		try:
			self._readPopup(obj)
		except Exception:
			log.debugWarning("Proton VPN Accessibility could not read a flyout", exc_info=True)

	def _readPopup(self, obj):
		"""Read the text of a flyout or message when focus first moves into it; menus read themselves."""
		walker = _rawWalker()
		element = obj.UIAElement
		popup = None
		for _level in range(10):
			element = walker.GetParentElement(element)
			if not element:
				break
			if element.CurrentClassName == "Popup":
				popup = element
				break
		if not popup:
			self._lastPopup = None
			return
		runtimeId = tuple(popup.GetRuntimeId())
		if runtimeId == self._lastPopup:
			return
		self._lastPopup = runtimeId
		if popup.FindFirst(
			UIAHandler.TreeScope_Descendants, _condition(UIAHandler.UIA_ClassNamePropertyId, "MenuFlyout")
		):
			return
		texts = _texts(popup)
		if texts and popup.CurrentName in ("Popup", texts[0]):
			# NVDA already said the first line as the flyout's name.
			texts = texts[1:]
		# Links and buttons say their own text when focused.
		ownText = {obj.name}
		found = popup.FindAll(
			UIAHandler.TreeScope_Descendants,
			_condition(UIAHandler.UIA_ControlTypePropertyId, UIAHandler.UIA_HyperlinkControlTypeId),
		)
		for index in range(found.Length):
			ownText.add(found.GetElement(index).CurrentName)
		texts = [_speakable(text) for text in texts if text not in ownText]
		if texts:
			ui.message(", ".join(texts))

	def event_nameChange(self, obj, nextHandler):
		if isinstance(obj, UIA) and obj.UIAAutomationId == "ProtectionTitle" and obj.name != self._lastProtection:
			self._lastProtection = obj.name
			ui.message(obj.name)
		nextHandler()

	@script(
		# Translators: Description of the command that reads Proton VPN's connection status.
		description=_("Reports whether Proton VPN protects you, where you are connected and for how long"),
		gesture="kb:NVDA+shift+v",
	)
	def script_reportVpnStatus(self, gesture):
		foreground = api.getForegroundObject()
		try:
			window = UIAHandler.handler.clientObject.ElementFromHandle(foreground.windowHandle)
			parts = []
			for automationId in ("ProtectionTitle", "ConnectionCardDescription", "ProtectionDescription"):
				element = window.FindFirst(
					UIAHandler.TreeScope_Descendants, _condition(UIAHandler.UIA_AutomationIdPropertyId, automationId)
				)
				if element and element.CurrentName and element.CurrentName.strip():
					parts.append(element.CurrentName.strip())
		except Exception:
			log.debugWarning("Proton VPN Accessibility could not read the status", exc_info=True)
			parts = []
		if parts:
			ui.message(", ".join(parts))
		else:
			# Translators: Said when the Proton VPN main window, which shows the status, is not open.
			ui.message(_("Status not available. Open Proton VPN's main window and try again."))
