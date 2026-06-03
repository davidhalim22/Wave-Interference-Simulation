import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from config import (GRID_SIZE, X_MIN, X_MAX, Y_MIN, Y_MAX)

def animate_wave(source1, source2, X, Y):
    fig, ax = plt.subplots(figsize=(8,6))
    
    image = ax.imshow(np.zeros((GRID_SIZE, GRID_SIZE)), extent=(X_MIN, X_MAX, Y_MIN, Y_MAX), cmap='viridis', animated=True)
    
    def update(frame):
        time = frame * 0.1

        wave1 = source1.generate_wave(X, Y, time)
        wave2 = source2.generate_wave(X, Y, time)

        total_wave = wave1 + wave2

        image.set_array(total_wave)

        return [image]

    animation = FuncAnimation(fig, update, frames=100, interval=50)

    ax.set_title("Wave Interference Animation")

    # Return the animation object so the caller can keep a reference
    return animation