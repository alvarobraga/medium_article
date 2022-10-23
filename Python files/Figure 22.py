'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 22.py: Plot histogram of the 
              RMS values forr gain=0.915
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rms_squared_filtered_values = np.loadtxt(
    "../Dataset/rms_squared_filtered_values_gain_0.915.txt", dtype=float)
rms_squared_filtered_values = np.sqrt(rms_squared_filtered_values)
rms_squared_filtered_values /= 4096.
rms_squared_filtered_values *= 3.3*15
bins = 50
setFontDict = {'fontsize': 20,
               'fontweight': "bold"}
plt.figure(figsize=(30, 8))
plt.hist(rms_squared_filtered_values, bins=bins, color="red")
# plt.axvline(x=np.mean(rms_squared_filtered_values), color='black', linestyle='--', linewidth=2.)
# plt.axvline(x=np.median(rms_squared_filtered_values), color='green', linestyle='--', linewidth=2.)
plt.title("Irms - filtered values with gain equals to 0.915",
          fontdict=setFontDict)
plt.text(2.21, 28, 'Mean = {}'.format(
    np.round(np.mean(rms_squared_filtered_values), 4)), weight="bold", fontsize=20)
plt.text(2.21, 26.5, 'Median = {}'.format(np.round(
    np.median(rms_squared_filtered_values), 4)), weight="bold", fontsize=20)
plt.text(2.21, 25, 'IQR = {}'.format(np.round(
    stats.iqr(rms_squared_filtered_values), 4)), weight="bold", fontsize=20)
plt.xticks(weight="bold", fontsize=20)
plt.yticks(weight="bold", fontsize=20)
plt.show()
