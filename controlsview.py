import numpy as np

# Load the control sequence
control_sequence = np.load("controls/controls_X_Y.npy", allow_pickle=True)

# Print the control sequence
print("Control Sequence:")
for i, control in enumerate(control_sequence):
    print(f"Step {i + 1}: {control}")