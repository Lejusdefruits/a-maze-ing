from main import Maze


class Cell_output:
    def __init__(self):
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0


def get_hex_cell(cell_obj):
    value = 0
    if cell_obj.north:
        value += 1
    if cell_obj.east:
        value += 2
    if cell_obj.south:
        value += 4
    if cell_obj.west:
        value += 8
    return format(value, "X")


def get_neighbors_map(grid, x, y, width, height):
    res = {"north": 1, "south": 1, "west": 1, "east": 1}

    if y > 0 and grid[y - 1][x].value in [1, 42]:
        res["north"] = 0
    if y < height - 1 and grid[y + 1][x].value in [1, 42]:
        res["south"] = 0
    if x > 0 and grid[y][x - 1].value in [1, 42]:
        res["west"] = 0
    if x < width - 1 and grid[y][x + 1].value in [1, 42]:
        res["east"] = 0

    return res


def parse_grid(maze) -> list:
    new_grid = [[Cell_output() for _ in range(maze.width)] for _ in range(maze.height)]

    for y in range(maze.height):
        for x in range(maze.width):
            neighbors = get_neighbors_map(maze.grid, x, y, maze.width, maze.height)
            target = new_grid[y][x]
            target.north = neighbors["north"]
            target.south = neighbors["south"]
            target.east = neighbors["east"]
            target.west = neighbors["west"]
    return new_grid


def get_solver(maze: Maze):
    result = ""
    for i, current in enumerate(maze.solution[:-1]):
        x, y = current
        neighbors = {
            "N": (x, y - 1),
            "S": (x, y + 1),
            "E": (x - 1, y),
            "W": (x + 1, y),
        }
        for key, val in neighbors.items():
            if val != maze.exit:
                if maze.solution[i + 1] == val:
                    result += key
    return result


def outpoute(maze: Maze):
    grid = parse_grid(maze)

    with open(maze.output_file, "w") as f:
        for row in grid:
            line = "".join(get_hex_cell(cell_obj) for cell_obj in row)
            f.write(line + "\n")
        f.write("\n")
        f.write(f"{maze.entry[0]} {maze.entry[1]}\n")
        f.write(f"{maze.exit[0]} {maze.exit[1]}\n")
        f.write(f"{get_solver(maze)}\n")
