import numpy as np
import matplotlib.pyplot as plt
from config import *
from wave_source import WaveSource
from visualization import (plot_wave, plot_intensity)
from animation import (animate_interference)
from analysis import (calculate_energy, calculate_statistics, measure_runtime, start_memory_tracking, stop_memory_tracking)
from report_generator import (generate_report)

# Start memory tracking
start_memory_tracking()

# Create grid
x = np.linspace(X_MIN, X_MAX, GRID_SIZE)
y = np.linspace(Y_MIN, Y_MAX, GRID_SIZE)

X, Y = np.meshgrid(x, y)

# Calculate wave parameters
k = 2 * np.pi / WAVELENGTH
omega = 2 * np.pi * FREQUENCY

source1 = WaveSource(x=-3, y=0, amplitude=AMPLITUDE, wavelength=WAVELENGTH, frequency=FREQUENCY)
source2 = WaveSource(x=3, y=0, amplitude=AMPLITUDE, wavelength=WAVELENGTH, frequency=FREQUENCY, phase=PHASE_DIFFERENCE)

wave1 = measure_runtime(source1.generate_wave, X, Y, TIME)
wave2 = measure_runtime(source2.generate_wave, X, Y, TIME)

total_wave = wave1 + wave2

energy = calculate_energy(total_wave)
statistics = calculate_statistics(total_wave)

print(f"""
Energy: {energy:.4f}
Mean: {statistics['mean']:.4f}
Standard Deviation: {statistics['std']:.4f}
Max Amplitude: {statistics['max']:.4f}
      """)

print(generate_report(total_wave))

# Visualize the wave interference pattern
plot_wave(total_wave, "Wave Interference Pattern")
plot_intensity(total_wave)

# Animate the wave interference pattern
animation = animate_interference(source1, source2, X, Y)

# Keep a reference to the animation and show the figure
stop_memory_tracking()
plt.show()