# Emulation For AD9833 Using Python: 


import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker 
 
# Constants 
MCLK = 25e6  # Master Clock Frequency (25 MHz) 
PHASE_ACC_BITS = 28  # 28-bit Phase Accumulator 
DAC_RESOLUTION = 10  # 10-bit DAC 
LOOKUP_TABLE_SIZE = 4096  # 12-bit SIN ROM addressable steps 
 
VPP_DESIRED = 0.6  # Desired output peak-to-peak voltage (V) 
VREF = 3.3  # DAC reference voltage (assumed) 
V_AMPLITUDE = VPP_DESIRED / 2  # Peak amplitude (0.3V) 
 
# User-defined output frequency 
f_out = float(input("Enter output frequency in Hz: "))  # Example: 1 kHz 
 
# Compute Phase Increment (Delta Phase) 
delta_phase = int((f_out * (2**PHASE_ACC_BITS)) / MCLK) 
print(f"Delta Phase: {delta_phase}") 
 
# Generate SIN ROM lookup table centered at 0V (-0.3V to +0.3V) 
sin_rom = [V_AMPLITUDE * np.sin(2 * np.pi * n / LOOKUP_TABLE_SIZE) for n in 
range(LOOKUP_TABLE_SIZE)] 
 
# Compute the number of samples per sine wave period 
samples_per_period = int(MCLK / f_out)  # Number of samples required for one full sine 
period 
num_periods = 5  # At least 5 full sine wave cycles 
extra_samples = samples_per_period + 1  # Extra cycle has one extra sample 
num_samples = (num_periods * samples_per_period) + extra_samples  # Total samples including extra 
 
# Simulate the waveform generation (Sampled Delta Phase) 
waveform_sampled = [] 
time_sampled = [] 
phase_accumulator = 0   
cycle_count = 0   
 
while cycle_count < num_periods:   
    for i in range(samples_per_period):   
        sin_rom_index = (phase_accumulator >> 16) & 0xFFF  # Extract top 12 MSBs 
        dac_output = sin_rom[sin_rom_index]  # Fetch voltage amplitude 
        waveform_sampled.append(dac_output) 
        time_sampled.append((cycle_count * samples_per_period + i) / MCLK)  # Time tracking 
 
        # Update phase accumulator 
        phase_accumulator = (phase_accumulator + delta_phase) % (2**PHASE_ACC_BITS) 
 
    cycle_count += 1   
 
# *Extra Cycle (One Extra Sample)* 
for i in range(extra_samples):   
    sin_rom_index = (phase_accumulator >> 16) & 0xFFF 
    dac_output = sin_rom[sin_rom_index] 
 
    if i == extra_samples - 1: 
        dac_output = 0.0  # Force last value to zero 
 
    waveform_sampled.append(dac_output) 
    time_sampled.append((cycle_count * samples_per_period + i) / MCLK)  # Time tracking 
    phase_accumulator = (phase_accumulator + delta_phase) % (2**PHASE_ACC_BITS) 
 
# *Generate Full SIN ROM-Based Sine Wave (4096 Values, Repeated for 5 Cycles)* 
T_sample = 1 / MCLK  # Time per sample 
T_period = 1 / f_out  # Time for one full sine wave cycle 
T_total = num_periods * T_period  # Total time for 5 cycles 
time_full = np.linspace(0, T_total, num_periods * LOOKUP_TABLE_SIZE)  # Corrected time axis in seconds 
waveform_full = np.tile(sin_rom, num_periods)  # Repeat the full sine wave 5 times 
 
# *Generate Phase Values (0 to 2π for 4096 points)* 
phase_values = np.linspace(0, 2*np.pi, LOOKUP_TABLE_SIZE) 
 
# *Save Phase vs Voltage to File* 
with open("phase_vs_voltage.txt", "w") as file: 
    file.write("Phase (radians) | Voltage (V)\n") 
    file.write("-----------------------------\n") 
    for i in range(LOOKUP_TABLE_SIZE): 
        file.write(f"{phase_values[i]:.6f} | {sin_rom[i]:.10f}V\n") 
 
# *Save SIN ROM Lookup Table to File* 
with open("sin_rom_data.txt", "w") as file: 
    file.write("Index | SIN ROM Value (V)\n") 
    file.write("------------------------\n") 
    for i in range(LOOKUP_TABLE_SIZE): 
        file.write(f"{i:4d} | {sin_rom[i]:.10f}V\n") 
 
# *Save Sampled Delta Phase Values to File* 
with open("sampled_sine_wave.txt", "w") as file: 
    file.write(f"Delta Phase: {delta_phase}\n\n") 
    file.write("Sampled Sine Wave Using Delta Phase:\n") 
    file.write("Step | Phase Accumulator | SIN ROM Index | Voltage (V)\n") 
    file.write("--------------------------------------------------------\n") 
     
    phase_accumulator = 0 
    for i in range(num_samples): 
        sin_rom_index = (phase_accumulator >> 16) & 0xFFF   
        voltage = sin_rom[sin_rom_index] 
        file.write(f"{i:4d} | {phase_accumulator:20d} | {sin_rom_index:13d} | {voltage:.10f}V\n") 
        phase_accumulator = (phase_accumulator + delta_phase) % (2**PHASE_ACC_BITS)   
 
print("SIN ROM values saved to 'sin_rom_data.txt'") 
print("Sampled sine wave values saved to 'sampled_sine_wave.txt'") 
print("Phase vs Voltage values saved to 'phase_vs_voltage.txt'") 
 
# *Plot Full SIN ROM Lookup Table (4096 Values, 5 Cycles)* 
plt.figure(figsize=(10, 4)) 
plt.plot(time_full, waveform_full, label="Full SIN ROM (4096 Points per Cycle)", color='b') 
plt.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.8) 
plt.grid(which='minor', linestyle='--', linewidth=0.5, alpha=0.5) 
plt.minorticks_on() 
plt.xlabel("Time (s)")   
plt.ylabel("Output Voltage (V)") 
plt.title(f"Full SIN ROM Lookup Table (5 Cycles)") 
plt.legend() 
plt.show() 
 
# *Plot Sampled Sine Wave (Delta Phase)* 
plt.figure(figsize=(10, 4)) 
plt.plot(time_sampled, waveform_sampled, label="Sampled (Delta Phase)", color='r') 
plt.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.8) 
plt.grid(which='minor', linestyle='--', linewidth=0.5, alpha=0.5) 
plt.minorticks_on() 
plt.xlabel("Time (s)") 
plt.ylabel("Output Voltage (V)") 
plt.title(f"Sampled Sine Wave Using Delta Phase (5 Cycles)") 
plt.legend() 
plt.show() 
 
# *Plot Sine Wave vs Phase (0 to 2π) with π labels* 
plt.figure(figsize=(10, 4)) 
plt.plot(phase_values, sin_rom, label="Sine Wave vs Phase", color='g') 
plt.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.8) 
plt.grid(which='minor', linestyle='--', linewidth=0.5, alpha=0.5) 
plt.minorticks_on() 
 
# *Set x-axis labels in multiples of π* 
plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ["0", "π/2", "π", "3π/2", "2π"]) 
 
plt.xlabel("Phase (radians)") 
plt.ylabel("Output Voltage (V)") 
plt.title("Sine Wave with Respect to Phase (0 to 2π)") 
plt.legend() 
plt.show()