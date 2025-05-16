import unittest
from a_star import a_star
from bfs import breadth_first_search
from node import Node, nodes

class TestAStar(unittest.TestCase):
    def setUp(self):
        # Set up start and goal positions
        self.start = nodes[0].position
        self.goal = nodes[-1].position

    def test_heuristic_admissibility(self):
        """Test that the Manhattan distance heuristic never overestimates the actual cost."""
        for node in nodes:
            # Get actual shortest path cost using BFS
            bfs_steps = breadth_first_search(node.position, self.goal)
            if bfs_steps and "Path found!" in bfs_steps[-1][4][0]:
                actual_cost = float(bfs_steps[-1][4][2].split(": ")[1])
                
                # Get heuristic estimate
                heuristic_cost = Node.manhattan_distance(node, nodes[-1])
                
                # Heuristic should never overestimate
                self.assertLessEqual(heuristic_cost, actual_cost,
                    f"Heuristic overestimates cost for node {node.index} at {node.position}")

    def test_path_optimality(self):
        """Test that A* finds the same path length as BFS."""
        # Get A* path
        a_star_steps = a_star(self.start, self.goal)
        a_star_path_length = len(a_star_steps[-1][3]) if a_star_steps else 0
        
        # Get BFS path
        bfs_steps = breadth_first_search(self.start, self.goal)
        bfs_path_length = len(bfs_steps[-1][3]) if bfs_steps else 0
        
        # Both should find a path
        self.assertTrue(a_star_path_length > 0, "A* did not find a path")
        self.assertTrue(bfs_path_length > 0, "BFS did not find a path")
        
        # Path lengths should be equal
        self.assertEqual(a_star_path_length, bfs_path_length,
            "A* path length differs from BFS path length")

    def test_f_score_property(self):
        """Test that f = g + h for all nodes in the final path."""
        a_star_steps = a_star(self.start, self.goal)
        if not a_star_steps:
            self.fail("A* did not find a path")
            
        # Get the final path
        final_path = a_star_steps[-1][3]
        
        # Check f = g + h for each node in the path
        for position in final_path:
            node = next(n for n in nodes if n.position == position)
            self.assertEqual(node.f, node.g + node.h,
                f"f != g + h for node {node.index} at {node.position}")

    def test_path_continuity(self):
        """Test that the path is continuous (each node is connected to the next)."""
        a_star_steps = a_star(self.start, self.goal)
        if not a_star_steps:
            self.fail("A* did not find a path")
            
        # Get the final path
        final_path = a_star_steps[-1][3]
        
        # Check that each consecutive pair of nodes is connected
        for i in range(len(final_path) - 1):
            current_pos = final_path[i]
            next_pos = final_path[i + 1]
            
            current_node = next(n for n in nodes if n.position == current_pos)
            next_node = next(n for n in nodes if n.position == next_pos)
            
            self.assertIn(next_node.index, current_node.neighbors,
                f"Path is not continuous between nodes {current_node.index} and {next_node.index}")

if __name__ == '__main__':
    unittest.main() 