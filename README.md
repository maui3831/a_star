# Pathfinding Algorithms Visualization

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

For Introduction to Artificial Intelligence
by AI Group 2

- [Pathfinding Algorithms Visualization](#pathfinding-algorithms-visualization)
  - [1. Introduction](#1-introduction)
  - [2. How Code Works](#2-how-code-works)
  - [3. Requirements](#3-requirements)
  - [4. How to Run](#4-how-to-run)
  - [5. Features](#5-features)
  - [6. Project Structure](#6-project-structure)
  - [7. Controls](#7-controls)
  - [8. Visualization Elements](#8-visualization-elements)
  - [9. Algorithm Information](#9-algorithm-information)
  - [10. Implementation Details](#10-implementation-details)
  - [11. Contributing](#11-contributing)

## 1. Introduction
This project implements interactive visualizations of two pathfinding algorithms (A* and Breadth-First Search) using Pygame. It features a maze-like environment where a rat navigates from a start position to a goal position, with real-time visualization of each algorithm's decision-making process.

## 2. How Code Works
- The program initializes a graphical interface using Pygame.
- Nodes and connections are defined in the `node.py` file.
- Two pathfinding algorithms are implemented:
  - A* algorithm for finding the shortest path using heuristic functions
  - Breadth-First Search for finding the shortest path by exploring all nodes at the current depth before moving deeper
- The visualization includes animations of the rat moving along the path.

## 3. Requirements
- Python 3.13 or higher
- Pygame library
- Rich (for console output formatting)

## 4. How to Run
1. Clone the repository.
2. Install the required dependencies using the following command:
   ```bash
   pip install pygame rich
   ```
3. Run either algorithm:
   ```bash
   # For A* algorithm
   python a_star.py
   
   # For Breadth-First Search
   python bfs.py
   ```

## 5. Features
- Interactive visualization of two pathfinding algorithms:
  - A* Search: Uses heuristic functions to find the optimal path
  - Breadth-First Search: Explores all nodes at the current depth before moving deeper
- Real-time display of node values:
  - A*: f, g, and h values for each node
  - BFS: g values (distance from start) for each node
- Step-by-step navigation through the algorithm's execution
- Animated rat movement along the final path
- Visual distinction between different node states (open set, closed set, current node, path)
- Beautiful maze background with custom rat sprites
- Dynamic window title showing the current algorithm being visualized

## 6. Project Structure

- `a_star.py`: Implementation of the A* algorithm
- `bfs.py`: Implementation of the Breadth-First Search algorithm
- `node.py`: Node class definition and graph structure
- `gui.py`: Pygame-based visualization system
- `assets/`: Directory containing images and sprites
  - `maze_bg.png`: Background maze image
  - `mouse.png`: Application icon
  - `rat/`: Directory containing rat sprites for different directions

## 7. Controls

- **Right Arrow**: Move forward through the algorithm steps
- **Left Arrow**: Move backward through the algorithm steps
- **Close Window**: Exit the program

## 8. Visualization Elements

- **Green Node**: Start position
- **Yellow Node**: Goal position
- **Cyan Nodes**: Nodes in the open set (queue for BFS)
- **Dark Gray Nodes**: Nodes in the closed set (visited nodes)
- **Pink Node**: Current node being evaluated
- **Orange Path**: Final path from start to goal
- **White Nodes**: Unvisited nodes

## 9. Algorithm Information

### A* Algorithm
The visualization shows:
- f(x) = g(x) + h(x) formula at the top of the screen
- Current node's f, g, and h values
- f-value for each node in the graph
- h-value (heuristic) for each node
- Possible next nodes after each expansion

### Breadth-First Search
The visualization shows:
- Current node's g value (distance from start)
- g-value for each node in the graph
- Nodes currently in the queue
- Step-by-step exploration of nodes at each depth level

## 10. Implementation Details

### A* Algorithm
The implementation uses:
- Manhattan distance as the heuristic function
- Priority queue for efficient node selection
- Step-by-step visualization of the algorithm's progress
- Path reconstruction using parent pointers

### Breadth-First Search
The implementation uses:
- Queue for level-order traversal
- Separate tracking of nodes in queue and visited nodes
- Step-by-step visualization of the exploration process
- Path reconstruction using parent pointers

### Visualization System
The visualization includes:
- Real-time rendering of the graph
- Smooth animation of the rat's movement
- Direction-aware rat sprites
- Clear visual distinction between different node states
- Detailed algorithm information display
- Dynamic window title showing the current algorithm

## 11. Contributing

Feel free to submit issues and enhancement requests!