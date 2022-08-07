# ● _tones
# an utility to generate tones.
# Copyright (C) 2022 David CM

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
		self.samples = buf.raw
		self.curChunk = 0

	def nextChunk(self, size):
		numSamples = len(self.samples)
		while self.curChunk < numSamples:
			size = min(size, numSamples -self.curChunk)
			if size <1:
				return
			samples = self.samples[self.curChunk:self.curChunk + size]
			self.curChunk += size
			yield samples

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

	def nextChunk(self, size):
		while self.curChunk < self.numSamples:
			size = min(size, self.numSamples -self.curChunk)
			if size <1:
				return
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
		self.chunkSize = 4410
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
			for data in self.toneGen.nextChunk(self.chunkSize):
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


def beep(hz,length,left=50,right=50):
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
