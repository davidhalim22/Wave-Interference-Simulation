import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Grid settings
GRID_SIZE = 400

X_MIN = -10
X_MAX = 10

Y_MIN = -10
Y_MAX = 10

# Wave settings
AMPLITUDE = 1
WAVELENGTH = 2
FREQUENCY = 1

# Time
TIME = 0

# Create grid
x = np.linspace(X_MIN, X_MAX, GRID_SIZE)
y = np.linspace(Y_MIN, Y_MAX, GRID_SIZE)

X, Y = np.meshgrid(x, y)

# Calculate wave parameters
k = 2 * np.pi / WAVELENGTH
omega = 2 * np.pi * FREQUENCY

# Define sources
class WaveSource:
    def __init__(self, x, y, amplitude, phase=0):
        self.x = x
        self.y = y
        self.amplitude = amplitude
        self.phase = phase

    def calculate_distance(self, X, Y):
        r = np.sqrt((X - self.x)**2 + (Y - self.y)**2)
        return r

    def generate_wave(self, X, Y, k, omega, time):
        r = self.calculate_distance(X, Y)
        wave = self.amplitude * np.sin(k * r - omega * time + self.phase)
        return wave

