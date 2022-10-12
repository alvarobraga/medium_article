'''Code to plot raw signal in the frequency domain'''

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
x = np.loadtxt("./raw_conversion_result.txt", dtype='int')

offset = np.mean(x)
for i in range(x.shape[0]):
    x[i] -= offset

y = []
for n in range(x.shape[0]):
    if n >= 2:
        y.append((a0*x[n] + a1*x[n-1] + a2*x[n-2]
                  + b1*y[n-1] + b2*y[n-2]))
    elif n == 1:
        y.append((a0*x[n] + a1*x[n-1] + b1*y[n-1]))

    else:
        y.append(a0*x[n])


setFontDict = {'fontsize': 20,
               'fontweight': "bold"}
plt.figure(figsize=(30, 8))
plt.title("Current sensor output signal - time domain",
          fontdict=setFontDict)
plt.ylabel("Amplitude", fontdict=setFontDict)
plt.xlabel("Samples", fontdict=setFontDict)
# ticks = np.linspace(0, 1000, 21)
# plt.yticks(fontsize=20)
# plt.xticks(ticks, fontsize=20)
plt.xlim(right=750)
plt.grid()
plt.plot(x, 'r', label="Not filtered")
plt.plot(y, 'b', label="Filtered")
plt.legend(loc="lower right", prop={'size': 25})
plt.show()
