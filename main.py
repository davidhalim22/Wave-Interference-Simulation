import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import DEFAULT_CONFIG, SimulationConfig
from wave_source import WaveSource
from visualization import plot_wave, plot_intensity
from analysis import calculate_energy, calculate_statistics, measure_runtime, percent_difference, start_memory_tracking, stop_memory_tracking
from report_generator import generate_report


class WaveInterferenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wave Interference Simulator")
        self.config = SimulationConfig(**vars(DEFAULT_CONFIG))
        self.animation = None
        self.animation_window = None
        self.animation_fig = None
        self.animation_ax = None
        self.animation_canvas = None
        self.animation_image = None
        self.animation_time_text = None
        self.animation_running = False
        self.animation_time = 0.0
        self.animation_X = None
        self.animation_Y = None
        self.entries = {}
        self.use_intensity_var = tk.BooleanVar(value=self.config.use_intensity)
        self.live_update_var = tk.BooleanVar(value=False)
        self.randomization_mode_var = tk.StringVar(value="same")
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        fields = [
            ("Grid Size", "grid_size"),
            ("X Min", "x_min"),
            ("X Max", "x_max"),
            ("Y Min", "y_min"),
            ("Y Max", "y_max"),
            ("Source 1 Amplitude", "source1_amplitude"),
            ("Source 1 Wavelength", "source1_wavelength"),
            ("Source 2 Amplitude", "source2_amplitude"),
            ("Source 2 Wavelength", "source2_wavelength"),
            ("Frequency", "frequency"),
            ("Phase Difference", "phase_difference"),
            ("Time", "time"),
            ("Time Step", "time_step"),
            ("Frames", "frames"),
            ("Interval (ms)", "interval"),
            ("Source 1 X", "source1_x"),
            ("Source 1 Y", "source1_y"),
            ("Source 2 X", "source2_x"),
            ("Source 2 Y", "source2_y"),
        ]

        for row, (label_text, key) in enumerate(fields):
            label = ttk.Label(frame, text=label_text)
            label.grid(row=row, column=0, sticky="w", padx=(0, 6), pady=2)
            value = tk.StringVar(value=str(getattr(self.config, key)))
            entry = ttk.Entry(frame, textvariable=value, width=14)
            entry.grid(row=row, column=1, sticky="ew", pady=2)
            self.entries[key] = value

        intensity_check = ttk.Checkbutton(
            frame,
            text="Use intensity in animation",
            variable=self.use_intensity_var,
        )
        intensity_check.grid(row=len(fields), column=0, columnspan=2, sticky="w", pady=(8, 2))

        live_update_check = ttk.Checkbutton(
            frame,
            text="Live update parameters",
            variable=self.live_update_var,
        )
        live_update_check.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="w", pady=(0, 12))

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields) + 2, column=0, columnspan=2, sticky="ew")
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        random_mode_label = ttk.Label(button_frame, text="Randomization mode:")
        random_mode_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 2))
        ttk.Radiobutton(
            button_frame,
            text="Same for both sources",
            variable=self.randomization_mode_var,
            value="same",
        ).grid(row=4, column=0, sticky="w", padx=(0, 4))
        ttk.Radiobutton(
            button_frame,
            text="Different for each source",
            variable=self.randomization_mode_var,
            value="different",
        ).grid(row=4, column=1, sticky="w")

        ttk.Button(button_frame, text="Apply Settings", command=self.apply_settings).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(button_frame, text="Animate", command=self.animate_simulation).grid(row=0, column=2, sticky="ew", padx=2)
        ttk.Button(button_frame, text="Pause/Resume", command=self.toggle_animation).grid(row=0, column=3, sticky="ew", padx=2)
        ttk.Button(button_frame, text="Randomize A/W", command=self.randomize_amplitude_wavelength).grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=(8,0))
        ttk.Button(button_frame, text="Reset Defaults", command=self.reset_parameters).grid(row=1, column=2, columnspan=2, sticky="ew", padx=2, pady=(8,0))
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).grid(row=2, column=0, columnspan=4, sticky="ew", padx=2, pady=(8,0))

        ttk.Button(frame, text="Show Wave Plot", command=self.show_wave_plot).grid(row=len(fields) + 3, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Button(frame, text="Show Intensity Plot", command=self.show_intensity_plot).grid(row=len(fields) + 4, column=0, columnspan=2, sticky="ew", pady=4)

        log_label = ttk.Label(frame, text="Simulation Log")
        log_label.grid(row=0, column=2, sticky="w", padx=(12, 0))

        self.log_text = tk.Text(frame, width=60, height=24, wrap="word", state="disabled", background="#f7f7f7")
        self.log_text.grid(row=1, column=2, rowspan=len(fields) + 4, sticky="nsew", padx=(12, 0))

        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(len(fields) + 4, weight=1)

    def log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def apply_settings(self) -> bool:
        try:
            new_config = SimulationConfig(
                grid_size=int(self.entries["grid_size"].get()),
                x_min=float(self.entries["x_min"].get()),
                x_max=float(self.entries["x_max"].get()),
                y_min=float(self.entries["y_min"].get()),
                y_max=float(self.entries["y_max"].get()),
                source1_amplitude=float(self.entries["source1_amplitude"].get()),
                source1_wavelength=float(self.entries["source1_wavelength"].get()),
                source2_amplitude=float(self.entries["source2_amplitude"].get()),
                source2_wavelength=float(self.entries["source2_wavelength"].get()),
                frequency=float(self.entries["frequency"].get()),
                phase_difference=float(self.entries["phase_difference"].get()),
                time=float(self.entries["time"].get()),
                time_step=float(self.entries["time_step"].get()),
                frames=int(self.entries["frames"].get()),
                interval=int(self.entries["interval"].get()),
                source1_x=float(self.entries["source1_x"].get()),
                source1_y=float(self.entries["source1_y"].get()),
                source2_x=float(self.entries["source2_x"].get()),
                source2_y=float(self.entries["source2_y"].get()),
                use_intensity=self.use_intensity_var.get(),
            )

            if new_config.grid_size < 10:
                raise ValueError("Grid size must be at least 10.")
            if new_config.x_max <= new_config.x_min:
                raise ValueError("X Max must be greater than X Min.")
            if new_config.y_max <= new_config.y_min:
                raise ValueError("Y Max must be greater than Y Min.")
            if new_config.frames < 1:
                raise ValueError("Frames must be at least 1.")
            if new_config.interval < 1:
                raise ValueError("Interval must be at least 1 ms.")
            if new_config.time_step <= 0:
                raise ValueError("Time Step must be greater than 0.")

            self.config = new_config
            self.log("Settings applied successfully.")
            return True
        except ValueError as error:
            messagebox.showerror("Invalid setting", str(error))
            return False

    def randomize_amplitude_wavelength(self):
        rng = np.random.default_rng()
        mode = self.randomization_mode_var.get()

        if mode == "same":
            current_amp = self.get_entry_value("source1_amplitude", self.config.source1_amplitude, float)
            current_wl = self.get_entry_value("source1_wavelength", self.config.source1_wavelength, float)
            new_amp = current_amp * rng.uniform(0.5, 2.0)
            new_wl = current_wl * rng.uniform(0.7, 3.0)

            self.config.source1_amplitude = new_amp
            self.config.source1_wavelength = new_wl
            self.config.source2_amplitude = new_amp
            self.config.source2_wavelength = new_wl

            self.entries["source1_amplitude"].set(f"{new_amp:.3f}")
            self.entries["source1_wavelength"].set(f"{new_wl:.3f}")
            self.entries["source2_amplitude"].set(f"{new_amp:.3f}")
            self.entries["source2_wavelength"].set(f"{new_wl:.3f}")
            self.log(f"Randomized both sources to amplitude {new_amp:.3f}, wavelength {new_wl:.3f}")
        else:
            current_amp1 = self.get_entry_value("source1_amplitude", self.config.source1_amplitude, float)
            current_wl1 = self.get_entry_value("source1_wavelength", self.config.source1_wavelength, float)
            current_amp2 = self.get_entry_value("source2_amplitude", self.config.source2_amplitude, float)
            current_wl2 = self.get_entry_value("source2_wavelength", self.config.source2_wavelength, float)

            new_amp1 = current_amp1 * rng.uniform(0.5, 2.0)
            new_wl1 = current_wl1 * rng.uniform(0.7, 3.0)
            new_amp2 = current_amp2 * rng.uniform(0.5, 2.0)
            new_wl2 = current_wl2 * rng.uniform(0.7, 3.0)

            self.config.source1_amplitude = new_amp1
            self.config.source1_wavelength = new_wl1
            self.config.source2_amplitude = new_amp2
            self.config.source2_wavelength = new_wl2

            self.entries["source1_amplitude"].set(f"{new_amp1:.3f}")
            self.entries["source1_wavelength"].set(f"{new_wl1:.3f}")
            self.entries["source2_amplitude"].set(f"{new_amp2:.3f}")
            self.entries["source2_wavelength"].set(f"{new_wl2:.3f}")
            self.log(f"Randomized source 1 amplitude to {new_amp1:.3f}, wavelength to {new_wl1:.3f}")
            self.log(f"Randomized source 2 amplitude to {new_amp2:.3f}, wavelength to {new_wl2:.3f}")

        self.refresh_animation_frame()

    def reset_parameters(self):
        self.config = SimulationConfig(**vars(DEFAULT_CONFIG))
        for key, value in self.config.__dict__.items():
            if key in self.entries:
                self.entries[key].set(str(value))
        self.use_intensity_var.set(self.config.use_intensity)
        self.live_update_var.set(False)
        self.randomization_mode_var.set("same")
        self.log("Parameters reset to initial default values.")

    def create_sources(self):
        source1 = WaveSource(
            x=self.config.source1_x,
            y=self.config.source1_y,
            amplitude=self.config.source1_amplitude,
            wavelength=self.config.source1_wavelength,
            frequency=self.config.frequency,
        )
        source2 = WaveSource(
            x=self.config.source2_x,
            y=self.config.source2_y,
            amplitude=self.config.source2_amplitude,
            wavelength=self.config.source2_wavelength,
            frequency=self.config.frequency,
            phase=self.config.phase_difference,
        )
        return source1, source2

    def generate_wave_data(self):
        X, Y = self.config.make_grid()
        source1, source2 = self.create_sources()
        wave1 = source1.generate_wave(X, Y, self.config.time)
        wave2 = source2.generate_wave(X, Y, self.config.time)
        total_wave = wave1 + wave2
        return source1, source2, X, Y, wave1, wave2, total_wave

    def run_simulation(self):
        if not self.apply_settings():
            return

        self.log("Running simulation...")
        start_memory_tracking()
        source1, source2, X, Y, wave1, wave2, total_wave = self.generate_wave_data()
        stop_memory_tracking()

        energy = calculate_energy(total_wave)
        stats = calculate_statistics(total_wave)
        energy1 = calculate_energy(wave1)
        energy2 = calculate_energy(wave2)
        energy_diff = abs(energy1 - energy2)
        percent_diff = percent_difference(energy1, energy2)

        self.log(f"Energy: {energy:.4f}")
        self.log(f"Mean: {stats['mean']:.4f}")
        self.log(f"Std dev: {stats['std']:.4f}")
        self.log(f"Energy source 1: {energy1:.6f}")
        self.log(f"Energy source 2: {energy2:.6f}")
        self.log(f"Energy difference: {energy_diff:.6f}")
        self.log(f"Percent difference: {percent_diff:.6f}%")
        self.log(generate_report(total_wave).strip())
        self.log("Simulation complete.")

    def show_wave_plot(self):
        if not self.apply_settings():
            return
        _, _, _, _, _, _, total_wave = self.generate_wave_data()
        plot_wave(
            total_wave,
            title="Wave Interference Pattern",
            x_min=self.config.x_min,
            x_max=self.config.x_max,
            y_min=self.config.y_min,
            y_max=self.config.y_max,
        )

    def show_intensity_plot(self):
        if not self.apply_settings():
            return
        _, _, _, _, _, _, total_wave = self.generate_wave_data()
        plot_intensity(
            total_wave,
            x_min=self.config.x_min,
            x_max=self.config.x_max,
            y_min=self.config.y_min,
            y_max=self.config.y_max,
        )

    def create_animation_window(self):
        if self.animation_window and self.animation_window.winfo_exists():
            return

        self.animation_window = tk.Toplevel(self.root)
        self.animation_window.title("Real-Time Wave Animation")
        self.animation_fig, self.animation_ax = plt.subplots(figsize=(6, 5))
        self.animation_canvas = FigureCanvasTkAgg(self.animation_fig, master=self.animation_window)
        self.animation_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.animation_window.protocol("WM_DELETE_WINDOW", self.close_animation_window)

    def close_animation_window(self):
        if self.animation is not None:
            self.animation.event_source.stop()
            self.animation = None
            self.animation_running = False
        if self.animation_window:
            self.animation_window.destroy()
            self.animation_window = None

    def get_entry_value(self, key, default, value_type=float):
        text = self.entries[key].get().strip()
        if text == "":
            return default
        try:
            return value_type(text)
        except ValueError:
            return default

    def update_live_parameters(self):
        if not self.live_update_var.get():
            return

        self.config.source1_amplitude = self.get_entry_value("source1_amplitude", self.config.source1_amplitude, float)
        self.config.source1_wavelength = self.get_entry_value("source1_wavelength", self.config.source1_wavelength, float)
        self.config.source2_amplitude = self.get_entry_value("source2_amplitude", self.config.source2_amplitude, float)
        self.config.source2_wavelength = self.get_entry_value("source2_wavelength", self.config.source2_wavelength, float)
        self.config.frequency = self.get_entry_value("frequency", self.config.frequency, float)
        self.config.phase_difference = self.get_entry_value("phase_difference", self.config.phase_difference, float)
        self.config.time_step = self.get_entry_value("time_step", self.config.time_step, float)
        self.config.source1_x = self.get_entry_value("source1_x", self.config.source1_x, float)
        self.config.source1_y = self.get_entry_value("source1_y", self.config.source1_y, float)
        self.config.source2_x = self.get_entry_value("source2_x", self.config.source2_x, float)
        self.config.source2_y = self.get_entry_value("source2_y", self.config.source2_y, float)
        self.config.use_intensity = self.use_intensity_var.get()

        interval = self.get_entry_value("interval", self.config.interval, int)
        if interval > 0:
            self.config.interval = interval
            if self.animation is not None:
                self.animation.event_source.interval = interval

    def toggle_animation(self):
        if self.animation is None:
            return
        if self.animation_running:
            self.animation.event_source.stop()
            self.animation_running = False
            self.log("Animation paused.")
        else:
            self.animation.event_source.start()
            self.animation_running = True
            self.log("Animation resumed.")

    def refresh_animation_frame(self):
        if self.animation_image is None or self.animation_X is None or self.animation_Y is None:
            return
        source1, source2 = self.create_sources()
        current_time = self.animation_time
        wave1 = source1.generate_wave(self.animation_X, self.animation_Y, current_time)
        wave2 = source2.generate_wave(self.animation_X, self.animation_Y, current_time)
        total_wave = wave1 + wave2
        if self.config.use_intensity:
            total_wave = total_wave**2
        self.animation_image.set_array(total_wave)
        self.animation_image.set_clim(vmin=np.min(total_wave), vmax=np.max(total_wave))
        self.animation_canvas.draw_idle()

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def animate_simulation(self):
        if not self.apply_settings():
            return
        self.log("Starting real-time animation...")
        source1, source2, X, Y, _, _, _ = self.generate_wave_data()
        self.create_animation_window()

        self.animation_ax.clear()
        self.animation_ax.set_title("Wave Interference Animation")
        self.animation_ax.set_xlabel("X")
        self.animation_ax.set_ylabel("Y")
        self.animation_ax.set_xlim(self.config.x_min, self.config.x_max)
        self.animation_ax.set_ylim(self.config.y_min, self.config.y_max)

        self.animation_X = X
        self.animation_Y = Y

        self.animation_image = self.animation_ax.imshow(
            np.zeros((Y.shape[0], X.shape[1])),
            extent=(self.config.x_min, self.config.x_max, self.config.y_min, self.config.y_max),
            origin='lower',
            cmap='viridis',
            animated=True,
        )
        self.animation_ax.scatter([source1.x, source2.x], [source1.y, source2.y], color='red', s=100)
        self.animation_time_text = self.animation_ax.text(0.02, 0.95, "", transform=self.animation_ax.transAxes, color="white")

        if self.animation is not None:
            self.animation.event_source.stop()

        self.animation_time = self.config.time

        def update(frame):
            self.update_live_parameters()
            source1, source2 = self.create_sources()
            self.animation_time += self.config.time_step
            current_time = self.animation_time
            wave1 = source1.generate_wave(X, Y, current_time)
            wave2 = source2.generate_wave(X, Y, current_time)
            total_wave = wave1 + wave2
            if self.config.use_intensity:
                total_wave = total_wave**2
            self.animation_image.set_array(total_wave)
            self.animation_image.set_clim(vmin=np.min(total_wave), vmax=np.max(total_wave))
            self.animation_time_text.set_text(f"Time: {current_time:.2f}s")
            if self.animation is not None and hasattr(self.animation, 'event_source'):
                self.animation.event_source.interval = self.config.interval
            return [self.animation_image, self.animation_time_text]

        frames = itertools.count() if self.config.frames <= 0 else self.config.frames
        self.animation = FuncAnimation(
            self.animation_fig,
            update,
            frames=frames,
            interval=self.config.interval,
            blit=False,
        )
        self.animation_running = True
        self.animation_canvas.draw_idle()


if __name__ == "__main__":
    root = tk.Tk()
    app = WaveInterferenceGUI(root)
    root.mainloop()