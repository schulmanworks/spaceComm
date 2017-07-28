#/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, misc, io
import scipy.io.wavfile
import scipy.signal
from scipy.fftpack import fft
import wave
import pdb
def dbmToLin(dbm):
    return 10**(dbm/10)
# b)
x = np.arange(dbmToLin(-5), dbmToLin(10), .01)
 # this is python's q-function. See here
 #https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.stats.norm.html
y = scipy.stats.norm.sf(np.sqrt(2*x))
plt.plot(x,y)
plt.yscale("log")
plt.title("BPSK BER")
plt.xlabel("CNR (dB)")
plt.ylabel("Probability of error")
plt.show()

# c)
y = scipy.stats.norm.sf(np.sqrt(x))
plt.plot(x,y)
plt.yscale("log")
plt.title("QPSK BER")
plt.xlabel("CNR (dB)")
plt.ylabel("Probability of error")
plt.show()
# Yes, it is a good assumption
