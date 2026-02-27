# ● enhanced tones
# Copyright (C) 2022 - 2023 David CM
import addonHandler, config, globalPluginHandler, os, wx
from gui import guiHelper, settingsDialogs
try:
	from gui.message import MessageDialog as _NVDAMessageDialog, DialogType as _DialogType
	_HAS_NEW_MESSAGE_DIALOG = True
except ImportError:
	from gui import nvdaControls
	_HAS_NEW_MESSAGE_DIALOG = False
from ._tones import *

addonHandler.initTranslation()


confspec = {
	"enableAddon": 'boolean(default=True)',
	"toneGenerator": f'string(default="{SineGenerator.id}")'
}
CONFIG_PATH = 'enhancedTones'
config.conf.spec[CONFIG_PATH] = confspec

origBeep = tones.beep
def replaceBeepFunction():
	try:
		from tones import decide_beep as d
		d.register(beep)
	except:
		tones.beep = beep

def resetBeepFunction():
	try:
		from tones import decide_beep as d
		d.unregister(beep)
	except:
		tones.beep = origBeep


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.handleConfigProfileSwitch()
		settingsDialogs.NVDASettingsDialog.categoryClasses.append(EnhancedTonesSettings)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def setGenerator(self, toneGen):
		terminate()
		initialize(toneGen, 44100)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		self.disableAddon()

	def disableAddon(self):
		resetBeepFunction()
		terminate()

	def handleConfigProfileSwitch(self):
		if not config.conf[CONFIG_PATH]["enableAddon"]:
			self.disableAddon()
			return
		replaceBeepFunction()
		name = config.conf[CONFIG_PATH]["toneGenerator"]
		if name in availableToneGenerators:
			self.setGenerator(availableToneGenerators[name])
		else:
			self.setGenerator(OrigTone)


if _HAS_NEW_MESSAGE_DIALOG:
	class DonationDialog(wx.Dialog):
		def __init__(self, parent, title, message, donateOptions):
			super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
			self.donateOptions = donateOptions
			sizer = wx.BoxSizer(wx.VERTICAL)
			text = wx.StaticText(self, label=message)
			text.Wrap(400)
			sizer.Add(text, 0, wx.ALL | wx.EXPAND, 10)
			btnSizer = wx.BoxSizer(wx.VERTICAL)
			for k in donateOptions:
				btn = wx.Button(self, label=k['label'], name=k['url'])
				btn.Bind(wx.EVT_BUTTON, self.onDonate)
				btnSizer.Add(btn, 0, wx.ALL | wx.EXPAND, 3)
			cancelBtn = wx.Button(self, id=wx.ID_CANCEL, label=_("&Not now"))
			cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))
			btnSizer.Add(cancelBtn, 0, wx.ALL | wx.CENTER, 3)
			sizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 10)
			self.SetSizerAndFit(sizer)
			self.CenterOnParent()

		def onDonate(self, evt):
			donateBtn = evt.GetEventObject()
			donateUrl = donateBtn.Name
			os.startfile(donateUrl)
			self.EndModal(wx.OK)
else:
	class DonationDialog(nvdaControls.MessageDialog):
		def __init__(self, parent, title, message, donateOptions):
			self.donateOptions = donateOptions
			super().__init__(parent, title, message, dialogType=nvdaControls.MessageDialog.DIALOG_TYPE_WARNING)

		def _addButtons(self, buttonHelper):
			for k in self.donateOptions:
				btn = buttonHelper.addButton(self, label=k['label'], name=k['url'])
				btn.Bind(wx.EVT_BUTTON, self.onDonate)
			cancelBtn = buttonHelper.addButton(self, id=wx.ID_CANCEL, label=_("&Not now"))
			cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))

		def onDonate(self, evt):
			donateBtn = evt.GetEventObject()
			donateUrl = donateBtn.Name
			os.startfile(donateUrl)
			self.EndModal(wx.OK)


def showDonationsDialog(parentWindow, addonName, donateOptions):
	title = _("Request for contributions to %s") % addonName
	message = _("""Creating add-ons demands substantial time and effort. With limited job prospects in my country, your donations could significantly aid in dedicating more time to developing free plugins for the community.
Your contribution would support the development of this and other free projects.
Would you like to contribute to this cause? Select from our available payment methods below. You will be redirected to the corresponding website to complete your donation.
Thank you for your support and generosity.""")
	return DonationDialog(parentWindow, title,  message, donateOptions).ShowModal()


DONATE_METHODS = (
	{
		'label': _('Using Paypal'),
		'url': 'https://paypal.me/davicm'
	},
	{
		'label': _('using Co-fi'),
		'url': 'https://ko-fi.com/davidacm'
	},
	{
		'label': _('See more methods on my github Page'),
		'url': 'https://davidacm.github.io/donations/'
	}
)


class EnhancedTonesSettings(settingsDialogs.SettingsPanel):
	# Translators: This is the label for the enhanced tones  settings panel.
	title = _("Enhanced tones")
	helpId = "EnhancedTonesSettings"

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: label for a checkbox option in the enhanced tones settings panel.
		self.enableAddon = sHelper.addItem(
			wx.CheckBox(self, label=_("&Enable this add-on. If disabled, the original function of NVDA will be used"))
		)
		self.enableAddon.SetValue(config.conf[CONFIG_PATH]["enableAddon"])

		# Translators: This is the label for a combobox in the
		# Enhanced tones settings panel.
		generatorLabel = _("&Generator to produce tones:")
		self.lbs = sorted(availableToneGenerators.values(), key = lambda k: k.name)
		choises = [k.name for k in self.lbs]
		self.lbsList = sHelper.addLabeledControl(generatorLabel, wx.Choice, choices=choises)
		index = 0
		for i, k in enumerate(self.lbs):
			if config.conf[CONFIG_PATH]["toneGenerator"] == k.id:
				index = i
		self.lbsList.SetSelection(index)
		donateButton = sHelper.addItem(wx.Button(self, label=_("&Support Enhanced tones add-on")))
		donateButton.Bind(wx.EVT_BUTTON, lambda e: showDonationsDialog(self, "Enhanced tones", DONATE_METHODS))

	def onSave(self):
		l = self.lbs[self.lbsList.GetSelection()]
		config.conf[CONFIG_PATH]["toneGenerator"] = l.id
		config.conf[CONFIG_PATH]["enableAddon"] = self.enableAddon.GetValue()
		config.post_configProfileSwitch.notify()
