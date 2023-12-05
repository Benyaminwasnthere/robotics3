import argparse
import os

import numpy as np

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

if __name__ == "__main__":
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