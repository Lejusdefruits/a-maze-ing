from output import Cell_output
from main import Maze
from parse import Entry, error
from main import Colors


def decode_hex_cell(hex_char):
    cell = Cell_output()
    value = int(hex_char, 16)

    cell.north = 1 if value & 1 else 0
    cell.east = 1 if value & 2 else 0
    cell.south = 1 if value & 4 else 0
    cell.west = 1 if value & 8 else 0

    return cell


def format_input(buffer: str):
    lines = [line for line in buffer.split("\n") if line]

    grid_lines = lines[:-3]
    entry = lines[-3]
    exit = lines[-2]
    solution = lines[-1]

    return grid_lines, entry, exit, solution


def make_entry(grid_lines, entry, exit, file_name, seed) -> dict:
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


def make_maze(maze: Maze, grid) -> None:
    for m_line, g_line in zip(maze.grid, grid):
        for i, (m_cell, g_cell) in enumerate(zip(m_line[:-1], g_line[:-1])):
            if i > 0 and g_cell.east == 0:
                m_line[i + 1].value = 0
                m_line[i + 1].color = Colors.WHITE
            if g_cell.west == 0:
                m_line[i - 1].value = 0
                m_line[i - 1].color = Colors.WHITE


def make_solution(maze: Maze, solution):
    x, y = maze.entry
    maze.solution = solution
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
        maze.grid[y][x].value = 4
        maze.grid[y][x].color = Colors.BRIGHT_YELLOW


def inp(seed: str) -> Maze:
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
    entry_dict = Entry(make_entry(grid_lines, entry, exit, "output.txt", seed).items())
    new_maze = Maze(entry_dict)
    make_maze(new_maze, new_grid)
    make_solution(new_maze, solution)
    new_maze.grid[new_maze.entry[1]][new_maze.entry[0]].color = Colors.BRIGHT_YELLOW
    new_maze.grid[new_maze.exit[1]][new_maze.exit[0]].color = Colors.RED
    return new_maze


if __name__ == "__main__":
    from seed import get_seed

    maze = input(get_seed("output.txt"))
    from render_ascii import render

    maze.place_42()
    render(maze)
