# ● enhanced tones
# Copyright (C) 2022 David CM
import config, globalPluginHandler
from ._tones import *
from ._configHelper import *

class AddonConfig(BaseConfig):
	path = 'enhancedTones'
	toneGenerator = 'int(default=0)'
	addonEnabled = 'boolean(default=False)'

AF = registerConfig(AddonConfig)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.origBeep = tones.beep
		self.setGenerator(ToneGenerator)

	def setGenerator(self, gen):
		terminate()
		initialize(gen, 44100)
		tones.beep=beep

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		tones.beep = self.origBeep
		terminate()
