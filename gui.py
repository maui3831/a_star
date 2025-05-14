import pygame
import time
from maze import nodes, connections, AStar

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# Initialize font
pygame.font.init()
font = pygame.font.SysFont("Arial", 12)

# Load and scale the background image
background = pygame.image.load("maze_bg.png")
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Set indices for all nodes
for i, node in enumerate(nodes):
    node.index = i


def update_node_state(node_idx, state):
    nodes[node_idx].state = state
    # Draw everything
    screen.blit(background, (0, 0))

    # Draw connections
    for node_idx, neighbors in connections.items():
        start_node = nodes[node_idx]
        for neighbor_idx in neighbors:
            end_node = nodes[neighbor_idx]
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (start_node.x, start_node.y),
                (end_node.x, end_node.y),
                2,
            )

    # Draw all nodes
    for node in nodes:
        node.draw(screen)

    pygame.display.flip()
    time.sleep(0.1)  # Add a small delay to make the visualization visible


# Main game loop
running = True
astar = None
search_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not search_started:
                # Start A* search from node 0 to the last node
                astar = AStar(0, len(nodes) - 1)
                search_started = True
                # Run the search with visualization
                path = astar.search(update_node_state)
                if path:
                    print(f"Path found: {path}")
                else:
                    print("No path found")

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw connections
    for node_idx, neighbors in connections.items():
        start_node = nodes[node_idx]
        for neighbor_idx in neighbors:
            end_node = nodes[neighbor_idx]
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (start_node.x, start_node.y),
                (end_node.x, end_node.y),
                2,
            )

    # Draw all nodes
    for node in nodes:
        node.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
