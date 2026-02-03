from main import Maze, Cell, Colors
from collections import deque
from parse import error


def solver(maze: Maze) -> None:
    start = maze.entry
    end = maze.exit

    queue = deque([start])
    visited = {start}
    parents = {start: None}
    found = False

    while queue:
        curr_x, curr_y = queue.popleft()

        if (curr_x, curr_y) == end:
            found = True
            break

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            cell: Cell = maze.grid[ny][nx]

            if (nx, ny) not in visited and cell.value in [0, 2, 3]:
                visited.add((nx, ny))
                parents[(nx, ny)] = (curr_x, curr_y)

                queue.append((nx, ny))

    if found:
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parents[current]
        path = path[::-1]

        for y, x in path:
            if not maze.grid[x][y].value in [2, 3]:
                maze.grid[x][y].color = Colors.BRIGHT_YELLOW
                maze.grid[x][y].value = 4
        return path
    error("Path not found")
