#/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, misc, io
import scipy.io.wavfile
import scipy.signal
from scipy.fftpack import fft
import wave
import pdb
import sounddevice as sd

# problem 1 part a
nyq_rate, samples = scipy.io.wavfile.read("modulated_signal.wav")
period = 1 / float(nyq_rate)
numSamples = len(samples)
sampleTimes = np.arange(0, numSamples, 1) * period
plt.plot(sampleTimes, samples)
plt.title("Initial signal over time")
plt.show()

# problem 1 part b


def pltFFT(inSamples, title=""):
    fourier = fft(inSamples)
    numSamples = len(inSamples)
    freqAxis = np.linspace(0.0, 1.0 / (2.0 * period), numSamples // 2)
    # freq = np.fft.fftfreq(numSamples, d=period)
    # freqAxis = np.arange(len(fourier)) / period
    plt.plot(freqAxis, 2.0 / numSamples * np.abs(fourier[0:numSamples // 2]))
    plt.title(title)
    plt.show()  # We see the center freq is 15KHz
pltFFT(samples, title="FFT of initial signal")


# problem 1 part c
FIR = scipy.signal.firwin(31, .3 * np.pi)

w, h = scipy.signal.freqz(FIR)
plt.plot(w, abs(h))  # 20*np.log10(abs(h)))\
plt.title("Frequency response of filter")
plt.show()

# problem 1 part d
fc = 15000
sinWave = np.sin(2 * np.pi * fc * sampleTimes)
cosWave = np.cos(2 * np.pi * fc * sampleTimes)

inPhase = samples * sinWave
quadrature = samples * cosWave

inPhase = scipy.signal.lfilter(FIR, [1.0], inPhase)
quadrature = scipy.signal.lfilter(FIR, [1.0], quadrature)

# output = np.convolve(samples, FIR)
sampleTimes = np.arange(0, len(inPhase), 1) / period
plt.plot(sampleTimes, inPhase)
plt.title("In phase signal over time")
plt.show()

sampleTimes = np.arange(0, len(quadrature), 1) / period
plt.plot(sampleTimes, quadrature)
plt.title("Quadrature signal over time")
plt.show()

# His house is blue
scipy.io.wavfile.write("inphase.wave", nyq_rate, inPhase)
# his favorite color is green
scipy.io.wavfile.write("quad.wave", nyq_rate, quadrature)

pltFFT(inPhase, title="FFT of in phase signal")
pltFFT(quadrature, title="FFT of quadrature signal")
