'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 12.py: Plot current sensor output
              signal filtered in the frequency domain
'''

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq

sampling_size = 2000
'''Filter coefficients'''
a0 = .0251
a1 = .0502
a2 = .0251
b0 = 1.2491
b1 = 1.9498
b2 = -.8011

# Normalise coefficients
a0 /= b0
a1 /= b0
a2 /= b0
b1 /= b0
b2 /= b0

'''Signal not filtered'''
x = np.loadtxt("../Dataset/raw_conversion_values.txt", dtype='int')

offset = np.mean(x)
for i in range(x.shape[0]):
    x[i] -= offset

xf = fft(x)  # Apply Fast Fourier Transform to the discrete signal
# Frequency components (-Nyquist to +Nyquist)
freqs = fftfreq(sampling_size, 1/sampling_size)

'''Convert from double-sided spectra to single-sided spectra'''
idx = np.where(freqs > 0)
b = 2 * xf[idx]
positive_freqs_no_DC = freqs[idx]
# Without the DC component, the fundamental component has the highest amplitude
amplitude_50Hz_component = np.abs(b[np.argmax(np.abs(b))])
# Normalise amplitudes
normalised = 20*np.log10(np.abs(b)/amplitude_50Hz_component)

y = []
for n in range(x.shape[0]):
    if n >= 2:
        y.append((a0*x[n] + a1*x[n-1] + a2*x[n-2]
                  + b1*y[n-1] + b2*y[n-2]))
    elif n == 1:
        y.append((a0*x[n] + a1*x[n-1] + b1*y[n-1]))

    else:
        y.append(a0*x[n])

yf = fft(y)
c = 2 * yf[idx]
amplitude_50Hz_component = np.abs(c[np.argmax(np.abs(c))])
normalised_y = 20*np.log10(np.abs(c)/amplitude_50Hz_component)


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
plt.plot(positive_freqs_no_DC, normalised, 'r', label="Not filtered")
plt.plot(positive_freqs_no_DC, normalised_y, 'b', label="Filtered")
plt.legend(prop={'size': 25})
plt.show()
