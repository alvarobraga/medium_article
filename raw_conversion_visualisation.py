'''Code to plot raw data'''

import numpy as np
from matplotlib import pyplot as plt

x = np.loadtxt("./raw_conversion_result.txt", dtype='int')
n = np.linspace(0, 1999, 2000)
plt.figure(figsize=(30, 15))
# plt.xlim(right=500)
plt.plot(n, x, color='r')
plt.show()
