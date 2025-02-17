import numpy as np
import matplotlib.pyplot as plt
import math

def find_repeated_block(arr):
    """
    Find the smallest block that repeats over the array.
    For example, if arr = [-2, 3, -2, 3, -2, 3], it returns [-2, 3].
    """
    n = len(arr)
    # Try block lengths from 1 up to n//2 (inclusive)
    for block_len in range(1, n // 2 + 1):
        pattern = arr[:block_len]
        full_repeats = n // block_len
        is_repeated = True
        for i in range(full_repeats):
            start = i * block_len
            end = start + block_len
            if arr[start:end] != pattern:
                is_repeated = False
                break
        if is_repeated:
            return pattern
    return arr

def generate_wave_from_pattern(t, pattern, offset=0):
    """
    Generate a binary wave from a run–length pattern.
    
    The pattern is a list of durations:
      - A negative value indicates a run of 0's.
      - A positive value indicates a run of 1's.
    
    The pattern repeats every period = sum(abs(pattern)).
    An offset (in seconds) can be applied.
    """
    period = sum(abs(x) for x in pattern)
    # Precompute boundaries (in seconds) within one period.
    boundaries = []
    current = 0
    for x in pattern:
        current += abs(x)
        boundaries.append(current)
    
    wave = np.zeros_like(t, dtype=int)
    for i, time_val in enumerate(t):
        mod_time = (time_val - offset) % period
        for j, boundary in enumerate(boundaries):
            if mod_time < boundary:
                wave[i] = 1 if pattern[j] > 0 else 0
                break
    return wave

def evaluate_wave_from_pattern(time, pattern, offset=0):
    """
    Evaluate the binary wave (0 or 1) at a given time from the run–length pattern.
    """
    period = sum(abs(x) for x in pattern)
    mod_time = (time - offset) % period
    current = 0
    for x in pattern:
        current += abs(x)
        if mod_time < current:
            return 1 if x > 0 else 0
    return 0

def run_length_encode_wave(wave, dt):
    """
    Convert a binary wave (array of 0's and 1's) into a run-length encoded list.
    
    Each run is represented by its duration in seconds:
      - A negative duration indicates a run of 0's.
      - A positive duration indicates a run of 1's.
    """
    if len(wave) == 0:
        return []
    
    runs = []
    current_value = wave[0]
    count = 1
    for i in range(1, len(wave)):
        if wave[i] == current_value:
            count += 1
        else:
            duration = count * dt
            runs.append(duration if current_value == 1 else -duration)
            current_value = wave[i]
            count = 1
    duration = count * dt
    runs.append(duration if current_value == 1 else -duration)
    return runs

def simulate_and_get_cycle_pattern(dt, T_total, wave1_pattern, wave1_offset, wave2_pattern, wave2_offset, mode):
    """
    Simulate Wave 1 (priority) and Wave 2 (original) using run–length patterns,
    compute the modified (retimed) Wave 2 using the two–pointer method, and then 
    determine the cycle pattern of the modified Wave 2.
    
    Returns a dictionary containing:
      - 't': time array
      - 'wave1': Wave 1 (array)
      - 'wave2': Original Wave 2 (array)
      - 'modified_wave2': Modified (retimed) Wave 2 (array)
      - 'rl_wave1': run–length encoded Wave 1 (list)
      - 'rl_wave2': run–length encoded Original Wave 2 (list)
      - 'rl_modified': run–length encoded Modified Wave 2 (list)
      - 'cycle_pattern': detected cycle pattern in Modified Wave 2 (list)
    """
    t = np.arange(0, T_total, dt)
    
    # Generate the original waves from patterns.
    wave1 = generate_wave_from_pattern(t, wave1_pattern, offset=wave1_offset)
    wave2 = generate_wave_from_pattern(t, wave2_pattern, offset=wave2_offset)
    
    # Compute the Modified (Retimed) Wave 2 using two pointers.
    # p_old tracks progress along the original Wave 2 timeline (in seconds)
    p_old = 0.0  
    modified_wave2 = np.zeros_like(t, dtype=int)
    
    for i in range(len(t)):
        # Sample Wave 1 at simulation time t[i]
        w1_val = wave1[i]
        # Evaluate original Wave 2 at time p_old using its pattern.
        w2_val = evaluate_wave_from_pattern(p_old, wave2_pattern, offset=wave2_offset)
    
        if w1_val == 1:
            # Wave 1 is ON → it has priority.
            if w2_val == 1:
                # Scenario 1: Wave 1 on and original Wave 2 is "on" → force modified output to 0.
                # Do not advance p_old.
                modified_wave2[i] = 0
                if mode=="availability":
                    p_old += dt
            else:
                # Scenario 2: Wave 1 on and original Wave 2 is "off" → output 0 and advance p_old.
                modified_wave2[i] = 0
                p_old += dt
        else:
            # Scenario 3: Wave 1 is OFF → output the original Wave 2 value and advance p_old.
            modified_wave2[i] = w2_val
            p_old += dt
    
    # Get run-length encoded arrays.
    rl_wave1 = run_length_encode_wave(wave1, dt)
    rl_wave2 = run_length_encode_wave(wave2, dt)
    rl_modified = run_length_encode_wave(modified_wave2, dt)
    
    # ---- Extra work to determine the cycle pattern of Modified Wave 2 ----
    # Compute total "on" time from the original Wave 2 pattern.
    wave2_Ts = 0
    for k in wave2_pattern:
        if k > 0:
            wave2_Ts += k

    sum_up = 0
    Time_to_i = 0
    i_idx = 0
    while i_idx < len(rl_modified) and sum_up < wave2_Ts:
        if rl_modified[i_idx] > 0:
            sum_up += rl_modified[i_idx]
        Time_to_i += abs(rl_modified[i_idx])
        i_idx += 1

    # Compute the period of Wave 1 from its pattern.
    wave1_T = 0
    for k in wave1_pattern:
        # Add absolute duration.
        wave1_T += abs(k)
    
    #If the time consumed is less than the period of Wave 1, scale accordingly.
    if Time_to_i < wave1_T:
        multiplier = math.ceil(wave1_T / Time_to_i)+1
        sum_up = 0
        while i_idx < len(rl_modified) and sum_up < multiplier*wave2_Ts:
            if rl_modified[i_idx] > 0:
                sum_up += rl_modified[i_idx]
            i_idx += 1

    # Take the remainder of the run-length encoded modified wave starting from index i_idx.
    rl_modified_cycle = rl_modified[i_idx:]
    
    # Find the smallest repeating block (cycle pattern) in the modified wave.
    cycle_pattern = find_repeated_block(rl_modified_cycle)
    # ----------------------------------------------------------------------
    
    return {
        't': t,
        'wave1': wave1,
        'wave2': wave2,
        'modified_wave2': modified_wave2,
        'rl_wave1': rl_wave1,
        'rl_wave2': rl_wave2,
        'rl_modified': rl_modified,
        'cycle_pattern': cycle_pattern
    }

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    # Define simulation parameters.
    dt = 1              # time step (seconds)
    T_total = 100       # total simulation time (seconds)
    mode = "contention" # "contention"/ "availability"
    
    # Define wave patterns (run-length encoded arrays).
    # For Wave 1 (priority): e.g., [-4, 4] means 4 s off, 4 s on (period = 8 s).
    wave1_pattern = [-9, 4, -6, 1]
    wave1_offset = 0
    
    # For Wave 2 (original): e.g., [6, -4] means 6 s on, 4 s off (period = 10 s).
    # (You can mix negatives and positives in any order.)
    wave2_pattern = [-4, 4]
    wave2_offset = 0
    
    # Run the simulation.
    result = simulate_and_get_cycle_pattern(dt, T_total, wave1_pattern, wave1_offset, wave2_pattern, wave2_offset, mode)
    
    # Print the run-length encoded arrays and the detected cycle pattern.
    print("mode:",mode)
    print("Run-length encoded arrays (in seconds):")
    print("Wave 1         :", result['rl_wave1'])
    print("Original Wave 2:", result['rl_wave2'])
    print("Modified Wave 2:", result['rl_modified'])
    print("\nDetected cycle pattern in Modified Wave 2:", result['cycle_pattern'])
    
    # Plot all waves in one figure (three subplots).
    t = result['t']
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    axs[0].step(t, result['wave1'], where='post', color='blue')
    axs[0].set_title("Wave 1 (Priority)")
    axs[0].set_ylabel("Signal")
    axs[0].set_ylim(-0.2, 1.2)
    axs[0].grid(True)
    axs[0].set_xticks(np.arange(0, T_total+1, 1))
    
    axs[1].step(t, result['wave2'], where='post', color='green')
    axs[1].set_title("Original Wave 2")
    axs[1].set_ylabel("Signal")
    axs[1].set_ylim(-0.2, 1.2)
    axs[1].grid(True)
    axs[1].set_xticks(np.arange(0, T_total+1, 1))
    
    axs[2].step(t, result['modified_wave2'], where='post', color='red', linewidth=2)
    axs[2].set_title("Modified (Retimed) Wave 2")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("Signal")
    axs[2].set_ylim(-0.2, 1.2)
    axs[2].grid(True)
    axs[2].set_xticks(np.arange(0, T_total+1, 1))
    
    plt.tight_layout()
    plt.show()
