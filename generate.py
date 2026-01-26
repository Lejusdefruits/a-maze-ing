from random import shuffle


def get_neighbors(maze, visited, x, y):
    potential_targets = [(x, y - 2), (x, y + 2), (x - 2, y), (x + 2, y)]
    neighbors = []

    for nx, ny in potential_targets:
        if maze.is_valid_cell(nx, ny):
            if not visited[ny][nx]:
                mx, my = (x + nx) // 2, (y + ny) // 2
                if maze.grid[my][mx].value != 42:
                    neighbors.append((nx, ny))

    shuffle(neighbors)
    return neighbors


def backtrack(maze, visited, x, y):
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


def generate(maze):
    visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]

    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x].value == 42:
                visited[y][x] = True

    start_x, start_y = maze.entry
    backtrack(maze, visited, start_x, start_y)
