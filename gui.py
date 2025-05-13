import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame with Background")

# Node class to represent positions in the maze
class Node:
    def __init__(self, x, y, radius=10, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

# Define node positions (you can adjust these coordinates based on your maze)
nodes = [
    Node(90, 72),   
    Node(152, 72), # down 1
    Node(190, 72), # center 1  
    Node(152, 160), # left 1
    Node(53, 160),  # down 2
    Node(53, 250),  # right 1
    Node(152, 250), # down 3
    Node(152, 348), # left 2
    Node(53, 348),  # down 4
    Node(53, 440),  # down 5
    Node(53, 528),  # down 6
    Node(53, 625),  # down 7
    Node(152, 625), # right 2
    Node(220, 625), # right 3
    Node(220, 533), # up 1       
    Node(290, 533), # right 4
    Node(220, 440), # up 2
    Node(120, 440), # left 3
    Node(120, 528), # down 8
    Node(155, 528), # right 5
    Node(220, 348), # up 3
    Node(290, 348), # right 6
    Node(290, 440), # down 9
    Node(390, 440), # right 7
    Node(390, 533), # down 10
    Node(358, 533), # left 4
    Node(358, 625), # down 11
    Node(290, 625), # right 8
    Node(320, 348), # right 9
    Node(390, 348), # right 10
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
]

# Load and scale the background image
# Note: You'll need to replace 'background.jpg' with your actual image file
background = pygame.image.load('maze_bg.png')
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the background
    screen.blit(background, (0, 0))
    
    # Draw all nodes
    for node in nodes:
        node.draw(screen)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

