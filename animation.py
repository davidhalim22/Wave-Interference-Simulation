import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from config import *



def animate_interference(source1, source2, X, Y):
    fig, ax = plt.subplots(figsize=(8,6))
    image = ax.imshow(np.zeros((GRID_SIZE, GRID_SIZE)), extent=(X_MIN, X_MAX, Y_MIN, Y_MAX), origin='lower', cmap='viridis', animated=True)
    fig.colorbar(image, ax=ax, label="Amplitude")
    
    # Plot the sources
    ax.scatter([source1.x, source2.x], [source1.y, source2.y], color="red", s=100)

    time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, color="white")
    
    ax.set_title("Wave Interference Animation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    
    def update(frame):
        time = frame * 0.05

        wave1 = source1.generate_wave(X, Y, time)
        wave2 = source2.generate_wave(X, Y, time)

        total_wave = wave1 + wave2
        
        if USE_INTENSITY:
            total_wave = total_wave**2

        image.set_array(total_wave)
        image.set_clim(vmin=np.min(total_wave), vmax=np.max(total_wave))
        time_text.set_text(f"Time: {time:.2f}s")

        return [image], time_text

    animation = FuncAnimation(fig, update, frames=FRAMES, interval=INTERVAL, blit=False)
    return animation
