import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
import os

x = random.uniform(0.0, 2.0)
y = random.uniform(0.0, 2.0)
theta = random.uniform(0.0, 2.0)
# ... (previous code remains unchanged)
# Initial state [x, y, theta]
q = np.array([x, y, theta])

# Control input [v, omega]
u = np.array([0.0, 0.0])

# Robot dimensions
length = 0.1
width = 0.2

# Time step
dt = 0.1

# Control limits
v_max = 0.3
v_min = -0.3
phi_max = 0.9
phi_min = -0.9


def differential_drive_model(q, u):
    dq = np.zeros_like(q)
    dq[0] = u[0] * np.cos(q[2]) * dt
    dq[1] = u[0] * np.sin(q[2]) * dt
    dq[2] = u[1] * dt
    return dq


def on_key(event):
    global u
    if event.key == 'up':
        u[0] = np.clip(u[0] + 0.1, v_min, v_max)
    elif event.key == 'down':
        u[0] = np.clip(u[0] - 0.1, v_min, v_max)
    elif event.key == 'right':
        u[1] = np.clip(u[1] + 0.2, phi_min, phi_max)
    elif event.key == 'left':
        u[1] = np.clip(u[1] - 0.2, phi_min, phi_max)


def draw_rotated_rectangle(ax, center, width, height, angle_degrees, color='b'):
    x, y = center
    rect = patches.Rectangle((x - width / 2, y - height / 2), width, height, linewidth=1, edgecolor=color,
                             facecolor='none')
    t = Affine2D().rotate_deg_around(x, y, angle_degrees) + ax.transData
    rect.set_transform(t)
    ax.add_patch(rect)
# Create a folder to store control sequences
if not os.path.exists("controls"):
    os.makedirs("controls")

# Initialize plot
fig, ax = plt.subplots(figsize=(6, 6))
fig.canvas.mpl_connect('key_press_event', on_key)

# Initialize variables for control sequence
control_sequence = []
current_control = np.array([0.0, 0.0])  # Initial control

# Simulation duration and steps
total_steps = 200
total_duration = 20.0
steps_per_sequence = 20
dt = total_duration / total_steps

for step in range(total_steps):
    # Update state
    dq = differential_drive_model(q, current_control)
    q += dq

    # Check if the robot is within the boundaries
    if q[0] < 0.2 or q[0] > 1.8 or q[1] < 0.2 or q[1] > 1.8:
        # If the robot gets too close to the boundary, resample control
        current_control = np.random.uniform(low=[v_min, phi_min], high=[v_max, phi_max])
        continue

    # Visualization
    plt.clf()
    ax = plt.gca()
    plt.xlim(0, 2)
    plt.ylim(0, 2)

    # Draw robot body
    draw_rotated_rectangle(ax, [q[0], q[1]], length, width, np.degrees(q[2]))

    plt.pause(0.05)

    # Store control in the sequence

    control_sequence.append(current_control.copy())

    # Change control every steps_per_sequence steps
    if (step + 1) % steps_per_sequence == 0:
        current_control = np.random.uniform(low=[v_min, phi_min], high=[v_max, phi_max])

# Save the control sequence to a file
control_sequence.insert(0, q)
control_sequence = np.array(control_sequence, dtype=object)
np.save(os.path.join("controls", "controls_X_Y.npy"), control_sequence)
