import numpy as np
from config import (GRID_SIZE, DX, DT, C)

class WaveSolver:
    def __init__(self):
        self.u_prev = np.zeros((GRID_SIZE, GRID_SIZE))
        self.u = np.zeros((GRID_SIZE, GRID_SIZE))
        self.u_next = np.zeros((GRID_SIZE, GRID_SIZE))

        center = GRID_SIZE // 2
        self.u[center, center] = 1.0

    # Finite difference method for wave equation
    def step(self):
        
        # Calculate the coefficient for the finite difference update
        # Stability condition: C * DT / DX <= 1
        coefficient = ((C * DT / DX)**2)

        # Finite difference update for the wave equation
        self.u_next[1:-1,1:-1] = (
            2*self.u[1:-1,1:-1] - self.u_prev[1:-1,1:-1] + coefficient *
            (self.u[2:,1:-1] + self.u[:-2,1:-1] + 
             self.u[1:-1,2:] + self.u[1:-1,:-2] - 
             4*self.u[1:-1,1:-1])
        )

        self.u_prev = self.u.copy()
        self.u = self.u_next.copy()
        return self.u