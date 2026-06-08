from analysis import (calculate_energy, calculate_rms, calculate_max_amplitude, calculate_statistics, measure_runtime)

def generate_report(wave):
    energy = calculate_energy(wave)
    rms = calculate_rms(wave)
    maximum = calculate_max_amplitude(wave)
    stats = calculate_statistics(wave)

    report = f"""
==================================
WAVE SIMULATION REPORT
==================================

Energy: {energy:.4f}
RMS: {rms:.4f}
Maximum Amplitude: {maximum:.4f}
Mean: {stats['mean']:.4f}
Standard Deviation: {stats['std']:.4f}

==================================
"""
    return report