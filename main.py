import numpy as np
from config import *
from wave_source import WaveSource
import matplotlib.pyplot as plt
from visualization import plot_wave
from animation import animate_wave

# Create grid
x = np.linspace(X_MIN, X_MAX, GRID_SIZE)
y = np.linspace(Y_MIN, Y_MAX, GRID_SIZE)

X, Y = np.meshgrid(x, y)

# Calculate wave parameters
k = 2 * np.pi / WAVELENGTH
omega = 2 * np.pi * FREQUENCY

source1 = WaveSource(x=-3, y=0, amplitude=AMPLITUDE, wavelength=WAVELENGTH, frequency=FREQUENCY)
source2 = WaveSource(x=3, y=0, amplitude=AMPLITUDE, wavelength=WAVELENGTH, frequency=FREQUENCY)

wave1 = source1.generate_wave(X, Y, TIME)
wave2 = source2.generate_wave(X, Y, TIME)

total_wave = wave1 + wave2

# Visualize the wave interference pattern
plot_wave(total_wave, "Wave Interference Pattern")


# Animate the wave interference pattern
anim = animate_wave(source1, source2, X, Y)

# Keep a reference to the animation and show the figure
plt.show()