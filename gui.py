import pygame
import sys
from dataclasses import dataclass
from typing import List, Tuple
from node import Node

# Constants for visualization colors and sizes
CELL_SIZE = 20
PATH_COLOR = (248, 248, 242)  # White
START_COLOR = (80, 250, 123)  # Green
GOAL_COLOR = (241, 250, 140)  # Yellow
OPEN_SET_COLOR = (139, 233, 253)  # Cyan
CLOSED_SET_COLOR = (68, 71, 90)  # Dark gray
CURRENT_NODE_COLOR = (255, 121, 198)  # Pink
PATH_COLOR_FINAL = (255, 184, 108)  # Orange

# Visualizer class for handling the graphical interface
@dataclass
class Visualizer:
    nodes: List[Node]  # List of all nodes in the graph
    start: Tuple[int, int]  # Start position coordinates
    goal: Tuple[int, int]  # Goal position coordinates
    algorithm_name: str = "Pathfinding Visualization" # Default title

    def __post_init__(self):
        # Initialize Pygame and set up the display
        pygame.init()
        self.width = 900
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_image = pygame.image.load("assets/maze_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        pygame.display.set_caption(f"{self.algorithm_name} - Step-by-Step") # Use the algorithm name in caption
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 18)  
        self.font_small = pygame.font.SysFont(None, 13)  
        self.load_rat_images()  
        self.animating = False  
        self.current_path = []  
        self.animation_speed = 1.0  
        pygame.display.set_icon(pygame.image.load("assets/mouse.png"))

    def load_rat_images(self):
        # Load and scale rat sprites for different movement directions
        self.rat_images = {}
        directions = [
            "top",
            "top_right",
            "right",
            "bottom_right",
            "bottom",
            "bottom_left",
            "left",
            "top_left",
        ]
        try:
            for direction in directions:
                img = pygame.image.load(f"assets/rat/rat_{direction}.png")
                self.rat_images[direction] = pygame.transform.scale(img, (72, 72))
        except Exception as e:
            print(f"Error loading rat images: {e}")
            pygame.quit()
            sys.exit()

    def determine_direction(self, dx, dy):
        # Determine the direction of movement based on x and y differences
        if dx > 0 and dy < 0:
            return "top_right"
        elif dx > 0 and dy > 0:
            return "bottom_right"
        elif dx < 0 and dy < 0:
            return "top_left"
        elif dx < 0 and dy > 0:
            return "bottom_left"
        elif dx > 0 and dy == 0:
            return "right"
        elif dx < 0 and dy == 0:
            return "left"
        elif dx == 0 and dy < 0:
            return "top"
        elif dx == 0 and dy > 0:
            return "bottom"
        else:
            return "right"

    def start_animation(self, path):
        # Initialize animation of the rat moving along the path
        if len(path) < 2:
            return
        self.animating = True
        self.current_path = path
        self.current_segment = 0
        self.progress = 0.0
        start_pos = self.current_path[0]
        end_pos = self.current_path[1]
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        self.current_direction = self.determine_direction(dx, dy)

    def draw_nodes(self, current_node, open_set, closed_set, path=None):
        # Draw the background
        self.screen.blit(self.bg_image, (0, 0))

        # Draw the A* formula and current node values
        formula = "f(x) = g(x) + h(x)"
        if current_node:
            g_val = f"{current_node.g:.0f}" if current_node.g != float("inf") else "inf"
            h_val = f"{current_node.h:.0f}" if current_node.h != float("inf") else "inf"
            f_val = f"{current_node.f:.0f}" if current_node.f != float("inf") else "inf"
            formula += f"   |   Current: f={f_val}, g={g_val}, h={h_val}"

        # Draw formula with shadow effect
        x, y = 20, 10
        outline_color = (0, 0, 0)
        text_color = (255, 255, 255)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            shadow = self.font.render(formula, True, outline_color)
            self.screen.blit(shadow, (x + dx, y + dy))
        text_surface = self.font.render(formula, True, text_color)
        self.screen.blit(text_surface, (x, y))

        # Create temporary surface for animation
        if self.animating:
            alpha = 100
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        else:
            temp_surface = self.screen

        # Draw connections between nodes
        for node in self.nodes:
            x1, y1 = node.position
            for neighbor_idx in node.neighbors:
                neighbor = self.nodes[neighbor_idx]
                x2, y2 = neighbor.position
                color = (180, 180, 180, alpha) if self.animating else (180, 180, 180)
                pygame.draw.line(temp_surface, color, (x1, y1), (x2, y2), 2)

        # Draw nodes with their values
        for node in self.nodes:
            x, y = node.position
            color = PATH_COLOR
            if node.position == self.start:
                color = START_COLOR
            elif node.position == self.goal:
                color = GOAL_COLOR
            elif path and (x, y) in path:
                color = PATH_COLOR_FINAL
            elif node.position in closed_set:
                color = CLOSED_SET_COLOR
            elif node in open_set:
                color = OPEN_SET_COLOR

            draw_color = (*color, alpha) if self.animating else color
            pygame.draw.circle(temp_surface, draw_color, (x, y), CELL_SIZE)

            # Draw f-value
            f_val = f"{node.f:.0f}" if node.f != float("inf") else "inf"
            f_surface = self.font.render(f_val, True, (0, 0, 0))
            f_rect = f_surface.get_rect(center=(x, y - 5))
            temp_surface.blit(f_surface, f_rect)

            # Draw h-value
            h_val = f"{node.h:.0f}" if node.h != float("inf") else "inf"
            h_surface = self.font_small.render(f"h:{h_val}", True, (0, 0, 200))
            h_rect = h_surface.get_rect(midtop=(x, y + 7))
            temp_surface.blit(h_surface, h_rect)

        # Apply animation surface if needed
        if self.animating:
            self.screen.blit(temp_surface, (0, 0))

        # Draw current node highlight
        if current_node:
            x, y = current_node.position
            if not (
                self.animating
                and self.current_path
                and current_node.position == self.goal
            ):
                pygame.draw.circle(self.screen, CURRENT_NODE_COLOR, (x, y), CELL_SIZE)

        # Draw animated rat
        if self.animating and self.current_path:
            if self.current_segment < len(self.current_path) - 1:
                start_pos = self.current_path[self.current_segment]
                end_pos = self.current_path[self.current_segment + 1]
                current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * self.progress
                current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * self.progress
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                current_direction = self.determine_direction(dx, dy)
            else:
                current_x, current_y = self.current_path[-1]
                current_direction = self.current_direction
            rat_image = self.rat_images[current_direction]
            rat_rect = rat_image.get_rect(center=(current_x, current_y))
            self.screen.blit(rat_image, rat_rect)

        pygame.display.flip()

    def update_display(self, current_node, open_set, closed_set, path=None, delay=0):
        # Update the visualization with current algorithm state
        self.current_node = current_node
        self.open_set = open_set
        self.closed_set = closed_set
        self.path = path
        self.draw_nodes(current_node, open_set, closed_set, path)
        pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
