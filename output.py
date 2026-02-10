from models import Maze
from parse import error


class Cell_output:
    """Helper class to store cell wall configuration for output."""

    def __init__(self):
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0

    def __str__(self) -> str:
        return (
            f"Cell(N:{self.north}, S:{self.south}, "
            f"E:{self.east}, W:{self.west})"
        )

    def __repr__(self) -> str:
        return self.__str__()


def get_hex_cell(cell_obj: Cell_output) -> str:
    """Convert a cell's wall configuration to a hexadecimal string."""
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


def get_neighbors_map(
    grid: list[list], x: int, y: int, width: int, height: int
) -> dict[str, int]:
    """Determine wall status based on neighbor cell values."""
    res = {"north": 1, "south": 1, "west": 1, "east": 1}
    self_is_wall = grid[y][x].value in [1, 42]

    if y > 0:
        neigh_is_wall = grid[y - 1][x].value in [1, 42]
        res["north"] = 1 if self_is_wall != neigh_is_wall else 0

    if y < height - 1:
        neigh_is_wall = grid[y + 1][x].value in [1, 42]
        res["south"] = 1 if self_is_wall != neigh_is_wall else 0

    if x > 0:
        neigh_is_wall = grid[y][x - 1].value in [1, 42]
        res["west"] = 1 if self_is_wall != neigh_is_wall else 0

    if x < width - 1:
        neigh_is_wall = grid[y][x + 1].value in [1, 42]
        res["east"] = 1 if self_is_wall != neigh_is_wall else 0

    return res


def parse_grid(maze: Maze) -> list[list[Cell_output]]:
    """Convert the maze grid into a grid of Cell_output objects."""
    new_grid = [[Cell_output() for _ in range(maze.width)]
                for _ in range(maze.height)]

    for y in range(maze.height):
        for x in range(maze.width):
            neighbors = get_neighbors_map(
                maze.grid, x, y, maze.width, maze.height)
            target = new_grid[y][x]
            target.north = neighbors["north"]
            target.south = neighbors["south"]
            target.east = neighbors["east"]
            target.west = neighbors["west"]
    return new_grid


def get_solver(maze: Maze) -> str:
    """Convert the solution path into a string of directions (NSEW)."""
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


def outpoute(maze: Maze) -> None:
    """Write the maze structure and solution to the output file."""
    grid = parse_grid(maze)

    try:
        with open(maze.output_file, "w") as f:
            for row in grid:
                line = "".join(get_hex_cell(cell_obj) for cell_obj in row)
                f.write(line + "\n")
            f.write("\n")
            f.write(f"{maze.entry[0]}, {maze.entry[1]}\n")
            f.write(f"{maze.exit[0]}, {maze.exit[1]}\n")
            f.write(f"{get_solver(maze)}\n")
    except OSError as e:
        error(f"Failed to write output file: {e}")
