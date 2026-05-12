import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Grid
Nx, Ny = 300, 300
x = np.linspace(-10, 10, Nx)
y = np.linspace(-10, 10, Ny)
X, Y = np.meshgrid(x, y)

# Sources
source1 = (-3, 0)
source2 = (3, 0)

# Parameters
A = 1
wavelength = 2
k = 2 * np.pi / wavelength
omega = 2 * np.pi * 0.5

# Distances
R1 = np.sqrt((X - source1[0])**2 + (Y - source1[1])**2)
R2 = np.sqrt((X - source2[0])**2 + (Y - source2[1])**2)

# Avoid divide by zero
R1[R1 == 0] = 1e-6
R2[R2 == 0] = 1e-6

# Figure
fig, ax = plt.subplots(figsize=(7, 7))

Z = np.zeros_like(X)

im = ax.imshow(
    Z,
    extent=[-10, 10, -10, 10],
    origin='lower',
    cmap='RdBu',
    vmin=-2,
    vmax=2,
    animated=True
)

ax.set_title("2D Wave Interference")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Animation
def update(frame):
    t = frame * 0.05

    wave1 = A * np.sin(k * R1 - omega * t)
    wave2 = A * np.sin(k * R2 - omega * t)

    Z = wave1 + wave2

    im.set_array(Z)

    return [im]

ani = FuncAnimation(
    fig,
    update,
    frames=300,
    interval=30,
    blit=True
)

plt.show()