#/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, misc, io
import scipy.io.wavfile
import scipy.signal
from scipy.fftpack import fft
import wave
import pdb

# shamelessly stolen from HW 6 problem 1


def plotThis(x, y, title=""):
    plt.plot(x, y)
    plt.title(title)
    plt.show()


def pltFFT(inSamples, period, title=""):
    fourier = fft(inSamples)
    numSamples = len(inSamples)
    freqAxis = np.linspace(0.0, 1.0 / (2.0 * period), numSamples // 2)
    # freq = np.fft.fftfreq(numSamples, d=period)
    # freqAxis = np.arange(len(fourier)) / period
    plt.plot(freqAxis, 2.0 / numSamples * np.abs(fourier[0:numSamples // 2]))
    plt.title(title)
    plt.show()  # We see the center freq is 15KHz


# technically for b, necessary for a
nyq_rate1, samples1 = scipy.io.wavfile.read("audio_file1.wav")
nyq_rate2, samples2 = scipy.io.wavfile.read("audio_file2.wav")

nyq_rate1 = float(nyq_rate1)
period1 = 1 / nyq_rate1

nyq_rate2 = float(nyq_rate2)
period2 = 1 / nyq_rate2

max_nyq = max(nyq_rate1, nyq_rate2)
min_nyq = min(nyq_rate1, nyq_rate2)

aver_nyq = np.mean((nyq_rate1, nyq_rate2))
min_period = min(period1, period2)
# a)
bpf = scipy.signal.firwin(numtaps=61, cutoff=[1, 300, 3400],
                          nyq=max_nyq)
w, h = scipy.signal.freqz(bpf)
# rescale the normalized w output so it looks better when graphing
# scipy normalizes the output axis of the filter for whatever reason
# plotThis(w * 3400*2, abs(h), "Frequency response of filter")

# b)
filtered1 = scipy.signal.lfilter(bpf, [1.0], samples1)
filtered2 = scipy.signal.lfilter(bpf, [1.0], samples2)
pltFFT(filtered1, period1, "FFT of signal 1 filtered")
scipy.io.wavfile.write("orig_filt1.wave", nyq_rate1, filtered1)
scipy.io.wavfile.write("orig_filt2.wave", nyq_rate2, filtered2)
# pltFFT(filtered2, period2,"FFT of signal 2 filtered")

# c)
t1 = np.arange(0, len(filtered1) * period1, period1)
filtered1Shift = filtered1 * np.cos(2 * np.pi * 10e3 * t1)
# pltFFT(filtered1Shift, period1, "FFT of shifted signal 1")

t2 = np.arange(0, len(filtered2) * period2, period2)
filtered2Shift = filtered2 * np.cos(2 * np.pi * 18e3 * t2)
# pltFFT(filtered2Shift, period2, "FFT of shifted signal 2")

diff = len(filtered2Shift) - len(filtered1Shift)
filtered1Shift = np.pad(filtered1Shift, (0, diff),
                        'constant', constant_values=(0,))

mux = filtered2Shift + filtered1Shift #filtered2Shift +
# fc = 14e3 * 2
# Tc = 1 / fc
# Plot FFT doesn't work well for mux'd signals since there is no longer a
# definitivie nyquist rate here.
# pltFFT(abs(mux), Tc, "FFT of mux'd signal")

# d)
noise = np.random.normal(0, 0.01, size=len(mux))
No = 2 * np.var(noise)
print "No = ", No
# pltFFT(noise, Tc, "FFT of noise with No = %f" % No)

muxPlusNoise = mux #+ noise
# pltFFT(muxPlusNoise, Tc, "FFT of mux + noise")

# e)
def downFreq(center, muxPlusNoise, period, bpf):
    filterBW = (3400-300)
    bpfHighFreq = scipy.signal.firwin(numtaps=61, cutoff=[1, center-filterBW, center+filterBW],
                              nyq=2 / period)
    demux_filtered = scipy.signal.lfilter(bpfHighFreq, [1.0], muxPlusNoise)
    t_demux = np.arange(0, len(demux_filtered) * period, period)

    # The fact that multiplying by a negative frequency here works just
    # blows my damn mind. I have finally risen from a lowly undergrad
    # to a wizard with the power of pure black magic.
    demux_stepDown = demux_filtered * np.cos(2 * np.pi * (-1*center) * t_demux)

    return scipy.signal.lfilter(bpf, [1.0], demux_stepDown)

demux_stepDown1_filt = downFreq(10e3, muxPlusNoise, period1, bpf)
demux_stepDown2_filt = downFreq(18e3, muxPlusNoise, period2, bpf)
pltFFT(demux_stepDown1_filt, 1/nyq_rate1, "Demux filtered 1")
scipy.io.wavfile.write("audio_fil1_out.wave", nyq_rate1, demux_stepDown1_filt)
scipy.io.wavfile.write("audio_fil2_out.wave", nyq_rate2, demux_stepDown2_filt)
