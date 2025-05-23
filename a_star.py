import heapq
from gui import Visualizer
from node import Node, nodes
import pygame
import sys
from rich import print

# Helper function to find a node by its position in the graph
def get_node_by_position(position):
    for node in nodes:
        if node.position == position:
            return node
    return None

# Restores the state of all nodes from a snapshot
# Used when navigating backwards through the algorithm steps
def restore_nodes(snapshot):
    for node, (g, h, f, parent_idx) in zip(nodes, snapshot):
        node.g = g
        node.h = h
        node.f = f
        node.parent = nodes[parent_idx] if parent_idx is not None else None

# Main A* algorithm implementation
def a_star(start_pos, goal_pos):
    # Initialize data structures
    open_heap = []  # Priority queue for nodes to be evaluated
    open_set = set()  # Set to track nodes in open_heap
    closed_set = set()  # Set of evaluated nodes
    g_score = {}  # Cost from start to current node
    f_score = {}  # Estimated total cost from start to goal through current node

    # Get start and goal nodes
    start_node = get_node_by_position(start_pos)
    goal_node = get_node_by_position(goal_pos)

    # Helper function to create a snapshot of node states
    def snapshot_nodes():
        return [
            (node.g, node.h, node.f, node.parent.index if node.parent else None)
            for node in nodes
        ]

    # Initialize all nodes
    for node in nodes:
        node.g = float("inf")  # Cost from start to node
        node.h = 0  # Heuristic cost from node to goal
        node.f = float("inf")  # Total cost (g + h)
        node.parent = None  # Parent node for path reconstruction

    # Initialize start node
    start_node.g = 0
    start_node.h = Node.manhattan_distance(start_node, goal_node)
    start_node.f = start_node.g + start_node.h

    # Add start node to open set
    g_score[start_node.index] = 0
    f_score[start_node.index] = start_node.f
    heapq.heappush(open_heap, (start_node.f, start_node.h, start_node.index))
    open_set.add(start_node.index)

    steps = []  # Store algorithm steps for visualization

    # Main A* loop
    while open_heap:
        # Get node with lowest f-score
        current_f, current_h, current_idx = heapq.heappop(open_heap)
        current_node = nodes[current_idx]

        # Skip if node was already evaluated
        if current_node.position in closed_set:
            continue

        # Check if goal is reached
        if current_node.position == goal_pos:
            path = current_node.get_path()
            # Record path visualization steps
            for i in range(len(path)):
                steps.append(
                    (
                        current_node,
                        [nodes[i] for _, _, i in open_heap],
                        set(closed_set),
                        path[: i + 1],
                        [f"Path step {i + 1}/{len(path)}: {path[: i + 1]}"],
                        snapshot_nodes(),
                    )
                )
            # Record final path information
            path_with_indices = [
                f"Node {next(n.index for n in nodes if n.position == step)}: {step} "
                for step in path
            ]
            steps.append(
                (
                    current_node,
                    [nodes[i] for _, _, i in open_heap],
                    set(closed_set),
                    path,
                    [
                        "\nPath found!",
                        f"Path length: {len(path)}",
                        f"Total cost (g): {current_node.g}",
                        "Path (from start to goal):",
                        *path_with_indices,
                    ],
                    snapshot_nodes(),
                )
            )
            return steps

        # Add current node to closed set
        closed_set.add(current_node.position)

        # Evaluate neighbors
        for neighbor_idx in current_node.neighbors:
            neighbor_node = nodes[neighbor_idx]
            if neighbor_node.position in closed_set:
                continue

            # Calculate tentative g-score
            tentative_g = current_node.g + Node.manhattan_distance(
                current_node, neighbor_node
            )
            
            # Update neighbor if better path found
            if tentative_g < getattr(neighbor_node, "g", float("inf")):
                neighbor_node.g = tentative_g
                neighbor_node.h = Node.manhattan_distance(neighbor_node, goal_node)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                neighbor_node.parent = current_node

                # Update scores
                g_score[neighbor_idx] = tentative_g
                f_score[neighbor_idx] = neighbor_node.f

                # Add to open set if not already there
                heapq.heappush(
                    open_heap, (neighbor_node.f, neighbor_node.h, neighbor_idx)
                )
                open_set.add(neighbor_idx)

        # Record current step for visualization
        open_candidates = sorted(open_heap)
        next_nodes_log = ["Possible next nodes after neighbor expansion:"]
        for f_val, h_val, idx in open_candidates:
            node = nodes[idx]
            g_val = f"{node.g:.0f}" if node.g != float("inf") else "inf"
            h_val_str = f"{node.h:.0f}" if node.h != float("inf") else "inf"
            next_nodes_log.append(
                f"  Node {node.index} at {node.position}: f={f_val:.0f}, g={g_val}, h={h_val_str}"
            )

        steps.append(
            (
                current_node,
                [nodes[i] for _, _, i in open_heap],
                set(closed_set),
                None,
                next_nodes_log,
                snapshot_nodes(),
            )
        )

    return steps

# Main program entry point
if __name__ == "__main__":
    # Set start and goal positions
    start = nodes[0].position
    goal = nodes[-1].position

    # Run A* algorithm
    steps = a_star(start, goal)
    if not steps:
        print("No path found.")
        sys.exit()

    # Initialize visualization
    step_idx = 0
    total_steps = len(steps)
    visualizer = Visualizer(nodes, start, goal, algorithm_name="A* Search")

    # Display initial state
    current_node, open_set, closed_set, path, log_lines, node_snapshot = steps[step_idx]
    restore_nodes(node_snapshot)
    visualizer.update_display(current_node, open_set, closed_set, path, delay=0)
    if not (
        log_lines
        and (log_lines[0].startswith("Path step") or "Path found!" in log_lines[0])
    ):
        print(
            f"\nChosen node: {current_node.index} at {current_node.position} (f={current_node.f:.0f}, g={current_node.g:.0f}, h={current_node.h:.0f})"
        )
    print("\n".join(log_lines))

    # Main visualization loop
    clock = pygame.time.Clock()
    while True:
        delta_time = clock.tick(60) / 1000.0

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Handle step navigation
                if event.key == pygame.K_RIGHT:
                    if step_idx < total_steps - 1:
                        step_idx += 1
                        (
                            current_node,
                            open_set,
                            closed_set,
                            path,
                            log_lines,
                            node_snapshot,
                        ) = steps[step_idx]
                        restore_nodes(node_snapshot)
                        visualizer.update_display(
                            current_node, open_set, closed_set, path, delay=0
                        )
                        if not (
                            log_lines
                            and (
                                log_lines[0].startswith("Path step")
                                or "Path found!" in log_lines[0]
                            )
                        ):
                            print(
                                f"\nChosen node: {current_node.index} at {current_node.position} (f={current_node.f:.0f}, g={current_node.g:.0f}, h={current_node.h:.0f})"
                            )
                        print("\n".join(log_lines))
                        if step_idx == total_steps - 1 and path:
                            visualizer.start_animation(path)
                elif event.key == pygame.K_LEFT:
                    if step_idx > 0:
                        step_idx -= 1
                        (
                            current_node,
                            open_set,
                            closed_set,
                            path,
                            log_lines,
                            node_snapshot,
                        ) = steps[step_idx]
                        restore_nodes(node_snapshot)
                        visualizer.update_display(
                            current_node, open_set, closed_set, path, delay=0
                        )
                        if not (
                            log_lines
                            and (
                                log_lines[0].startswith("Path step")
                                or "Path found!" in log_lines[0]
                            )
                        ):
                            print(
                                f"\nChosen node: {current_node.index} at {current_node.position} (f={current_node.f:.0f}, g={current_node.g:.0f}, h={current_node.h:.0f})"
                            )
                        print("\n".join(log_lines))
                        visualizer.animating = False

        # Handle animation
        if visualizer.animating:
            visualizer.progress += visualizer.animation_speed * delta_time
            if visualizer.progress >= 1.0:
                visualizer.current_segment += 1
                if visualizer.current_segment >= len(visualizer.current_path) - 1:
                    visualizer.animating = False
                    visualizer.progress = 1.0
                else:
                    start_pos = visualizer.current_path[visualizer.current_segment]
                    end_pos = visualizer.current_path[visualizer.current_segment + 1]
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    visualizer.current_direction = visualizer.determine_direction(
                        dx, dy
                    )
                    visualizer.progress = 0.0
            visualizer.draw_nodes(
                visualizer.current_node,
                visualizer.open_set,
                visualizer.closed_set,
                visualizer.path,
            )

        pygame.display.flip()
