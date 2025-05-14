import heapq
import math
from gui import Node, nodes, connections

class AStar:
    def __init__(self, start_idx, goal_idx):
        self.start_idx = start_idx
        self.goal_idx = goal_idx
        self.start_node = nodes[start_idx]
        self.goal_node = nodes[goal_idx]
        
    def heuristic(self, node1, node2):
        # Euclidean distance heuristic
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    
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
                tentative_g_score = g_score[current_idx] + self.heuristic(current_node, nodes[neighbor_idx])
                
                # Visualize neighbor being considered
                if gui_callback:
                    gui_callback(neighbor_idx, "considering")
                
                if neighbor_idx not in g_score or tentative_g_score < g_score[neighbor_idx]:
                    # This path is better, record it
                    came_from[neighbor_idx] = current_idx
                    g_score[neighbor_idx] = tentative_g_score
                    f_score[neighbor_idx] = tentative_g_score + self.heuristic(nodes[neighbor_idx], self.goal_node)
                    
                    if neighbor_idx not in [idx for _, idx in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor_idx], neighbor_idx))
        
        return None  # No path found
