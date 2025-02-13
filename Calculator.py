import numpy as np
from Visualization import plot_three_waves

def generate_custom_wave(t, period, on_duration, offset=0):
    """
    Generate a square wave that is HIGH (1) for a duration of 'on_duration'
    every 'period' seconds, shifted by 'offset'.

    The signal is 1 when (t - offset) mod period < on_duration, and 0 otherwise.
    """
    mod_t = (t - offset) % period
    wave = (mod_t < on_duration).astype(int)
    return wave

if __name__ == '__main__':
    # ---------------------------
    # Simulation Parameters
    # ---------------------------
    dt = 1  # simulation time step in seconds
    T_total = 50.0  # total simulation time in seconds
    t = np.arange(0, T_total, dt)

    # ---------------------------
    # Wave Parameters
    # ---------------------------
    # Wave 1 (priority) parameters:
    #   period: 4 seconds, on_duration: 2 seconds, offset: 2 seconds → starts low.
    wave1_params = {
        'period': 4.0,
        'on_duration': 2.0,
        'offset': 2.0
    }

    # Wave 2 (original) parameters:
    #   period: 5 seconds, on_duration: 3 seconds, offset: 2 seconds → starts low.
    wave2_params = {
        'period': 5.0,
        'on_duration': 2.0,
        'offset': 3.0
    }

    # ---------------------------
    # Generate the Original Waves
    # ---------------------------
    wave1 = generate_custom_wave(t, **wave1_params)
    print(wave1)
    wave2 = generate_custom_wave(t, **wave2_params)  # For comparison
    print(wave2)

    # ---------------------------
    # Compute the Modified (Retimed) Wave 2 Using Two Pointers
    # ---------------------------
    # p_old tracks the progress along the original Wave 2 timeline (in seconds)
    p_old = 0.0
    modified_wave2 = np.zeros_like(t)

    # Extract Wave 2 parameters for convenience.
    w2_period = wave2_params['period']
    w2_on_duration = wave2_params['on_duration']
    w2_offset = wave2_params['offset']

    for i in range(len(t)):
        # Evaluate Wave 1 at simulation time t[i]
        w1_val = wave1[i]

        # Evaluate the original Wave 2 at time p_old:
        mod_time = (p_old - w2_offset) % w2_period
        w2_val = 1 if mod_time < w2_on_duration else 0

        if w1_val == 1:
            # Wave 1 is ON → it has priority.
            if w2_val == 1:
                # Scenario 1: Wave 1 on, and original Wave 2 is in its ON interval.
                # Force modified Wave 2 to 0 (idle) and do NOT advance p_old.
                modified_wave2[i] = 0
            else:
                # Scenario 2: Wave 1 on, and original Wave 2 is OFF.
                modified_wave2[i] = 0
                p_old += dt  # Advance p_old.
        else:
            # Scenario 3: Wave 1 is OFF.
            # Output the original Wave 2 value and advance p_old.
            modified_wave2[i] = w2_val
            p_old += dt

    # ---------------------------
    # Measure the Slowdown Factor
    # ---------------------------
    # We define the slowdown factor as:
    #       slowdown = (total new up time) / (total original up time)
    #
    # Here the "up time" is the total time (in seconds) that the signal is HIGH (1) over the simulation.
    total_original_up_time = np.sum(wave2) * dt
    total_new_up_time = np.sum(modified_wave2) * dt

    # Compute the slowdown factor:
    slowdown = total_new_up_time / total_original_up_time if total_original_up_time > 0 else 0

    print("Total original Wave 2 up time: {:.3f} s".format(total_original_up_time))
    print("Total modified Wave 2 up time: {:.3f} s".format(total_new_up_time))
    print("Slowdown factor (new up time / original up time): {:.3f}".format(slowdown))

    plot_three_waves(t, T_total, wave1, wave2, modified_wave2)


