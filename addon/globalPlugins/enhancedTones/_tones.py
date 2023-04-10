# ● _tones
# an utility to generate tones.
# Copyright (C) 2022 - 2023 David CM

import addonHandler, config, math, nvwave, threading, tones
from ctypes import c_short, create_string_buffer
from io import BytesIO
from NVDAHelper import generateBeep

addonHandler.initTranslation()


class OrigTone:
	name = _("Native tone generator")
	id = 'OrigTone'
	def __init__(self, hz=None):
		self.samples = b''

	def startGenerate(self, hz,length,left,right):
		buf=create_string_buffer(generateBeep(None,hz,length,left,right))
		generateBeep(buf,hz,length,left,right)
		self.samples = BytesIO(buf)
		self.samples.size = len(buf)

	def nextChunk(self, size=8820):
		while True:
			rest = self.samples.size -self.samples.tell()
			# to avoid very small chunks at the end. Append the last part if is less than size*2
			if rest < size*2:
				size = rest
			d = self.samples.read(size)
			if d:
				yield d
			else:
				return


class ToneGenerator:
	name = _("Custom tone generator")
	id = 'ToneGenerator'
	def __init__(self, rate=44100):
		self.bytes = 2
		self.maxAmplitude = int(2 ** (self.bytes * 8) / 2) - 1
		self.rate = rate
		self.freq = 0

	def sine_wave(self, freq):
		cs = float(2 *math.pi *freq /float(self.rate))
		i=0
		while True:
			yield float(math.sin(cs *i))
			i+=1
			if i == self.rate:
				i=0

	def normalizeSample(self, sample):
		ret = int(sample * self.maxAmplitude)
		if ret < -self.maxAmplitude:
			ret = -self.maxAmplitude
		elif ret > self.maxAmplitude:
			ret = self.maxAmplitude
		return c_short(ret)

	def setToneVals(self, freq, time, ampL=0.5, ampR=0.5):
		self.numSamples = int(time *self.rate)
		self.curChunk = 0
		if freq != self.freq:
			self.freq = freq
			self.gen = self.sine_wave(freq)
		self.time = time
		self.ampL = ampL
		self.ampR = ampR

	def nextChunk(self, size=4000):
		while self.curChunk < self.numSamples:
			rest = self.numSamples -self.curChunk
			# to avoid very small chunks at the end. Append the last part if is less than size*2
			if rest < size*2:
				size = rest
			self.curChunk += size
			samples = BytesIO()
			for i in range(size):
				w = next(self.gen)
				samples.write(self.normalizeSample(self.ampL * w))
				samples.write(self.normalizeSample(self.ampR * w))
			yield samples.getvalue()

	def startGenerate(self, hz, length, left, right):
		self.setToneVals(hz, length/1000.0, left/100.0, right/100.0)


class PlayerTone(threading.Thread):
	def __init__(self, toneGen, hz):
		super().__init__(target=self.run)
		self.tonePlayer = None
		self.hz = hz
		self.samples = b""
		self.values = None
		self.waitBeep = threading.Event()
		self.stopFlag = False
		self.chunkSize = 2000
		self.setToneGen(toneGen, hz)
		self.setPlayer()

	def setPlayer(self, outputDevice=None):
		if not outputDevice:
			outputDevice = config.conf["speech"]["outputDevice"]
		self.tonePlayer = nvwave.WavePlayer(2, self.hz, 16, outputDevice=outputDevice)

	def setToneGen(self, toneGen, hz):
		if toneGen == OrigTone:
			hz = 44100
		self.hz = hz
		self.toneGen = toneGen(hz)
		if self.tonePlayer and self.hz != hz:
				self.player.close()
				self.setPlayer()

	def run(self):
		while True:
			self.waitBeep.wait()
			if self.stopFlag: break
			hz, length, left, right = self.values
			self.waitBeep.clear()
			self.toneGen.startGenerate(hz,length,left,right)
			for data in self.toneGen.nextChunk():
				self.tonePlayer.feed(data)
				if self.waitBeep.is_set():
					break
		self.tonePlayer.close()
		self.tonePlayer= None

	def beep(self, hz,length,left, right):
		self.values = (hz, length, left, right)
		self.waitBeep.set()

	def terminate(self):
		self.stopFlag = True
		self.waitBeep.set()


toneThread= None
def initialize(toneGen, hz):
	global toneThread
	toneThread = PlayerTone(toneGen, hz)
	toneThread.start()


def beep(
		hz: float,
		length: int,
		left: int = 50,
		right: int = 50,
		isSpeechBeepCommand: bool = False
):
	toneThread.beep(hz, length, left, right)


def terminate():
	global toneThread
	if not toneThread:
		return
	toneThread.terminate()
	toneThread.join()
	toneThread = None

availableToneGenerators = {
	OrigTone.id: OrigTone,
	ToneGenerator.id: ToneGenerator
}
