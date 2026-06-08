import numpy as np

# Define sources
class WaveSource:
    def __init__(self, x, y, amplitude, wavelength, frequency, phase=0):
        self.x = x
        self.y = y
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.frequency = frequency
        self.phase = phase
        
        self.k = 2 * np.pi / wavelength
        self.omega = 2 * np.pi * frequency

    def calculate_distance(self, X, Y):
        r = np.sqrt((X - self.x)**2 + (Y - self.y)**2)
        return r

    def generate_wave(self, X, Y, time):
        r = self.calculate_distance(X, Y)
        
        # Avoid divide by zero
        r = np.where(r < 0.1, 0.1, r)
        
        # Calculate wave using the formula: A * sin(k*r - omega*t + phase) / sqrt(r)
        wave = self.amplitude * np.sin(self.k * r - self.omega * time + self.phase) / np.sqrt(r)
        return wave

