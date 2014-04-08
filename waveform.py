# -*- coding: utf-8 -*-

from copy import deepcopy
from numpy import *
from scipy.signal import butter, lfilter

class Waveform:
    """Class for waveforms that saves important data like the sample
    rate and nyquist frequency along with the samples."""
    def __init__(self, duration, samplerate):
        self.samplerate = float(samplerate)
        self.sampleinterval = 1. / self.samplerate
        self.nyquist = .5*samplerate
        self.time = arange(0.0, float(duration), self.sampleinterval)

    def add_offset(self, offset):
        self.samples += offset
        return self

    def add_uniform_noise(self, a):
        "Adds white noise with amplitude *a* to the signal"
        self.samples += random.uniform(-a, a, self.samples.shape[0])
        return self

    def add_gauss_noise(self, a):
        "Adds white noise with amplitude *a* to the signal"
        self.samples += random.normal(0, a, self.samples.shape[0])
        return self

    def __lfilter(self, b, a):
        self.samples = lfilter(b, a, self.samples)
        return self

    def bandpass(self, low, high, order):
        """Apply Butterworth bandpass filter with corner frequencies
        *low* and *high* to signal"""
        b, a = butter(order, (low/self.nyquist, high/self.nyquist), btype='band')
        return self.__lfilter(b, a)

    def lowpass(self, cutoff, order):
        """Apply Butterworth lowpass filter"""
        b, a = butter(order, cutoff/self.nyquist, btype='low')
        return self.__lfilter(b, a)

    def highpass(self, cutoff, order):
        """Apply Butterworth lowpass filter"""
        b, a = butter(order, cutoff/self.nyquist, btype='high')
        return self.__lfilter(b, a)

    def copy(self):
        return deepcopy(self)

    def to_TWaveform(self):
        """Create ROOT/OrcaROOT TWaveform object from waveform,
        which can for example be used for fitting."""
        import ROOT
        import pathfinder
        ROOT.gSystem.Load(pathfinder.libWaveWaveBase)
        w = ROOT.TDoubleWaveform(self.samples, len(self.samples))
        w.SetSamplingFreq(self.samplerate*ROOT.CLHEP.second)
        return w

if __name__ == '__main__':
    from decayingsine import DecayingSine
    s = DecayingSine(7, 2, 10, 1e5)
    s.add_gauss_noise(.1)
    w = s.to_TWaveform()
    w.GimmeHist().Draw()
    raw_input("Press enter to continue...")
