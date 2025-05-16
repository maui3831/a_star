from collections import deque
from gui import Visualizer
from node import Node, nodes
import pygame
import sys
from rich import print

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

def breadth_first_search(start_pos, goal_pos):
    # Initialize data structures
    queue = deque()  
    visited = set() 
    in_queue_set = set() 
    g_score = {}  

    # Get start and goal nodes
    start_node = get_node_by_position(start_pos)
    goal_node = get_node_by_position(goal_pos)

    def snapshot_nodes():
        return [
            (node.g, node.h, node.f, node.parent.index if node.parent else None)
            for node in nodes
        ]

    # Initialize all nodes for a clean state
    for node in nodes:
        node.g = float("inf")
        node.h = 0
        node.f = float("inf")
        node.parent = None

    # Initialize start node's properties
    start_node.g = 0
    start_node.f = 0
    g_score[start_node.index] = 0

    # Add start node to queue and in_queue_set
    queue.append(start_node)
    in_queue_set.add(start_node.position)

    # Record initial state: start_node is in queue, nothing visited (explored)
    steps = [(
        None,  
        list(queue), 
        set(visited),  
        None, 
        ["Initial state: Start node added to queue. Nothing explored yet."],
        snapshot_nodes(),
    )]

    # Main BFS loop
    while queue:
        current_node = queue.popleft()
        in_queue_set.remove(current_node.position)
        
        # Node becomes "explored" or "visited" when it's popped and processed
        visited.add(current_node.position)

        # Check if goal is reached AFTER marking current_node as visited
        if current_node.position == goal_pos:
            path = current_node.get_path()
            # Record this step where goal is identified as current_node
            steps.append((
                current_node,
                list(queue),
                set(visited),
                None, # Path will be shown in subsequent steps
                [f"Goal node {current_node.index} reached! Path reconstruction starts."],
                snapshot_nodes(),
            ))
            # Record path visualization steps
            for i in range(len(path)):
                steps.append((
                    current_node, 
                    list(queue),
                    set(visited),
                    path[: i + 1],
                    [f"Path step {i + 1}/{len(path)}: {path[: i + 1]}"],
                    snapshot_nodes(),
                ))
            path_with_indices = [
                f"Node {next(n.index for n in nodes if n.position == step)}: {step} "
                for step in path
            ]
            steps.append((
                current_node,
                list(queue),
                set(visited),
                path,
                [
                    "\nPath found!",
                    f"Path length: {len(path)}",
                    f"Total cost (g): {current_node.g}",
                    "Path (from start to goal):",
                    *path_with_indices,
                ],
                snapshot_nodes(),
            ))
            return steps

        # Evaluate neighbors
        for neighbor_idx in current_node.neighbors:
            neighbor_node = nodes[neighbor_idx]
            
            # Add to queue only if not visited (popped) AND not already in queue
            if neighbor_node.position not in visited and neighbor_node.position not in in_queue_set:
                tentative_g = current_node.g + Node.manhattan_distance(
                    current_node, neighbor_node
                )
                if tentative_g < getattr(neighbor_node, "g", float("inf")):
                    neighbor_node.g = tentative_g
                    neighbor_node.f = tentative_g
                    neighbor_node.parent = current_node
                    g_score[neighbor_idx] = tentative_g
                
                queue.append(neighbor_node)
                in_queue_set.add(neighbor_node.position)

        # Record current step for visualization
        log_message = [f"Processing node {current_node.index} at {current_node.position}. It is now explored."]
        if list(queue):
            log_message.append("  Nodes currently in queue (g=cost):")
            for node_in_queue in queue:
                g_val = f"{node_in_queue.g:.0f}" if node_in_queue.g != float("inf") else "inf"
                log_message.append(
                    f"    Node {node_in_queue.index} at {node_in_queue.position}: g={g_val}"
                )
        else:
            log_message.append("  Queue is now empty.")
            if current_node.position != goal_pos:
                 log_message.append("  Goal not reached and queue is empty. No path exists.")


        steps.append((
            current_node,
            list(queue), 
            set(visited), 
            None,
            log_message,
            snapshot_nodes(),
        ))

    # If loop finishes and goal not found (should be handled by empty queue log)
    if not any("Path found!" in step[4][0] for step in steps if len(step[4]) > 0 and isinstance(step[4][0], str)):
        steps.append((
            None, 
            [], 
            set(visited), 
            None, 
            ["BFS complete. Goal not reached. No path found."], 
            snapshot_nodes()
        ))
    return steps

if __name__ == "__main__":
    # Set start and goal positions
    start = nodes[0].position
    goal = nodes[-1].position

    # Run BFS algorithm
    steps = breadth_first_search(start, goal)
    if not steps:
        print("No path found.")
        sys.exit()

    # Initialize visualization
    step_idx = 0
    total_steps = len(steps)
    visualizer = Visualizer(nodes, start, goal, algorithm_name="Breadth-First Search")

    # Display initial state
    current_node, open_set, closed_set, path, log_lines, node_snapshot = steps[step_idx]
    restore_nodes(node_snapshot)
    visualizer.update_display(current_node, open_set, closed_set, path, delay=0)
    
    # Print log for the current step
    if current_node is None:
        print(f"\nStep {step_idx + 1}/{total_steps}: Initial state.")
    elif not (log_lines and (log_lines[0].startswith("Path step") or "Path found!" in log_lines[0])):
        print(f"\nStep {step_idx + 1}/{total_steps}: Current node {current_node.index} at {current_node.position} (g={current_node.g:.0f})")
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
                        current_node, open_set, closed_set, path, log_lines, node_snapshot = steps[step_idx]
                        restore_nodes(node_snapshot)
                        visualizer.update_display(current_node, open_set, closed_set, path, delay=0)
                        
                        if current_node is None: # Should not happen if step_idx > 0
                            print(f"\nStep {step_idx + 1}/{total_steps}: Initial state.")
                        elif not (log_lines and (log_lines[0].startswith("Path step") or "Path found!" in log_lines[0])):
                            print(f"\nStep {step_idx + 1}/{total_steps}: Current node {current_node.index} at {current_node.position} (g={current_node.g:.0f})")
                        print("\n".join(log_lines))
                        
                        if step_idx == total_steps - 1 and path:
                            visualizer.start_animation(path)
                elif event.key == pygame.K_LEFT:
                    if step_idx > 0:
                        step_idx -= 1
                        current_node, open_set, closed_set, path, log_lines, node_snapshot = steps[step_idx]
                        restore_nodes(node_snapshot)
                        visualizer.update_display(current_node, open_set, closed_set, path, delay=0)

                        if current_node is None:
                             print(f"\nStep {step_idx + 1}/{total_steps}: Initial state.")
                        elif not (log_lines and (log_lines[0].startswith("Path step") or "Path found!" in log_lines[0])):
                            print(f"\nStep {step_idx + 1}/{total_steps}: Current node {current_node.index} at {current_node.position} (g={current_node.g:.0f})")
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
                    visualizer.current_direction = visualizer.determine_direction(dx, dy)
                    visualizer.progress = 0.0
            visualizer.draw_nodes(
                visualizer.current_node,
                visualizer.open_set,
                visualizer.closed_set,
                visualizer.path,
            )

        pygame.display.flip()
