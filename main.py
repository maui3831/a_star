import heapq
from typing import List, Tuple, Set, Dict
import random

class Node:
    def __init__(self, x: int, y: int, g_cost: float = float('inf'), h_cost: float = 0):
        self.x = x
        self.y = y
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Heuristic cost from current node to goal
        self.parent = None    # Parent node for path reconstruction
        
    @property
    def f_cost(self) -> float:
        return self.g_cost + self.h_cost
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class Maze:
    def __init__(self, width: int, height: int, wall_probability: float = 0.3):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.start = None
        self.goal = None
        self.generate_maze(wall_probability)
    
    def generate_maze(self, wall_probability: float):
        # Generate random walls
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < wall_probability:
                    self.grid[y][x] = 1
        
        # Ensure start and goal are not walls
        while True:
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            if self.grid[start_y][start_x] == 0:
                self.start = Node(start_x, start_y)
                break
        
        while True:
            goal_x = random.randint(0, self.width - 1)
            goal_y = random.randint(0, self.height - 1)
            if self.grid[goal_y][goal_x] == 0 and (goal_x != start_x or goal_y != start_y):
                self.goal = Node(goal_x, goal_y)
                break
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == 0
    
    def get_neighbors(self, node: Node) -> List[Node]:
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            if self.is_valid_position(new_x, new_y):
                neighbors.append(Node(new_x, new_y))
        
        return neighbors
    
    def manhattan_distance(self, node1: Node, node2: Node) -> float:
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)
    
    def print_maze(self, path: List[Node] = None):
        if path is None:
            path = []
        
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == (self.start.x, self.start.y):
                    print('S', end=' ')
                elif (x, y) == (self.goal.x, self.goal.y):
                    print('G', end=' ')
                elif any(node.x == x and node.y == y for node in path):
                    print('*', end=' ')
                elif self.grid[y][x] == 1:
                    print('#', end=' ')
                else:
                    print('.', end=' ')
            print()

def a_star(maze: Maze) -> List[Node]:
    # Initialize open and closed sets
    open_set = []
    closed_set = set()
    
    # Initialize start node
    start_node = maze.start
    start_node.g_cost = 0
    start_node.h_cost = maze.manhattan_distance(start_node, maze.goal)
    
    # Add start node to open set
    heapq.heappush(open_set, start_node)
    
    while open_set:
        current = heapq.heappop(open_set)
        
        # If we reached the goal, reconstruct and return the path
        if current == maze.goal:
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]
        
        closed_set.add(current)
        
        # Check all neighbors
        for neighbor in maze.get_neighbors(current):
            if neighbor in closed_set:
                continue
            
            # Calculate new g_cost
            new_g_cost = current.g_cost + 1
            
            if neighbor not in open_set or new_g_cost < neighbor.g_cost:
                neighbor.g_cost = new_g_cost
                neighbor.h_cost = maze.manhattan_distance(neighbor, maze.goal)
                neighbor.parent = current
                
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)
    
    return []  # No path found

def main():
    # Create a maze
    maze = Maze(10, 30)
    
    # Print initial maze
    print("Initial Maze:")
    maze.print_maze()
    print("\nSolving maze...")
    
    # Find path using A*
    path = a_star(maze)
    
    # Print solution
    print("\nSolution:")
    maze.print_maze(path)
    
    if path:
        print(f"\nPath length: {len(path)}")
    else:
        print("\nNo path found!")

if __name__ == "__main__":
    main()


