import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Setup the 2D grid
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

# 2. Wave parameters
k = 2.0  # Wave number (2*pi / wavelength)
w = 5.0  # Angular frequency
A = 1.0  # Amplitude

# 3. Define the two source positions
source1 = (-3, 0)
source2 = (3, 0)

# Calculate the distance from each point on the grid to the sources
R1 = np.sqrt((X - source1[0])**2 + (Y - source1[1])**2)
R2 = np.sqrt((X - source2[0])**2 + (Y - source2[1])**2)

# 4. Initialize the plot
fig, ax = plt.subplots(figsize=(8, 6))

# Calculate initial wave state (t=0)
Z = A * np.sin(k * R1) + A * np.sin(k * R2)

# Create a heatmap plot using a Red-Blue colormap
cax = ax.imshow(Z, extent=[-10, 10, -10, 10], origin='lower', cmap='RdBu', vmin=-2, vmax=2)
fig.colorbar(cax, label='Amplitude')
ax.set_title('2D Wave Interference')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# 5. Define the animation function
def animate(t):
    # Scale time to slow down the animation slightly
    time = t * 0.1
    # Calculate superposition of both waves at current time
    Z_t = A * np.sin(k * R1 - w * time) + A * np.sin(k * R2 - w * time)
    # Update the data in the plot
    cax.set_data(Z_t)
    return cax,

# 6. Run the animation
ani = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True)

# Note: If running in a Jupyter Notebook, you may need to use:
# from IPython.display import HTML
# HTML(ani.to_jshtml())
plt.show()