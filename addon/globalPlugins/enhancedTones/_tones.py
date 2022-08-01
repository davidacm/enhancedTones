# ● _tones
# an utility to generate tones.
# Copyright (C) 2022 David CM


import config, math, nvwave, struct, threading, tones
from itertools import cycle
from NVDAHelper import generateBeep
from ctypes import create_string_buffer

class OrigTone:
	name = "Tonos originales"
	def __init__(self, hz=None):
		pass

	def generate(self, hz,length,left,right):
		buf=create_string_buffer(generateBeep(None,hz,length,left,right))
		generateBeep(buf,hz,length,left,right)
		return buf.raw


class ToneGenerator:
	name = "tonos personalizados"
	def __init__(self, rate=44100):
		self.bytes = 2
		self.maxAmplitude = int((2 ** (self.bytes * 8)) / 2) - 1
		self.rate = rate

	def sine_wave(self, freq):
		cs = float(2 *math.pi *freq /float(self.rate))
		for i in cycle(range(self.rate)):
			yield float(math.sin(cs *i))

	def generateTone(self, freq, time, ampL=0.5, ampR=0.5):
		numsamples = int(time *self.rate)
		samples = []
		gen = self.sine_wave(freq)
		for i in range(numsamples):
			w = next(gen)
			samples.append(ampL * w)
			samples.append(ampR * w)
		return samples

	def packSample(self, sample):
		ret = int(sample * self.maxAmplitude)
		if ret < -self.maxAmplitude: ret = -self.maxAmplitude
		elif ret > self.maxAmplitude: ret = self.maxAmplitude
		return struct.pack("h", ret)

	def serialize(self, samples):
		return bytes(b'').join([bytes(self.packSample(k)) for k in samples])

	def generate(self, hz, length, left, right):
		return self.serialize(self.generateTone(hz, length/1000.0, left/100.0, right/100.0))


class PlayerTone(threading.Thread):
	def __init__(self, toneGen, hz):
		super().__init__(target=self.run)
		self.tonePlayer = None
		self.hz = hz
		self.samples = b""
		self.values = None
		self.waitBeep = threading.Event()
		self.stopFlag = False
		self.chunkSize=8820
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
			self.samples = self.toneGen.generate(hz,length,left,right)
			for i in range(0, len(self.samples), self.chunkSize):
				if len(self.samples)-i < self.chunkSize*2:
					self.tonePlayer.feed(self.samples[i:len(self.samples)])
					break
				else: self.tonePlayer.feed(self.samples[i:i+self.chunkSize])
				if self.waitBeep.is_set(): break
		self.tonePlayer.close()
		self.tonePlayer= None

	def beep(self, hz,length,left, right):
		print("tratando beeping")
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

availableGenerators = [OrigTone, ToneGenerator]
