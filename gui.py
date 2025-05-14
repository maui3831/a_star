import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame with Background")

# Initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', 12)

# Node class to represent positions in the maze
class Node:
    def __init__(self, x, y, radius=10, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.neighbors = []
        self.index = None  # Will store the node's index

    def draw(self, surface):
        # Draw the circle
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        
        # Draw the index number if it exists
        if self.index is not None:
            text = font.render(str(self.index), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)
        
    def get_position(self):
        return self.x, self.y
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        
    def draw_connections(self, surface):
        for neighbor in self.neighbors:
            pygame.draw.line(surface, (0, 0, 0), (self.x, self.y), (neighbor.x, neighbor.y), 2)
    

# Define node positions (you can adjust these coordinates based on your maze)
nodes = [
    Node(90, 72),   # start node
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
    Node(880, 535), # finish
]

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
    86: [77]
}

# Load and scale the background image
# Note: You'll need to replace 'background.jpg' with your actual image file
background = pygame.image.load('maze_bg.png')
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Set indices for all nodes
for i, node in enumerate(nodes):
    node.index = i

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the background
    screen.blit(background, (0, 0))
    
    # Draw connections first (so they appear behind the nodes)
    for node_idx, neighbors in connections.items():
        start_node = nodes[node_idx]
        for neighbor_idx in neighbors:
            end_node = nodes[neighbor_idx]
            pygame.draw.line(screen, (0, 0, 0), (start_node.x, start_node.y), (end_node.x, end_node.y), 2)
    
    # Draw all nodes
    for node in nodes:
        node.draw(screen)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

