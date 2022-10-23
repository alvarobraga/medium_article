'''Code to plot raw signal in the frequency domain'''

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq

sampling_size = 2000

x = np.loadtxt("./raw_conversion_result.txt", dtype='int')

'''Remove Offset'''
offset = np.mean(x)
for i in range(x.shape[0]):
    x[i] -= offset


xf = fft(x)  # Apply Fast Fourier Transform to the discrete signal
# Frequency components (-Nyquist to +Nyquist)
freqs = fftfreq(sampling_size, 1/sampling_size)

'''Convert from double-sided spectra to single-sided spectra'''
idx = np.where(freqs >= 0)
b = 2 * xf[idx]
positive_freqs_no_DC = freqs[idx]
# Without the DC component, the fundamental component has the highest amplitude
amplitude_50Hz_component = np.abs(b[np.argmax(np.abs(b))])
# Normalise amplitudes, so we can compare all the components with the fundamental
normalised = 20*np.log10(np.abs(b)/amplitude_50Hz_component)

setFontDict = {'fontsize': 20,
               'fontweight': "bold"}
plt.figure(figsize=(30, 8))
plt.title("Current sensor output signal - frequency domain",
          fontdict=setFontDict)
plt.ylabel("Normalised amplitude - dB", fontdict=setFontDict)
plt.xlabel("Frequency - Hz", fontdict=setFontDict)
ticks = np.linspace(0, 1000, 21)
plt.yticks(fontsize=20)
plt.xticks(ticks, fontsize=20)
plt.grid()
plt.plot(positive_freqs_no_DC, normalised, 'r')
plt.show()
