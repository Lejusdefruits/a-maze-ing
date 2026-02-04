from output import Cell_output
from models import Maze, Colors
from parse import Entry, error


def decode_hex_cell(hex_char: str) -> Cell_output:
    """Decode a hexadecimal character into a Cell_output object."""
    cell = Cell_output()
    value = int(hex_char, 16)

    cell.north = 1 if value & 1 else 0
    cell.east = 1 if value & 2 else 0
    cell.south = 1 if value & 4 else 0
    cell.west = 1 if value & 8 else 0

    return cell


def format_input(buffer: str) -> tuple[list[str], str, str, str]:
    """Extract grid, entry, exit, and solution from the input buffer."""
    lines = [line for line in buffer.split("\n") if line]

    grid_lines = lines[:-3]
    entry = lines[-3]
    exit = lines[-2]
    solution = lines[-1]

    return grid_lines, entry, exit, solution


def make_entry(
    grid_lines: list[str], entry: str, exit: str, file_name: str, seed: str
) -> dict:
    """Create a dictionary for Maze initialization from parsed data."""
    entry_dict = {
        "WIDTH": len(grid_lines[0]),
        "HEIGHT": len(grid_lines),
        "ENTRY": entry,
        "EXIT": exit,
        "OUTPUT_FILE": file_name,
        "PERFECT": "True",
        "RENDER": "ascii",
        "SEED": seed
    }
    return entry_dict


def make_maze(maze: Maze, grid: list[list[Cell_output]]) -> None:
    """Reconstruct the maze grid based on the imported cell data."""
    for m_line, g_line in zip(maze.grid, grid):
        for i, (m_cell, g_cell) in enumerate(zip(m_line[:-1], g_line[:-1])):
            if i > 0 and g_cell.west != 0:
                m_line[i - 1].value = 0
                m_line[i - 1].color = Colors.BLACK
            if g_cell.east != 0:
                m_line[i + 1].value = 0
                m_line[i + 1].color = Colors.BLACK


def make_solution(maze: Maze, solution: str) -> None:
    """Reconstruct the solution path on the maze grid."""
    x, y = maze.entry
    path = [(x, y)]
    for dir in solution:
        if dir == "N":
            x, y = x, y - 1
        elif dir == "E":
            x, y = x - 1, y
        elif dir == "W":
            x, y = x + 1, y
        elif dir == "S":
            x, y = x, y + 1
        else:
            error(f"{dir} not valid for a direction")
        path.append((x, y))
        maze.grid[y][x].value = 4
        maze.grid[y][x].color = Colors.BRIGHT_YELLOW
    maze.solution = path


def inp(seed: str) -> Maze:
    """Import and reconstruct a maze from a seed string."""
    from seed import get_lab
    print(f"je pars de la seed: {seed}")

    buffer = get_lab(seed)

    grid_lines, entry, exit, solution = format_input(buffer)

    new_grid = []
    for line in grid_lines:
        tmp_line = []
        for i, char in enumerate(line):
            tmp_line.append(decode_hex_cell(char))
        new_grid.append(tmp_line)
    entry_dict = Entry(list(make_entry(grid_lines, entry,
                       exit, "output.txt", seed).items()))
    new_maze = Maze(entry_dict)
    make_maze(new_maze, new_grid)
    make_solution(new_maze, solution)
    new_maze.grid[new_maze.entry[1]][new_maze.entry[0]
                                     ].color = Colors.BRIGHT_YELLOW
    new_maze.grid[new_maze.entry[1]][new_maze.entry[0]].value = 2
    new_maze.grid[new_maze.exit[1]][new_maze.exit[0]].color = Colors.RED
    new_maze.grid[new_maze.exit[1]][new_maze.exit[0]].value = 3
    return new_maze


if __name__ == "__main__":
    from seed import get_seed

    maze = inp(get_seed("output.txt"))
