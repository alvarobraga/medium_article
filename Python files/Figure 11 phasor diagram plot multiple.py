'''
Author: Alvaro Braga
email: alvaro.braga3@gmail.com
Figure 11.py: Plot phasor diagram of the transfer
              function for multiple frequencies
'''

from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

# Coefficients - transfer function
a0 = .0251
a1 = .0502
a2 = .0251
b0 = 1.2491
b1 = -1.9498
b2 = .8011

# numerator transfer function
num = np.array([a0, a1, a2])

# denominator transfer function
den = np.array([b0, b1, b2])

# Sampling frequency
fs = 2000

# Create a linear space containing ω from 0 to fs, where Δω = 1/fs
omega = np.linspace(0, 2*np.pi, fs)

# nyquist frequency
nyquist = int(fs/2)

weight_num = num[0]
weight_den = den[0]
normalised_coeff_num = num/weight_num
normalised_coeff_den = den/weight_den

# An matrix of [nyquist,2] shape receives the real and imaginary parts of each
# Z point in the Z-plane (these points are on the unit circle)
# (real in column 0 and imaginary in column 1)
Z = np.empty([nyquist, 2], dtype=float)
for i, w in enumerate(omega[:nyquist]):
    Z[i][0] = np.cos(w)  # Real part
    Z[i][1] = np.sin(w)  # Imaginary part

# Find the roots of the numerator polynomial
rootsNumPoly = np.roots(normalised_coeff_num)
rootsDenPoly = np.roots(normalised_coeff_den)

# Create a matrix to store the real and imaginary part of each zero and
# another matrix to store the real and imaginary part of each pole
zeros = np.empty([rootsNumPoly.shape[0], 2])
zeros[:, 0], zeros[:, 1] = rootsNumPoly.real, rootsNumPoly.imag
poles = np.empty([rootsDenPoly.shape[0], 2])
poles[:, 0], poles[:, 1] = rootsDenPoly.real, rootsDenPoly.imag

# int(zeros.size / zeros.shape[1]) calculates the amount of zeros present
store_distance_from_each_zero = \
    np.zeros([nyquist, int(zeros.size / zeros.shape[1]), 2])

# Calculate the distance of each Z point to each zero
for i, zero in enumerate(zeros):
    module_distance_from_each_zero = np.add(
        Z, -zero)  # (real + real),(img + img)

    # Calculate phase angle contribution of each zero
    angle_zeros = np.arctan2(module_distance_from_each_zero[:, 1],
                             module_distance_from_each_zero[:, 0])

    # Check which angles are on the third quadrant
    real_negative = np.where(module_distance_from_each_zero[:, 0] < 0)
    img_negative = np.where(module_distance_from_each_zero[:, 1] < 0)
    on_third_quadrant = np.intersect1d(real_negative, img_negative)
    # Since the function numpy.arctan2 operates within the interval [-π,π],
    # for angles on the 3rd quadrant it is necessary to add 2π,
    # so we will have only positive angles
    angle_zeros[on_third_quadrant] += 2*np.pi

    module_distance_from_each_zero = \
        np.square(module_distance_from_each_zero)  # (real)^2, (imag)^2
    module_distance_from_each_zero = \
        np.sum(module_distance_from_each_zero, axis=1)  # (real)^2 + (imag)^2
    module_distance_from_each_zero = \
        np.sqrt(module_distance_from_each_zero)  # sqrt((real)^2 + (imag)^2))

    store_distance_from_each_zero[:, i, 0] = module_distance_from_each_zero
    store_distance_from_each_zero[:, i, 1] = angle_zeros

numerator_module_transfer_function = np.zeros([nyquist, 2])

for i in range(0, nyquist):
    numerator_module_transfer_function[i, 0] = np.prod(
        store_distance_from_each_zero[i, :, 0])
    numerator_module_transfer_function[i, 0] *= weight_num
    numerator_module_transfer_function[i, 1] = np.sum(
        store_distance_from_each_zero[i, :, 1])

# -----Repeat procedure for poles-------
store_distance_from_each_pole = \
    np.zeros([nyquist, int(poles.size / poles.shape[1]), 2])

# Calculate the distance of each Z point to each pole
for i, pole in enumerate(poles):
    module_distance_from_each_pole = np.add(
        Z, -pole)  # (real + real),(img + img)

    # Calculate phase angle contribution of each pole
    angle_poles = np.arctan2(module_distance_from_each_pole[:, 1],
                             module_distance_from_each_pole[:, 0])
    # Check which angles are on the third quadrant
    real_negative = np.where(module_distance_from_each_pole[:, 0] < 0)
    img_negative = np.where(module_distance_from_each_pole[:, 1] < 0)
    on_third_quadrant = np.intersect1d(real_negative, img_negative)
    # Since the function numpy.arctan2 operates within the interval [-π,π],
    # for angles on the 3rd quadrant it is necessary to add 2π,
    # so we will have only positive angles
    angle_poles[on_third_quadrant] += 2*np.pi

    module_distance_from_each_pole = \
        np.square(module_distance_from_each_pole)  # (real)^2, (imag)^2
    module_distance_from_each_pole = \
        np.sum(module_distance_from_each_pole, axis=1)  # (real)^2 + (imag)^2
    module_distance_from_each_pole = \
        np.sqrt(module_distance_from_each_pole)  # sqrt((real)^2 + (imag)^2))

    store_distance_from_each_pole[:, i, 0] = module_distance_from_each_pole
    store_distance_from_each_pole[:, i, 1] = angle_poles

denominator_module_transfer_function = np.zeros([nyquist, 2])

for i in range(0, nyquist):
    denominator_module_transfer_function[i, 0] = \
        np.prod(store_distance_from_each_pole[i, :, 0])
    denominator_module_transfer_function[i, 0] *= weight_den
    denominator_module_transfer_function[i, 1] = \
        np.sum(store_distance_from_each_pole[i, :, 1])

# Calculate module and angle Transfer function for each ω
transfer_function = np.zeros_like(numerator_module_transfer_function)

transfer_function[:, 0] = np.divide(numerator_module_transfer_function[:, 0],
                                    denominator_module_transfer_function[:, 0])

transfer_function[:, 1] = np.subtract(numerator_module_transfer_function[:, 1],
                                      denominator_module_transfer_function[:, 1])

fig, ax = plt.subplots(figsize=(8, 8))

ax.set_xlim(-1., 1.)
ax.set_ylim(-1., 1.)
ax.set_aspect('equal')
ax.axis('off')

ax.axhline(y=0., color='black', linestyle='--', linewidth=0.8)
ax.axvline(x=0., color='black', linestyle='--', linewidth=0.8)
a = [1.0000, 0.7079, 0.3162]
for i in a:
    circle2 = patches.Circle((0., 0.), i, color='k',
                             fill=False, linestyle='--', linewidth=0.8)
    ax.add_patch(circle2)

for i in range(0, nyquist, 5):
    if i == 50:
        color = "tab:orange"
    elif i == 100:
        color = "red"
    else:
        color = "blue"

    dx = transfer_function[i, 0]*np.cos(transfer_function[i, 1])
    dy = transfer_function[i, 0]*np.sin(transfer_function[i, 1])
    ax.arrow(x=0, y=0, dx=dx, dy=dy, length_includes_head=True,
             width=0.008, color=color)

plt.show()
