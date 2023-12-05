import numpy as np

def add_noise_to_controls(controls_file_path):
    # Load control inputs from the file
    control_sequence = np.load(controls_file_path, allow_pickle=True)
    executed_controls=[]
    # Extract initial pose and controls
    initial_pose = control_sequence[0]  # Use [0] directly for the initial pose
    planned_controls = control_sequence[1:]  # Use slicing to get the planned controls
    # Parameters for noise
    sigma_linear = 0.075
    sigma_angular = 0.2
    for i in range(len(planned_controls)):
        # Extract planned linear and angular velocities
        v_planned, omega_planned = planned_controls[i]

        # Generate noise
        noise_linear = np.random.normal(0, sigma_linear)
        noise_angular = np.random.normal(0, sigma_angular)
        v_noisy = v_planned + noise_linear
        omega_noisy = omega_planned + noise_angular
        current_control = np.array([omega_planned, noise_angular])
        executed_controls.append(current_control.copy())
    executed_controls.insert(0, initial_pose)
    return executed_controls

# Example usage
controls_file_path = "controls/controls_X_Y.npy"
executed_controls = add_noise_to_controls(controls_file_path)
print("done")
#
