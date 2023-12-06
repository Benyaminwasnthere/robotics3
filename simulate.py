import argparse
import os

import numpy as np
#-----------------------------------
# Function to generate odometry measurements
def generate_odometry_measurements(controls_file_path, sigma_e_omega, sigma_e_phi):
    control_sequence = np.load(controls_file_path, allow_pickle=True)
    executed_controls=[]
    # Extract initial pose and controls
    initial_pose = control_sequence[0]  # Use [0] directly for the initial pose
    planned_controls = control_sequence[1:]  # Use slicing to get the planned controls



    odometry_measurements = []
    current_pose = np.array(initial_pose)

    for control in planned_controls:
        # Extract control values
        v, phi = control

        # Implement Eq. 5 to generate odometry measurements with noise
        noisy_omega = v + np.random.normal(0, sigma_e_omega)
        noisy_phi = phi + np.random.normal(0, sigma_e_phi)


        # Append the noisy odometry measurement
        odometry_measurements.append([noisy_omega, noisy_phi])
    odometry_measurements.insert(0, initial_pose)
    return odometry_measurements

def create_executed(controls_file_path):
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
def simulate(plan_file, map_file, execution_file, sensing_file):
    # Implement your simulation logic here
    # You can use the provided file paths: plan_file, map_file, execution_file, sensing_file
    if not os.path.exists("readings"):
        os.makedirs("readings")
    if not os.path.exists("gts"):
        os.makedirs("gts")
    print(f"Plan File: {plan_file}")
    print(f"Map File: {map_file}")
    executed_controls = create_executed(f"controls/{plan_file}")
    control_sequence = np.array(executed_controls, dtype=object)
    np.save(os.path.join("gts", execution_file), control_sequence)
    print(f"Made Actuation Model: {execution_file} ")
    # Low-level noise
    sigma_e_omega_low = 0.05
    sigma_e_phi_low = 0.1
    measurements_low = generate_odometry_measurements(f"gts/{execution_file}", sigma_e_omega_low, sigma_e_phi_low)
    control_sequence = np.array(measurements_low, dtype=object)
    np.save(os.path.join("readings", f"{sensing_file}_L.npy"), control_sequence)
    # High-level noise
    sigma_e_omega_high = 0.1
    sigma_e_phi_high = 0.3
    measurements_high = generate_odometry_measurements(f"gts/{execution_file}", sigma_e_omega_high, sigma_e_phi_high)
    control_sequence = np.array( measurements_high, dtype=object)
    np.save(os.path.join("readings", f"{sensing_file}_H.npy"), control_sequence)

    print(f"Made Odometry model LOW: {sensing_file}_L.npy ")
    print(f"Made Odometry model HIGH: {sensing_file}_H.npy ")




if __name__ == "__main__":
    #input : --plan controls_X_Y.npy --map landmark_X.npy --execution gt_X_Y.npy --sensing readings_X_Y
    # Create argument parser
    parser = argparse.ArgumentParser(description="Simulate something.")

    # Add command line arguments
    parser.add_argument("--plan", type=str, help="Path to the plan file")
    parser.add_argument("--map", type=str, help="Path to the map file")
    parser.add_argument("--execution", type=str, help="Path to the execution file")
    parser.add_argument("--sensing", type=str, help="Path to the sensing file")

    # Parse command line arguments
    args = parser.parse_args()

    # Call the simulate function with the provided arguments
    simulate(args.plan, args.map, args.execution, args.sensing)
