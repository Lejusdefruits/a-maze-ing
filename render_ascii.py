from main import Maze, Cell
from os import system, name
from parse import error


def get_caracter(cell: Cell):
    if cell.value in [0, 1, 4, 42]:  # wall
        return "█"
    elif cell.value == 3 or cell.value == 2:  # exit
        return "◼"
    else:
        error(f"Invalid value of cell {cell.x}, {cell.y}: {cell.value}")


def render(maze: Maze):
    system("cls" if name == "nt" else "clear")
    reset = "\033[0m"
    for i in range(maze.height):
        current_line = ""
        for j in range(maze.width):
            current_cell: Cell = maze.grid[i][j]
            current_line += f"{current_cell.color}{get_caracter(current_cell)}{reset}"
        print(f"{current_line}")
