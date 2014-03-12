# -*- coding: utf-8 -*-

from numpy import *
from waveform import Waveform

class DecayingSine(Waveform):
    """Represents a decaying sinusoidal signal."""

    def __init__(self, freq, tau, T, samplerate, t0=None, phi=0):
       """Initialize signal without any noise.

       Arguments:
        * freq is the frequency of the signal in hertz
        * tau is the decay constant in seconds
        * T is the length of the signal in seconds
        * samplerate in Hz
        * t0 is the time the signal starts
        * dphi is the phase of the signal, 0 means cosine
        """

       Waveform.__init__(self, T, samplerate)

       self.samples = cos(2*pi*freq*self.time)*exp(-self.time/tau)

       if t0:
           self.samples = hstack((zeros(t0/selg.sampleinterval), self.samples))[:len(self.samples)]

if __name__ == '__main__':
    from pylab import *

    s = DecayingSine(7, 2, 10, 1e5)

    subplot(411)
    title("Without noise")
    plot(s.time, s.samples)
    subplot(412)
    title("White noised")
    plot(s.time, s.add_noise(.2).samples)
    subplot(413)
    title("Bandpass filtered")
    plot(s.time, s.copy().bandpass(3, 11, 2).samples)
    subplot(414)
    title("Lowpass filtered")
    plot(s.time, s.copy().lowpass(1e3, 2).samples)

    show()
