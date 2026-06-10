from dataclasses import dataclass
import numpy as np

@dataclass
class SimulationConfig:
    grid_size: int = 400
    x_min: float = -10.0
    x_max: float = 10.0
    y_min: float = -10.0
    y_max: float = 10.0

    source1_amplitude: float = 1.0
    source1_wavelength: float = 2.0
    source2_amplitude: float = 1.0
    source2_wavelength: float = 2.0
    frequency: float = 1.0
    phase_difference: float = 0.0

    frames: int = 300
    interval: int = 30

    time: float = 0.0
    time_step: float = 0.05
    use_intensity: bool = False

    source1_x: float = -10.0
    source1_y: float = -3.0
    source2_x: float = -10.0
    source2_y: float = 3.0

    def make_grid(self):
        x = np.linspace(self.x_min, self.x_max, self.grid_size)
        y = np.linspace(self.y_min, self.y_max, self.grid_size)
        return np.meshgrid(x, y)

DEFAULT_CONFIG = SimulationConfig()