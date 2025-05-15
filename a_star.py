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


def restore_nodes(snapshot):
    for node, (g, h, f, parent_idx) in zip(nodes, snapshot):
        node.g = g
        node.h = h
        node.f = f
        node.parent = nodes[parent_idx] if parent_idx is not None else None


def a_star(start_pos, goal_pos):
    visualizer = Visualizer(nodes, start_pos, goal_pos)

    open_heap = []
    open_set = set()
    closed_set = set()
    g_score = {}
    f_score = {}

    start_node = get_node_by_position(start_pos)
    goal_node = get_node_by_position(goal_pos)

    # Helper to snapshot all node values
    def snapshot_nodes():
        return [
            (node.g, node.h, node.f, node.parent.index if node.parent else None)
            for node in nodes
        ]

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

    # Collect steps for visualization
    steps = []

    while open_heap:
        current_f, current_idx = heapq.heappop(open_heap)
        current_node = nodes[current_idx]

        # If this node has already been processed with a better f, skip it
        if current_node.position in closed_set:
            continue

        if current_node.position == goal_pos:
            path = current_node.get_path()
            for i in range(len(path)):
                steps.append(
                    (
                        current_node,
                        [nodes[i] for _, i in open_heap],
                        set(closed_set),
                        path[: i + 1],
                        [f"Path step {i + 1}/{len(path)}: {path[: i + 1]}"],
                        snapshot_nodes(),
                    )
                )
            steps.append(
                (
                    current_node,
                    [nodes[i] for _, i in open_heap],
                    set(closed_set),
                    path,
                    [
                        "\nPath found!",
                        f"Path length: {len(path)}",
                        f"Total cost (g): {current_node.g}",
                        "Path (from start to goal):",
                        *(str(step) for step in path),
                    ],
                    snapshot_nodes(),
                )
            )
            return steps

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

        # Only log the open set after neighbor expansion
        open_candidates = sorted(open_heap)
        next_nodes_log = ["Possible next nodes after neighbor expansion:"]
        for f_val, idx in open_candidates:
            node = nodes[idx]
            g_val = f"{node.g:.0f}" if node.g != float("inf") else "inf"
            h_val = f"{node.h:.0f}" if node.h != float("inf") else "inf"
            next_nodes_log.append(
                f"  Node {node.index} at {node.position}: f={f_val:.0f}, g={g_val}, h={h_val}"
            )

        steps.append(
            (
                current_node,
                [nodes[i] for _, i in open_heap],
                set(closed_set),
                None,
                ["Neighbors added to open set (cyan)"] + next_nodes_log,
                snapshot_nodes(),
            )
        )

    return steps


if __name__ == "__main__":
    # Select start and goal from nodes
    start = nodes[0].position  # First node
    goal = nodes[-1].position  # Last node

    steps = a_star(start, goal)
    if not steps:
        print("No path found.")
        sys.exit()

    step_idx = 0
    total_steps = len(steps)
    visualizer = Visualizer(nodes, start, goal)

    # Restore node values for the first step before drawing
    current_node, open_set, closed_set, path, log_lines, node_snapshot = steps[step_idx]
    restore_nodes(node_snapshot)
    visualizer.update_display(current_node, open_set, closed_set, path, delay=0)
    print("\n".join(log_lines))

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
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
                    print("\n".join(log_lines))
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
                    print("\n".join(log_lines))
        # No need for pygame.time.delay here, as we wait for events
