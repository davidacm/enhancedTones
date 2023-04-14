# ● enhanced tones
# Copyright (C) 2022 - 2023 David CM
import addonHandler, config, globalPluginHandler, wx
from gui import guiHelper, settingsDialogs, SettingsPanel
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


class EnhancedTonesSettings(SettingsPanel):
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

	def onSave(self):
		l = self.lbs[self.lbsList.GetSelection()]
		config.conf[CONFIG_PATH]["toneGenerator"] = l.id
		config.conf[CONFIG_PATH]["enableAddon"] = self.enableAddon.GetValue()
		config.post_configProfileSwitch.notify()
