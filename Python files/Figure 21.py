'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 21.py: Plot of the step response
              for gain=1.0 and gain=0.915
'''

from matplotlib import pyplot as plt
import numpy as np

#Coefficients - filter
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

step = np.ones((2000,))


def filter(input, gain):
    output = []
    coeff_num = np.array([a0, a1, a2])
    coeff_num *= gain

    for i in range(len(input)):
        if i >= 2:
            output.append((coeff_num[0]*input[i] + coeff_num[1]*input[i-1] + coeff_num[2]*input[i-2]
                           + b1*output[i-1] + b2*output[i-2]))
        elif i == 1:
            output.append(
                (coeff_num[0]*input[i] + coeff_num[1]*input[i-1] + b1*output[i-1]))

        else:
            output.append(coeff_num[0]*input[i])

    return output


y1 = filter(step, 1.0)
y2 = filter(step, .915)


setFontDict = {'fontsize': 20,
               'fontweight': "bold"}
plt.figure(figsize=(30, 8))
plt.title("Step Response - simulation",
          fontdict=setFontDict)
plt.yticks(weight="bold", fontsize=20)
plt.ylabel("Amplitude", fontdict=setFontDict)
plt.xlabel("Samples", fontdict=setFontDict)
plt.ylim(top=1.2)
plt.xlim(right=80)
plt.plot(step, 'b', linewidth=5.0)
plt.plot(y1, 'r', label="Step Reponse - gain = 1.0", linewidth=5.0)
plt.plot(y2, 'orange', label="Step Reponse - gain = 0.915",
         linewidth=5.0, linestyle="--")
plt.legend(prop={'size': 25})
plt.show()
