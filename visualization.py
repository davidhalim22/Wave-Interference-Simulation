import matplotlib.pyplot as plt

def plot_wave(wave, title="Wave", x_min=-10, x_max=10, y_min=-10, y_max=10):
    plt.figure(figsize=(8,6))
    plt.imshow(wave, extent=(x_min, x_max, y_min, y_max), origin='lower', cmap='viridis')
    plt.colorbar(label='Amplitude')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.001)


def plot_intensity(wave, x_min=-10, x_max=10, y_min=-10, y_max=10):
    intensity = wave**2
    plt.figure(figsize=(8,6))
    plt.imshow(intensity, extent=(x_min, x_max, y_min, y_max), origin="lower", cmap="inferno")
    plt.colorbar(label="Intensity")
    plt.title("Wave Intensity Pattern")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.001)