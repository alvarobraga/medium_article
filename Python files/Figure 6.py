'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 6.py: Plot values obtained 
             from conversion
'''

import numpy as np
from matplotlib import pyplot as plt

x = np.loadtxt("../Dataset/raw_conversion_values.txt", dtype='int')
n = np.linspace(0, 1999, 2000)
plt.figure(figsize=(30, 15))
plt.xlim(right=500)
plt.plot(n, x, color='r')
plt.show()
