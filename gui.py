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

