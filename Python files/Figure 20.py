'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 20.py: Plot current box plot of
              the distribution of RMS values
              of filtered and not filtered signals
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rms_squared_filtered_values = np.loadtxt(
    "../Dataset/rms_squared_filtered_values.txt", dtype=float)
rms_squared_not_filtered_values = np.loadtxt(
    "../Dataset/rms_squared_not_filtered_values.txt", dtype=float)

rms_squared_filtered_values = np.sqrt(
    rms_squared_filtered_values) / 4096 * 3.3 * 15
rms_squared_not_filtered_values = np.sqrt(
    rms_squared_not_filtered_values) / 4096 * 3.3 * 15

rms_squared_filtered_values_normalised = rms_squared_filtered_values / \
    np.mean(rms_squared_filtered_values)
rms_squared_filtered_values_normalised -= 1

rms_squared_not_filtered_values_normalised = rms_squared_not_filtered_values / \
    np.mean(rms_squared_not_filtered_values)
rms_squared_not_filtered_values_normalised -= 1

setFontDict = {'fontsize': 20,
               'fontweight': "bold"}

data_dict = {'Filtered': rms_squared_filtered_values_normalised,
             'Not filtered': rms_squared_not_filtered_values_normalised}
fig, ax = plt.subplots(figsize=(15, 8))
ax.boxplot(data_dict.values(), widths=0.9)
ax.set_xticklabels(data_dict.keys(), weight="bold", fontsize=20)
plt.axhline(0.00475, color='red', linestyle='--', linewidth=.7)
plt.axhline(-0.00495, color='red', linestyle='--', linewidth=.7)

ax.text(.55, .003, 'Median = {}'.format(np.round(np.median(
    rms_squared_filtered_values), 4)), fontdict=setFontDict, color="blue")
ax.text(.55, .0025, 'Mean = {}'.format(np.round(
    np.mean(rms_squared_filtered_values), 4)), fontdict=setFontDict, color="blue")
ax.text(.55, .0020, 'IQR = {}'.format(np.round(stats.iqr(
    rms_squared_filtered_values), 4)), fontdict=setFontDict, color="blue")

ax.text(1.55, .003, 'Median = {}'.format(np.round(np.median(
    rms_squared_not_filtered_values), 4)), fontdict=setFontDict, color="red")
ax.text(1.55, .0025, 'Mean = {}'.format(np.round(np.mean(
    rms_squared_not_filtered_values), 4)), fontdict=setFontDict, color="red")
ax.text(1.55, .0020, 'IQR = {}'.format(np.round(stats.iqr(
    rms_squared_not_filtered_values), 4)), fontdict=setFontDict, color="red")

plt.show()
