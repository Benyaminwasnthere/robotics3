import numpy as np
import matplotlib.pyplot as plt

def visualize_map(landmarks, title):
    plt.scatter(landmarks[:, 0], landmarks[:, 1], marker='o')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.show()

def generate_landmark_map(num_landmarks, name):
    landmarks = np.random.rand(num_landmarks, 2) * 2  # Randomly place landmarks in [0, 2] x [0, 2]
    np.save(f"mapS/landmark_{name}.npy", landmarks)
    return landmarks

# Generate maps with 5 and 12 landmarks
if __name__ == '__main__':
    MAP1 = generate_landmark_map(5, 1)
    MAP2 = generate_landmark_map(5, 2)
    MAP3 = generate_landmark_map(12, 3)
    MAP4 = generate_landmark_map(12, 4)
    visualize_map(MAP1, 'Landmark Map with 5 Landmarks (MAP1)')
    visualize_map(MAP2, 'Landmark Map with 5 Landmarks (MAP2)')
    visualize_map(MAP3, 'Landmark Map with 12 Landmarks (MAP3)')
    visualize_map(MAP4, 'Landmark Map with 12 Landmarks (MAP4)')