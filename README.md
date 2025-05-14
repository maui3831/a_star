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
This project visualizes the A* pathfinding algorithm using Pygame. It demonstrates how the algorithm finds the shortest path between nodes in a maze-like environment.

## 2. How Code Works
- The program initializes a graphical interface using Pygame.
- Nodes and connections are defined in the `maze.py` file.
- The A* algorithm is implemented to find the shortest path between a start and end node.
- The visualization includes animations of the rat moving along the path.

## 3. Requirements
- Python 3.13 or higher
- Pygame library

## 4. How to Run
1. Clone the repository.
2. Install the required dependencies using the following command:
   ```bash
   pip install pygame
   ```
3. Run the `gui.py` file:
   ```bash
   python gui.py
   ```

## 5. Features
- Interactive visualization of the A* algorithm.
- Animated rat movement along the path.
- Customizable maze background and rat images.