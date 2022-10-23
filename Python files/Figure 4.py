'''Code to generate plots in Fig. 4'''

from matplotlib import pyplot as plt
import numpy as np

f = 50  # Sine wave frequency
T = 1/50  # Sine wave period
number_of_cycles = 5  # Number of cycles to be plotted
span_in_seconds = number_of_cycles * T
t = np.linspace(0, span_in_seconds, 10000)
sine_wave = np.sin(2*np.pi*f*t)
myRange = [i for i in range(50, 1050, 100)]
myRange[1] = 100

for i in myRange:
    fs = i
    # Calculate number of samples based on the number of cycles
    number_of_samples = int(number_of_cycles * fs/f)
    n = np.linspace(0, span_in_seconds, number_of_samples)
    samples = np.sin(2*np.pi*f*n)
    plt.figure(figsize=(8, 8))
    plt.title(f"Sample frequency = {fs}Hz")
    plt.plot(t, sine_wave, 'r', label="Sine wave", linestyle='dashed')
    plt.stem(n, samples, label="Samples", use_line_collection=True)
    plt.legend(loc="upper right")
    plt.show()
