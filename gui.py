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
background = pygame.image.load("assets/maze_bg.png")
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load rat images
rat_images = {}
directions = ['top', 'top_right', 'right', 'bottom_right', 'bottom', 'bottom_left', 'left', 'top_left']
try:
    for direction in directions:
        img = pygame.image.load(f"assets/rat/rat_{direction}.png")
        rat_images[direction] = pygame.transform.scale(img, (72, 72))
except Exception as e:
    print(f"Error loading rat images: {e}")
    pygame.quit()
    exit()

# Set indices for all nodes
for i, node in enumerate(nodes):
    node.index = i

def determine_direction(dx, dy):
    if dx > 0:
        if dy > 0:
            return 'bottom_right'
        elif dy < 0:
            return 'top_right'
        else:
            return 'right'
    elif dx < 0:
        if dy > 0:
            return 'bottom_left'
        elif dy < 0:
            return 'top_left'
        else:
            return 'left'
    else:
        if dy > 0:
            return 'bottom'
        elif dy < 0:
            return 'top'
        else:
            return 'right'  # Default case

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
    time.sleep(0.1)

# Main game loop
clock = pygame.time.Clock()
running = True
astar = None
search_started = False

# Animation variables
animating = False
current_path = []
current_segment = 0
current_rat_image = None
start_pos = (0, 0)
end_pos = (0, 0)
progress = 0.0
animation_speed = 1.0  # Adjust speed as needed

while running:
    delta_time = clock.tick(60) / 1000.0  # Delta time in seconds

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
                    current_path = path
                    if len(current_path) >= 2:
                        animating = True
                        current_segment = 0
                        start_node = nodes[current_path[0]]
                        end_node = nodes[current_path[1]]
                        start_pos = (start_node.x, start_node.y)
                        end_pos = (end_node.x, end_node.y)
                        dx = end_node.x - start_node.x
                        dy = end_node.y - start_node.y
                        current_rat_image = rat_images[determine_direction(dx, dy)]
                        progress = 0.0
                else:
                    print("No path found")

    # Update animation
    if animating:
        progress += animation_speed * delta_time
        if progress >= 1.0:
            current_segment += 1
            if current_segment >= len(current_path) - 1:
                animating = False
            else:
                start_node = nodes[current_path[current_segment]]
                end_node = nodes[current_path[current_segment + 1]]
                start_pos = (start_node.x, start_node.y)
                end_pos = (end_node.x, end_node.y)
                dx = end_node.x - start_node.x
                dy = end_node.y - start_node.y
                current_rat_image = rat_images[determine_direction(dx, dy)]
                progress = 0.0

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

    # Draw rat
    if animating and current_rat_image:
        current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        rat_rect = current_rat_image.get_rect(center=(current_x, current_y))
        screen.blit(current_rat_image, rat_rect)

    pygame.display.flip()

# Quit Pygame
pygame.quit()