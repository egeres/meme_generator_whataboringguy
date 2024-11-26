import random
from heapq import heappop, heappush

import numpy as np


def foo_random(N: int = 10, radius: float = 0.5):
    """
    Places N circles on a plane starting from the center,
    ensuring no overlap and each new circle is as close as
    possible to the center, with a more random distribution.

    Parameters:
    - N (int): Number of circles to place.
    - radius (float): Radius of each circle.

    Returns:
    - placed_circles (list of tuples): Coordinates of the placed circles.
    """
    r = radius
    placed_circles = [(0.0, 0.0)]  # Starting with the center point
    potential_positions = []  # Min-heap for potential positions
    considered_positions = set()  # To avoid re-processing positions

    # Function to generate random neighboring positions around a given circle
    def get_random_neighbors(x, y, r, num_neighbors=8):
        positions = []
        for _ in range(num_neighbors):
            angle_deg = random.uniform(0, 360)
            theta = np.deg2rad(angle_deg)
            x_new = x + 2 * r * np.cos(theta)
            y_new = y + 2 * r * np.sin(theta)
            positions.append((x_new, y_new))
        return positions

    # Initialize potential positions with random neighbors of the center circle
    initial_neighbors = get_random_neighbors(0.0, 0.0, r)
    for pos in initial_neighbors:
        dist_to_center = np.hypot(pos[0], pos[1])
        heappush(potential_positions, (dist_to_center, pos))
        considered_positions.add((round(pos[0], 8), round(pos[1], 8)))

    while len(placed_circles) < N:
        if not potential_positions:
            print("Ran out of potential positions before reaching N circles.")
            break

        # Get the closest potential position
        dist, pos = heappop(potential_positions)
        overlaps = False

        # Check for overlaps with existing circles
        for existing_pos in placed_circles:
            dx = pos[0] - existing_pos[0]
            dy = pos[1] - existing_pos[1]
            center_distance = np.hypot(dx, dy)
            if center_distance < 2 * r - 1e-6:
                overlaps = True
                break

        if not overlaps:
            placed_circles.append(pos)
            # Generate random neighbors for the new circle
            neighbors = get_random_neighbors(pos[0], pos[1], r)
            for neighbor in neighbors:
                neighbor_rounded = (round(neighbor[0], 8), round(neighbor[1], 8))
                if neighbor_rounded not in considered_positions:
                    dist_to_center = np.hypot(neighbor[0], neighbor[1])
                    heappush(potential_positions, (dist_to_center, neighbor))
                    considered_positions.add(neighbor_rounded)

    return placed_circles
