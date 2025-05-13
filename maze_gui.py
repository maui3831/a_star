import pygame
import sys
from main import Maze, a_star

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class MazeGUI:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.path = []
        self.solving = False
        self.solved = False
        
        # Calculate window size
        self.width = maze.width * CELL_SIZE
        self.height = maze.height * CELL_SIZE
        
        # Create window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("A* Maze Solver")
        
        # Create clock for FPS
        self.clock = pygame.time.Clock()
    
    def draw_maze(self):
        self.screen.fill(WHITE)
        
        # Draw walls and open spaces
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze.grid[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)
        
        # Draw start
        start_rect = pygame.Rect(
            self.maze.start.x * CELL_SIZE,
            self.maze.start.y * CELL_SIZE,
            CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(self.screen, GREEN, start_rect)
        
        # Draw goal
        goal_rect = pygame.Rect(
            self.maze.goal.x * CELL_SIZE,
            self.maze.goal.y * CELL_SIZE,
            CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(self.screen, RED, goal_rect)
        
        # Draw path
        for node in self.path:
            path_rect = pygame.Rect(
                node.x * CELL_SIZE,
                node.y * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(self.screen, BLUE, path_rect)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.solving:
                        self.solving = True
                        self.path = a_star(self.maze)
                        self.solved = True
                    elif event.key == pygame.K_r:  # Reset
                        self.maze = Maze(self.maze.width, self.maze.height)
                        self.path = []
                        self.solving = False
                        self.solved = False
            
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    # Create maze
    maze = Maze(30, 30)
    
    # Create and run GUI
    gui = MazeGUI(maze)
    gui.run()

if __name__ == "__main__":
    main() 