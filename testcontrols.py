import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
# Robot dimensions
# Simulation parameters
dt = 0.1
length = 0.1
width = 0.2
landmarks_map = np.load("maps/landmarks_0.npy")
def differential_drive_model(q, u):
    dq = np.zeros_like(q)
    dq[0] = u[0] * np.cos(q[2]) * dt
    dq[1] = u[0] * np.sin(q[2]) * dt
    dq[2] = u[1] * dt
    return dq

def draw_rotated_rectangle(ax, center, width, height, angle_degrees, color='b'):
    x, y = center
    rect = patches.Rectangle((x - width / 2, y - height / 2), width, height, linewidth=1, edgecolor=color,
                             facecolor='none')
    t = Affine2D().rotate_deg_around(x, y, angle_degrees) + ax.transData
    rect.set_transform(t)
    ax.add_patch(rect)

def animate_robot_trajectory(trajectory, control_sequence, landmarks_map, length, width):
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.xlim(0, 2)
    plt.ylim(0, 2)

    for i in range(len(trajectory)):
        q = trajectory[i]

        plt.clf()
        ax = plt.gca()
        plt.xlim(0, 2)
        plt.ylim(0, 2)

        # Draw path
        path_array = np.array(trajectory[:i+1])
        plt.plot(path_array[:, 0], path_array[:, 1], color='green', linestyle='--', linewidth=2)

        # Draw robot body
        draw_rotated_rectangle(ax, [q[0], q[1]], length, width, np.degrees(q[2]))
        plt.scatter(landmarks_map[:, 0], landmarks_map[:, 1], marker='o', label='Landmarks Map 1')
        plt.pause(0.05)

    plt.show()

if __name__ == "__main__":
    # Load control sequence
    control_sequence = np.load("controls/controls_X_Y.npy", allow_pickle=True)
    initial_location = control_sequence[0]
    control_sequence = control_sequence[1:]

    # Initialize variables
    q = initial_location
    trajectory = []
    print("initial- ", q)


    # Simulate robot movement
    for i in range(len(control_sequence)):
        dq = differential_drive_model(q, control_sequence[i])
        q += dq
        trajectory.append([q[0], q[1], q[2]])
        print(f"Trajectory position-{i}  ", q[0], q[1], q[2])

    # Animate the robot trajectory
    animate_robot_trajectory(trajectory, control_sequence, landmarks_map, length, width)
