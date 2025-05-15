import pygame
import sys
from dataclasses import dataclass
from typing import List, Tuple
from node import Node

# Constants
CELL_SIZE = 20
PATH_COLOR = (255, 255, 255)  # White
START_COLOR = (0, 255, 0)  # Green
GOAL_COLOR = (255, 0, 0)  # Red
OPEN_SET_COLOR = (139, 233, 253)  # Cyan
CLOSED_SET_COLOR = (100, 100, 100)  # Dark gray
CURRENT_NODE_COLOR = (255, 121, 198)  # Pink
PATH_COLOR_FINAL = (255, 184, 108)  # Orange


@dataclass
class Visualizer:
    nodes: List[Node]
    start: Tuple[int, int]
    goal: Tuple[int, int]

    def __post_init__(self):
        pygame.init()
        self.width = 900
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_image = pygame.image.load("assets/maze_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        pygame.display.set_caption("A* Search Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 18)  # Main font for f
        self.font_small = pygame.font.SysFont(None, 13)  # Smaller font for h

    def draw_nodes(self, current_node, open_set, closed_set, path=None):
        # Draw background image
        self.screen.blit(self.bg_image, (0, 0))

        # Draw formula at the top
        formula = "f(x) = g(x) + h(x)"
        if current_node:
            g_val = f"{current_node.g:.0f}" if current_node.g != float("inf") else "inf"
            h_val = f"{current_node.h:.0f}" if current_node.h != float("inf") else "inf"
            f_val = f"{current_node.f:.0f}" if current_node.f != float("inf") else "inf"
            formula += f"   |   Current: f={f_val}, g={g_val}, h={h_val}"
        formula_surface = self.font.render(formula, True, (0, 0, 0))
        self.screen.blit(formula_surface, (20, 10))

        # Print to console for logs
        if current_node:
            print(
                f"\nStep: Node {getattr(current_node, 'index', '?')} at {current_node.position} -> f={f_val}, g={g_val}, h={h_val}"
            )

        # Draw connections (edges) between nodes
        for node in self.nodes:
            x1, y1 = node.position
            for neighbor_idx in node.neighbors:
                neighbor = self.nodes[neighbor_idx]
                x2, y2 = neighbor.position
                pygame.draw.line(self.screen, (180, 180, 180), (x1, y1), (x2, y2), 2)

        # Draw all nodes
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

            pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE)

            # Draw f score slightly above center
            f_val = f"{node.f:.0f}" if node.f != float("inf") else "inf"
            f_surface = self.font.render(f_val, True, (0, 0, 0))
            f_rect = f_surface.get_rect(center=(x, y - 5))
            self.screen.blit(f_surface, f_rect)

            # Draw h score below f score, smaller font
            h_val = f"{node.h:.0f}" if node.h != float("inf") else "inf"
            h_surface = self.font_small.render(f"h:{h_val}", True, (0, 0, 200))
            h_rect = h_surface.get_rect(midtop=(x, y + 7))
            self.screen.blit(h_surface, h_rect)

        # Highlight current node
        if current_node:
            x, y = current_node.position
            pygame.draw.circle(
                self.screen,
                CURRENT_NODE_COLOR,
                (x, y),
                CELL_SIZE,
            )

        pygame.display.flip()

    def update_display(self, current_node, open_set, closed_set, path=None, delay=400):
        self.draw_nodes(current_node, open_set, closed_set, path)
        pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
