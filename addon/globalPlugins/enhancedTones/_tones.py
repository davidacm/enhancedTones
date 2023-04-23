# ● _tones
# an utility to generate tones.
# Copyright (C) 2022 David CM

import addonHandler, config, math, nvwave, threading, tones
from ctypes import c_short, create_string_buffer
from io import BytesIO
from NVDAHelper import generateBeep

addonHandler.initTranslation()


availableToneGenerators = {}
def registerGenerator(*generators):
	for k in generators:
		availableToneGenerators[k.id] = k


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


class AbstractGenerator:
	name = _("Sine Generator")
	id = 'SineGenerator'
	def __init__(self, rate=44100):
		# parameters
		self.bytes = 2
		self.rate = rate
		self.freq = 1000
		# constants
		self._MAX_AMPLITUDE = int(2 ** (self.bytes * 8) / 2) - 1
		self._MAX_SWEEP = 1000
		# generator state
		self.isGenerating = False
		self._curFreq = 1000
		self._gen = self.sampleGenerator()
		self._stepFreq = 0
		self._numSamples = 0
		self._curChunk = 0
		self._ampL = 0
		self._ampR = 0
		self._sweepCount = 0

	def sampleGenerator(self):
		""" this method is used to generate each sample according to the wave features.
		it's a generator tat yields infinite wave samples following the waveform specs.
		you must update the generation data if the _curFreq is updated.
		the sample will be multiplied by the amplitude for each channel (left and right)
		"""
		raise NotImplementedError()

	def normalizeSample(self, sample):
		ret = int(sample * self._MAX_AMPLITUDE)
		if ret < -self._MAX_AMPLITUDE:
			ret = -self._MAX_AMPLITUDE
		elif ret > self._MAX_AMPLITUDE:
			ret = self._MAX_AMPLITUDE
		return c_short(ret)

	def setToneVals(self, freq, length, ampL=0.5, ampR=0.5):
		self._numSamples = int(length *self.rate)
		self._curChunk = 0
		self._ampL = ampL
		self._ampR = ampR
		if not self.isGenerating or freq == 0:
			self.freq = freq
			self._curFreq = freq
			self._gen = self.sampleGenerator()
		elif freq != self.freq:
			self._sweepCount = min(self._MAX_SWEEP, self._numSamples)
			self._stepFreq = ((freq -self._curFreq) / self._sweepCount)
			self.freq = freq

	def nextChunk(self, size=4000):
		while self._curChunk < self._numSamples:
			self.isGenerating = True
			rest = self._numSamples -self._curChunk
			# to avoid very small chunks at the end. Append the last part if is less than size*2
			if rest < size*2:
				size = rest
			self._curChunk += size
			samples = BytesIO()
			for i in range(size):
				w = next(self._gen)
				if self._sweepCount > 0:
					self._curFreq += self._stepFreq
					self._sweepCount -= 1
				else:
					self._curFreq = self.freq
				samples.write(self.normalizeSample(self._ampL * w))
				samples.write(self.normalizeSample(self._ampR * w))
			yield samples.getvalue()
		self.isGenerating = False

	def startGenerate(self, hz, length, left, right):
		self.setToneVals(hz, length/1000.0, left/100.0, right/100.0)


class SineGenerator(AbstractGenerator):
	name = _("Sine Generator")
	id = 'SineGenerator'
	def __init__(self, rate=44100):
		super().__init__(rate)
		self._PHASE_BASE = float(2 *math.pi /self.rate)

	def sampleGenerator(self):
		freq = self._curFreq
		phaseAcc = 0.0
		delta = self._PHASE_BASE * freq
		i=0
		while True:
			if i == self.rate:
				i=0
				phaseAcc = 0.0
			if self._curFreq != freq:
				freq = self._curFreq
				delta = self._PHASE_BASE * freq
			yield math.sin(phaseAcc)
			phaseAcc += delta
			i+=1

# the following generators need improvements.

class SquareGenerator(AbstractGenerator):
	name = _("Square Generator")
	id = 'SquareGenerator'

	def sampleGenerator(self):
		freq = points = split = 0
		def updateValues():
			nonlocal freq, points, split
			freq = self._curFreq
			points = self.rate // freq
			split = points / 2
		updateValues()
		while True:
			i = 0
			while i < split:
				if self._curFreq != freq:
					updateValues()
				yield 1
				i+=1
			while i < points:
				if self._curFreq != freq:
					updateValues()
				yield -1
				i+=1


class SawtoothGenerator(AbstractGenerator):
	name = _("Sawtooth Generator")
	id = 'SawtoothGenerator'

	def sampleGenerator(self):
		freq = points = delta = 0
		def updateValues():
			nonlocal freq, points, delta
			freq = self._curFreq
			points = int(self.rate // freq)
			delta = 2/points
		updateValues()
		while True:
			i = 0
			while i < points:
				if self._curFreq != freq:
					updateValues()
				yield (delta*i) -1
				i+=1

class TriangleGenerator(AbstractGenerator):
	name = _("Triangle Generator")
	id = 'TriangleGenerator'

	def sampleGenerator(self):
		freq = points = delta = 0
		def updateValues():
			nonlocal freq, points, delta
			freq = self._curFreq
			points = int(self.rate // freq)
			delta = 2/points
		updateValues()
		while True:
			i = 0
			while i < points:
				if self._curFreq != freq:
					updateValues()
				yield abs((delta*i) -1)
				i+=1


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
		self.tonePlayer = nvwave.WavePlayer(2, self.hz, 16, outputDevice=outputDevice, wantDucking=False)

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

registerGenerator(OrigTone, SineGenerator, SawtoothGenerator, SquareGenerator, TriangleGenerator)
