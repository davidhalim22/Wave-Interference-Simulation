import matplotlib.pyplot as plt

from config import (X_MIN, X_MAX, Y_MIN, Y_MAX)

def plot_wave(wave, title):
    plt.figure(figsize=(8,6))
    plt.imshow(wave, extent=(X_MIN, X_MAX, Y_MIN, Y_MAX),  cmap='viridis')
    
    plt.colorbar(label='Amplitude')
    
    plt.title(title)
    
    plt.xlabel('X')
    plt.ylabel('Y')
    
    plt.show()