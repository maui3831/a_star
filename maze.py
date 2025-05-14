import heapq
import math
import pygame


# Node class to represent positions in the maze
class Node:
    def __init__(self, x, y, radius=10, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.neighbors = []
        self.index = None
        self.state = "normal"  # normal, exploring, considering, path

    def draw(self, surface):
        # Set color based on state
        if self.state == "normal":
            color = (255, 0, 0)  # Red
        elif self.state == "exploring":
            color = (0, 0, 255)  # Blue
        elif self.state == "considering":
            color = (255, 255, 0)  # Yellow
        elif self.state == "path":
            color = (0, 255, 0)  # Green
        else:
            color = self.color

        # Draw the circle
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)

        # Draw the index number if it exists
        if self.index is not None:
            font = pygame.font.SysFont("Arial", 12)
            text = font.render(str(self.index), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)


# Define node positions
nodes = [
    Node(90, 72),  # start node
    Node(152, 72),
    Node(190, 72),
    Node(152, 160),
    Node(53, 160),
    Node(53, 250),
    Node(152, 250),
    Node(152, 348),
    Node(53, 348),
    Node(53, 440),
    Node(53, 528),
    Node(53, 630),
    Node(152, 630),
    Node(220, 630),
    Node(220, 533),
    Node(290, 533),
    Node(220, 440),
    Node(120, 440),
    Node(120, 528),
    Node(155, 528),
    Node(220, 348),
    Node(290, 348),
    Node(290, 440),
    Node(390, 440),
    Node(390, 533),
    Node(358, 533),
    Node(358, 630),
    Node(290, 630),
    Node(320, 348),
    Node(390, 348),
    Node(390, 250),
    Node(320, 250),
    Node(223, 250),
    Node(223, 160),
    Node(390, 160),
    Node(287, 160),
    Node(287, 72),
    Node(390, 72),
    Node(255, 72),
    Node(458, 533),
    Node(458, 440),
    Node(458, 348),
    Node(525, 348),
    Node(525, 250),
    Node(525, 213),
    Node(598, 213),
    Node(598, 160),
    Node(525, 72),
    Node(458, 72),
    Node(458, 160),
    Node(525, 400),
    Node(525, 495),
    Node(525, 585),
    Node(525, 630),
    Node(435, 630),
    Node(598, 585),
    Node(598, 630),
    Node(668, 72),
    Node(668, 115),
    Node(598, 400),
    Node(598, 495),
    Node(598, 305),
    Node(665, 305),
    Node(703, 305),
    Node(703, 260),
    Node(703, 210),
    Node(668, 210),
    Node(773, 260),
    Node(773, 210),
    Node(810, 210),
    Node(848, 210),
    Node(810, 72),
    Node(738, 72),
    Node(738, 115),
    Node(773, 400),
    Node(848, 400),
    Node(848, 305),
    Node(848, 535),
    Node(848, 630),
    Node(738, 630),
    Node(738, 585),
    Node(665, 630),
    Node(665, 495),
    Node(773, 495),
    Node(665, 400),
    Node(703, 400),
    Node(880, 535),  # finish
]

# Set indices for all nodes
for i, node in enumerate(nodes):
    node.index = i

# Define connections between nodes
connections = {
    0: [1],
    1: [0, 2, 3],
    2: [1],
    3: [4, 1, 33],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [7, 9],
    9: [8, 10],
    10: [9, 11],
    11: [10, 12],
    12: [11, 13],
    13: [12, 14],
    14: [13, 15, 16],
    16: [14, 17, 20],
    17: [16, 18],
    18: [17, 19],
    19: [18],
    20: [16, 21],
    21: [20, 22, 28],
    22: [21, 23],
    23: [22, 24],
    24: [23, 25, 39],
    25: [26, 24],
    26: [25, 27],
    27: [26],
    28: [21, 29, 31],
    29: [28, 30],
    30: [29, 34, 43],
    31: [28, 32],
    32: [31, 33],
    33: [3, 32, 35],
    34: [30, 35],
    35: [33, 34, 36],
    36: [35, 38, 37],
    37: [36],
    38: [36],
    39: [24, 40],
    40: [39, 41],
    41: [40, 42],
    42: [41, 43, 50],
    43: [30, 42, 44],
    44: [43, 45, 47],
    45: [44, 46],
    46: [45],
    47: [44, 48, 57],
    48: [47, 49],
    49: [48],
    50: [42, 51, 59],
    51: [50, 52, 60],
    52: [51, 53, 55],
    53: [52, 54],
    54: [53],
    55: [52, 56],
    56: [55],
    57: [47, 58],
    58: [57],
    59: [50, 61],
    60: [51, 82],
    61: [59, 62],
    62: [61, 63, 84],
    63: [62, 64],
    64: [65, 67],
    65: [64, 66],
    66: [65],
    67: [64, 68, 74],
    68: [67, 69],
    69: [68, 70, 71],
    70: [69],
    71: [69, 72],
    72: [71, 73],
    73: [72],
    74: [67, 75],
    75: [74, 76, 77],
    76: [75],
    77: [78, 86],
    78: [77, 79],
    79: [78, 80, 81],
    80: [79],
    81: [79, 82],
    82: [60, 81, 83, 84],
    83: [82],
    84: [62, 82, 85],
    85: [84],
    86: [77],
}


class AStar:
    def __init__(self, start_idx, goal_idx):
        self.start_idx = start_idx
        self.goal_idx = goal_idx
        self.start_node = nodes[start_idx]
        self.goal_node = nodes[goal_idx]

    def heuristic(self, node1, node2):
        # Manhattan distance
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def get_neighbors(self, node_idx):
        return connections.get(node_idx, [])

    def reconstruct_path(self, came_from, current_idx):
        path = []
        while current_idx in came_from:
            path.append(current_idx)
            current_idx = came_from[current_idx]
        path.append(self.start_idx)
        path.reverse()
        return path

    def search(self, gui_callback=None):
        # Initialize open and closed sets
        open_set = []
        closed_set = set()

        # Initialize g_score and f_score dictionaries
        g_score = {self.start_idx: 0}
        f_score = {self.start_idx: self.heuristic(self.start_node, self.goal_node)}

        # Add start node to open set
        heapq.heappush(open_set, (f_score[self.start_idx], self.start_idx))

        # Dictionary to store the path
        came_from = {}

        while open_set:
            # Get node with lowest f_score
            current_f, current_idx = heapq.heappop(open_set)
            current_node = nodes[current_idx]

            # Visualize current node being explored
            if gui_callback:
                gui_callback(current_idx, "exploring")

            # Check if we reached the goal
            if current_idx == self.goal_idx:
                path = self.reconstruct_path(came_from, current_idx)
                # Visualize final path
                if gui_callback:
                    for node_idx in path:
                        gui_callback(node_idx, "path")
                return path

            # Add current node to closed set
            closed_set.add(current_idx)

            # Check all neighbors
            for neighbor_idx in self.get_neighbors(current_idx):
                if neighbor_idx in closed_set:
                    continue

                # Calculate tentative g_score
                tentative_g_score = g_score[current_idx] + self.heuristic(
                    current_node, nodes[neighbor_idx]
                )

                # Visualize neighbor being considered
                if gui_callback:
                    gui_callback(neighbor_idx, "considering")

                if (
                    neighbor_idx not in g_score
                    or tentative_g_score < g_score[neighbor_idx]
                ):
                    # This path is better, record it
                    came_from[neighbor_idx] = current_idx
                    g_score[neighbor_idx] = tentative_g_score
                    f_score[neighbor_idx] = tentative_g_score + self.heuristic(
                        nodes[neighbor_idx], self.goal_node
                    )

                    if neighbor_idx not in [idx for _, idx in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor_idx], neighbor_idx))

        return None  # No path found
