from .models import Maze, Cell
from os import system, name


def get_caracter(cell: Cell) -> str:
    """Return the ASCII character representation for a cell."""
    if cell.value in [0, 1, 4, 42]:  # wall
        return "█"
    elif cell.value == 3 or cell.value == 2:  # exit
        return "◼"
    else:
        raise ValueError(
            f"Invalid value of cell {cell.x}, {cell.y}: {cell.value}"
        )


def render(maze: Maze) -> None:
    """Print the maze to the console with colors."""
    system("cls" if name == "nt" else "clear")
    reset = "\033[0m"
    for i in range(maze.height):
        current_line = ""
        for j in range(maze.width):
            current_cell: Cell = maze.grid[i][j]
            current_line += (
                f"{current_cell.color}{get_caracter(current_cell)}{reset}"
            )
        print(f"{current_line}")
