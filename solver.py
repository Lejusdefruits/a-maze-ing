from main import Maze, Cell, Colors
from collections import deque


def solver(maze):
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
            print("Exit found !")
            return parents

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            nx, ny = curr_x + dx, curr_y + dy

            if 0 < nx < maze.width and 0 <= ny < maze.height:
                cell = maze.grid[ny][nx]

            if (nx, ny) not in visited and cell.value in [0, 2, 3]:
                visited.add((nx, ny))
                parents[(nx, ny)] = (curr_x, curr_y)
                queue.append((nx, ny))

    if found:
        path = []
        current = end
        while current is not None:
            path.append(current)
            px, py = current
            if maze.grid[py][px].value == 0: 
                maze.grid[py][px].color = Colors.RED 
            current = parents[current]
        return path[::-1]

    return None