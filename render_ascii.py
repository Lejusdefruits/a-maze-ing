from main import Maze, Cell, Colors


def get_caracter(cell: Cell):
    if cell.value in [
        0,
        1,
        4,
        42
    ]:  # wall
        return "█"
    elif cell.value == 3 or cell.value == 2:  # exit
        return "◼"
    else:
        raise ValueError(f"Invalid value of cell {cell.x}, {cell.y}: {cell.value}")


def render(maze: Maze):
    buffer = ""
    for i in range(maze.height):
        current_line = ""
        for j in range(maze.width):
            current_cell: Cell = maze.grid[i][j]
            current_line += (
                f"{current_cell.color}{get_caracter(current_cell)}{Colors.RESET}"
            )
        buffer += f"{current_line}\n"
    print(buffer)
