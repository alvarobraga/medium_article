'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 12.py: Plot filter response, in the 
              time domain, for 3 different
              frequencies
'''

from matplotlib import pyplot as plt
import numpy as np

# Filter coefficients
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


fs = 2000
freqs = [50, 100, 250]
number_of_cycles = 5
span_in_seconds = [number_of_cycles * 1/i for i in freqs]
number_of_samples = [int(number_of_cycles * fs/i) for i in freqs]

setFontDict = {'fontsize': 10,
               'fontweight': "bold"}

for i, f in enumerate(freqs):
    n = np.linspace(0, span_in_seconds[i], number_of_samples[i])
    x = np.sin(2*np.pi*f*n)
    y = []
    for i in range(len(x)):
        if i >= 2:
            y.append((a0*x[i] + a1*x[i-1] + a2*x[i-2]
                      + b1*y[i-1] + b2*y[i-2]))
        elif i == 1:
            y.append((a0*x[i] + a1*x[i-1] + b1*y[i-1]))

        else:
            y.append(a0*x[i])

    plt.figure(figsize=(15, 4))
    plt.title(f"Filter response for {f}Hz", fontdict=setFontDict)
    plt.ylabel("Amplitude", fontdict=setFontDict)
    plt.xlabel("Samples", fontdict=setFontDict)
    plt.plot(n, x, linestyle="dashed", label="Original signal")
    plt.plot(n, y, label="Filter output")
    plt.legend()
    plt.show()
