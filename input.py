from output import Cell_output
from models import Maze, Colors
from parse import Entry, error, MazeError


def decode_hex_cell(hex_char: str) -> Cell_output:
    """Decode a hexadecimal character into a Cell_output object."""
    cell = Cell_output()
    try:
        value = int(hex_char, 16)
    except ValueError:
        error(f"Invalid hex character: {hex_char}")

    cell.north = 1 if value & 1 else 0
    cell.east = 1 if value & 2 else 0
    cell.south = 1 if value & 4 else 0
    cell.west = 1 if value & 8 else 0

    return cell


def format_input(buffer: str) -> tuple[list[str], str, str, str]:
    """Extract grid, entry, exit, and solution from the input buffer."""
    lines = [line for line in buffer.split("\n") if line]

    if len(lines) < 3:
        error("Input file format invalid: missing entry, exit or solution")

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
    width = maze.width
    height = maze.height

    # Visited matrix to track processed cells
    visited = [[False for _ in range(width)] for _ in range(height)]

    # Start from Entry which we know is a Path (value 2)
    stack = [maze.entry]
    visited[maze.entry[1]][maze.entry[0]] = True

    while stack:
        x, y = stack.pop()
        current_cell = maze.grid[y][x]
        hex_data = grid[y][x]

        # Determine if current cell is Wall
        cur_is_wall = current_cell.value in [1, 42]

        # Define neighbors: name, x, y, separator_value
        neighbors = [
            ("north", x, y - 1, hex_data.north),
            ("south", x, y + 1, hex_data.south),
            ("east", x + 1, y, hex_data.east),
            ("west", x - 1, y, hex_data.west)
        ]

        for _, nx, ny, sep in neighbors:
            if 0 <= nx < width and 0 <= ny < height:
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    target_cell = maze.grid[ny][nx]

                    # Separator 1 means types are different, 0 means same
                    neigh_is_wall = cur_is_wall != (sep == 1)

                    if neigh_is_wall:
                        if target_cell.value not in [2, 3, 42]:
                            target_cell.value = 1
                            target_cell.color = Colors.WHITE
                    else:
                        if target_cell.value not in [2, 3, 42]:
                            target_cell.value = 0
                            target_cell.color = Colors.BLACK

                    stack.append((nx, ny))


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
    try:
        buffer = get_lab(seed)
    except ValueError as e:
        error(str(e))
    except Exception as e:
        error(f"Error processing seed: {e}")

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
    import sys
    from seed import get_seed

    if len(sys.argv) != 2:
        print("Usage: python3 input.py <filename>")
        sys.exit(1)

    try:
        file_name = sys.argv[1]
        seed = get_seed(file_name)
        print(f"{seed}")
        maze = inp(str(seed))
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied accessing '{file_name}'.")
        sys.exit(1)
    except MazeError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
