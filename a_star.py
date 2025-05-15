import heapq
from gui import Visualizer
from node import Node, nodes
import pygame
import sys


def get_node_by_position(position):
    for node in nodes:
        if node.position == position:
            return node
    return None


def a_star(start_pos, goal_pos):
    visualizer = Visualizer(nodes, start_pos, goal_pos)

    open_heap = []
    open_set = set()
    closed_set = set()
    g_score = {}
    f_score = {}

    start_node = get_node_by_position(start_pos)
    goal_node = get_node_by_position(goal_pos)

    # Reset node costs and parents
    for node in nodes:
        node.g = float("inf")
        node.h = 0
        node.f = float("inf")
        node.parent = None

    start_node.g = 0
    start_node.h = Node.manhattan_distance(start_node, goal_node)
    start_node.f = start_node.g + start_node.h

    g_score[start_node.index] = 0
    f_score[start_node.index] = start_node.f

    heapq.heappush(open_heap, (start_node.f, start_node.index))
    open_set.add(start_node.index)

    while open_heap:
        # Print all considered nodes in the open set before choosing
        print("\nOpen set candidates (before selection):")
        open_candidates = sorted(open_heap)
        for f_val, idx in open_candidates:
            node = nodes[idx]
            g_val = f"{node.g:.0f}" if node.g != float("inf") else "inf"
            h_val = f"{node.h:.0f}" if node.h != float("inf") else "inf"
            print(
                f"  Node {node.index} at {node.position}: f={f_val:.0f}, g={g_val}, h={h_val}"
            )

        current_f, current_idx = heapq.heappop(open_heap)
        current_node = nodes[current_idx]

        print(
            f"Chosen node: Node {current_node.index} at {current_node.position} with f={current_f:.0f}"
        )

        # If this node has already been processed with a better f, skip it
        if current_node.position in closed_set:
            continue

        visualizer.update_display(
            current_node, [nodes[i] for _, i in open_heap], closed_set
        )

        if current_node.position == goal_pos:
            path = current_node.get_path()
            for i in range(len(path)):
                visualizer.update_display(
                    current_node,
                    [nodes[i] for _, i in open_heap],
                    closed_set,
                    path[: i + 1],
                    delay=200,
                )
            # Print path found details
            print("\nPath found!")
            print(f"Path length: {len(path)}")
            print(f"Total cost (g): {current_node.g}")
            print("Path (from start to goal):")
            for step in path:
                print(step)
            return path

        closed_set.add(current_node.position)

        for neighbor_idx in current_node.neighbors:
            neighbor_node = nodes[neighbor_idx]
            if neighbor_node.position in closed_set:
                continue

            tentative_g = current_node.g + Node.manhattan_distance(
                current_node, neighbor_node
            )
            if tentative_g < getattr(neighbor_node, "g", float("inf")):
                neighbor_node.g = tentative_g
                neighbor_node.h = Node.manhattan_distance(neighbor_node, goal_node)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                neighbor_node.parent = current_node

                g_score[neighbor_idx] = tentative_g
                f_score[neighbor_idx] = neighbor_node.f

                heapq.heappush(open_heap, (neighbor_node.f, neighbor_idx))
                open_set.add(neighbor_idx)

                visualizer.update_display(
                    current_node, [nodes[i] for _, i in open_heap], closed_set
                )

    return None


if __name__ == "__main__":
    # Select start and goal from nodes
    start = nodes[0].position  # First node
    goal = nodes[-1].position  # Last node

    path = a_star(start, goal)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)
