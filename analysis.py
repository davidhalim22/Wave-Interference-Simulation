import time
import tracemalloc
import numpy as np


def measure_runtime(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    runtime = end - start
    print(f"Runtime: {runtime:.6f} seconds")

    return result

def start_memory_tracking():
    tracemalloc.start()

def stop_memory_tracking():
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Current Memory: {current/1024**2:.2f} MB")
    print(f"Peak Memory: {peak/1024**2:.2f} MB")

def calculate_energy(wave):
    return np.sum(wave**2)

def calculate_rms(wave):
    return np.sqrt(np.mean(wave**2))

def calculate_max_amplitude(wave):
    return np.max(np.abs(wave))

def calculate_statistics(wave):
    return {
        "max": np.max(wave),
        "min": np.min(wave),
        "mean": np.mean(wave),
        "std": np.std(wave)
    }

def print_metrics(wave):
    print("Energy:", calculate_energy(wave))
    print("RMS:", calculate_rms(wave))
    print("Max Amplitude:", calculate_max_amplitude(wave))
    
    stats = calculate_statistics(wave)
    print(f"Mean: {stats['mean']:.4f}")
    print(f"Standard Deviation: {stats['std']:.4f}")