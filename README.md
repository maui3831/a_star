# A* Pathfinding Visualization

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

For Introduction to Artificial Intelligence
by AI Group 2

- [A\* Pathfinding Visualization](#a-pathfinding-visualization)
  - [1. Introduction](#1-introduction)
  - [2. How Code Works](#2-how-code-works)
  - [3. Requirements](#3-requirements)
  - [4. How to Run](#4-how-to-run)
  - [5. Features](#5-features)

## 1. Introduction
This project implements an interactive visualization of the A* pathfinding algorithm using Pygame. It features a maze-like environment where a rat navigates from a start position to a goal position, with real-time visualization of the algorithm's decision-making process.

## 2. How Code Works
- The program initializes a graphical interface using Pygame.
- Nodes and connections are defined in the `maze.py` file.
- The A* algorithm is implemented to find the shortest path between a start and end node.
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
3. Run the `gui.py` file:
   ```bash
   python gui.py
   ```

## 5. Features
- Interactive visualization of A* pathfinding algorithm
- Real-time display of f, g, and h values for each node
- Step-by-step navigation through the algorithm's execution
- Animated rat movement along the final path
- Visual distinction between different node states (open set, closed set, current node, path)
- Beautiful maze background with custom rat sprites

## Project Structure

- `a_star.py`: Main implementation of the A* algorithm and program entry point
- `node.py`: Node class definition and graph structure
- `gui.py`: Pygame-based visualization system
- `assets/`: Directory containing images and sprites
  - `maze_bg.png`: Background maze image
  - `mouse.png`: Application icon
  - `rat/`: Directory containing rat sprites for different directions

### Controls

- **Right Arrow**: Move forward through the algorithm steps
- **Left Arrow**: Move backward through the algorithm steps
- **Close Window**: Exit the program

### Visualization Elements

- **Green Node**: Start position
- **Yellow Node**: Goal position
- **Cyan Nodes**: Nodes in the open set
- **Dark Gray Nodes**: Nodes in the closed set
- **Pink Node**: Current node being evaluated
- **Orange Path**: Final path from start to goal
- **White Nodes**: Unvisited nodes

### Algorithm Information

The visualization shows:
- f(x) = g(x) + h(x) formula at the top of the screen
- Current node's f, g, and h values
- f-value for each node in the graph
- h-value (heuristic) for each node
- Possible next nodes after each expansion

## Implementation Details

### A* Algorithm

The implementation uses:
- Manhattan distance as the heuristic function
- Priority queue for efficient node selection
- Step-by-step visualization of the algorithm's progress
- Path reconstruction using parent pointers

### Visualization System

The visualization includes:
- Real-time rendering of the graph
- Smooth animation of the rat's movement
- Direction-aware rat sprites
- Clear visual distinction between different node states
- Detailed algorithm information display

## Contributing

Feel free to submit issues and enhancement requests!