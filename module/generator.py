from random import random, shuffle
from .models import Maze


def get_neighbors(
    maze: Maze, visited: list[list[bool]], x: int, y: int
) -> list[tuple[int, int]]:
    """Identify unvisited neighbor cells available for path generation."""
    potential_targets = [
        (x, y - 2), (x, y + 2), (x - 2, y), (x + 2, y)
    ]
    neighbors = []

    for nx, ny in potential_targets:
        if maze.is_valid_cell(nx, ny):
            if not visited[ny][nx]:
                mx, my = (x + nx) // 2, (y + ny) // 2
                if maze.grid[my][mx].value != 42:
                    neighbors.append((nx, ny))

    shuffle(neighbors)
    return neighbors


def backtrack(maze: Maze, visited: list[list[bool]], x: int, y: int) -> None:
    """Recursively carve paths using the backtracking algorithm."""
    visited[y][x] = True

    if maze.grid[y][x].value != 42:
        maze.grid[y][x].dig()

    neighbors = get_neighbors(maze, visited, x, y)

    for nx, ny in neighbors:
        if not visited[ny][nx]:
            mx, my = (x + nx) // 2, (y + ny) // 2

            if maze.grid[my][mx].value != 42:
                maze.grid[my][mx].dig()

            backtrack(maze, visited, nx, ny)


def generate(maze: Maze) -> None:
    """Generate a perfect maze using Recursive Backtracker."""
    visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]

    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x].value == 42:
                visited[y][x] = True

    try:
        start_x, start_y = maze.entry
        backtrack(maze, visited, start_x, start_y)
    except RecursionError:
        print("Recursion limit reached. Maze might be incomplete.")

    if not maze.perfect:
        _make_imperfect(maze)


def _make_imperfect(maze: Maze) -> None:
    """Remove random walls to create loops in the maze."""
    for y in range(1, maze.height - 1):
        for x in range(1, maze.width - 1):
            if maze.grid[y][x].value == 1:
                if random() < 0.05:  # 5% chance to remove a wall
                    count_neighbors = 0
                    params = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for dx, dy in params:
                        if maze.grid[y + dy][x + dx].value != 1:
                            count_neighbors += 1
                    if count_neighbors >= 2:
                        maze.grid[y][x].dig()
