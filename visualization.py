import matplotlib.pyplot as plt

from config import *

def plot_wave(wave, title="Wave"):
    plt.figure(figsize=(8,6))
    plt.imshow(wave, extent=(X_MIN, X_MAX, Y_MIN, Y_MAX), origin='lower', cmap='viridis')
    
    plt.colorbar(label='Amplitude')
    
    plt.title(title)
    
    plt.xlabel('X')
    plt.ylabel('Y')
    
    plt.tight_layout()
    plt.show()



def plot_intensity(wave):
    intensity = wave**2
    plt.figure(figsize=(8,6))

    plt.imshow(intensity, extent=(X_MIN, X_MAX, Y_MIN, Y_MAX), origin="lower", cmap="inferno")

    plt.colorbar(label="Intensity")
    plt.title("Wave Intensity Pattern")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.tight_layout()
    plt.show()