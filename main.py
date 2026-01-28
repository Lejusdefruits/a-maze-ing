import sys
from sys import argv, stdout

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.setrecursionlimit(100000)

from parse import Entry, parse


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class Cell:
    def __init__(self, x, y):
        self.color = Colors.GREEN
        self.value = 1
        self.x = x
        self.y = y

    def dig(self):
        if self.value != 2 and self.value != 3:
            self.value = 0


class Maze:
    def __init__(self, args: Entry):
        self.perfect = args.perfect
        self.entry = args.entry
        self.exit = args.exit
        self.width = args.width
        self.height = args.height
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.grid[self.entry[1]][self.entry[0]].color = Colors.YELLOW
        self.grid[self.entry[1]][self.entry[0]].value = 2
        self.grid[self.exit[1]][self.exit[0]].value = 3

    def is_valid_cell(self, x, y):
        return (
            not self.is_border(x, y)
            and not (x < 0 or y < 0 or x >= self.width or y >= self.height)
            and self.grid[y][x].value != 42
        )

    def is_border(self, x, y):
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    def up(self, x, y):
        return self.grid[y - 1][x] if self.is_valid_cell(x, y - 1) else None

    def down(self, x, y):
        return self.grid[y + 1][x] if self.is_valid_cell(x, y + 1) else None

    def left(self, x, y):
        return self.grid[y][x - 1] if self.is_valid_cell(x - 1, y) else None

    def right(self, x, y):
        return self.grid[y][x + 1] if self.is_valid_cell(x + 1, y) else None

    def place_42(self):
        x_bloc, y_bloc = 7, 5
        if self.width < x_bloc or self.height < y_bloc:
            return -1

        x_start = (self.width - x_bloc) // 2
        y_start = (self.height - y_bloc) // 2

        nb_4 = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
        nb_2 = [
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (4, 2),
            (5, 2),
            (6, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        ]

        for dx, dy in nb_4 + nb_2:
            if self.is_valid_cell(x_start + dx, y_start + dy):
                self.grid[y_start + dy][x_start + dx].value = 42
                self.grid[y_start + dy][x_start + dx].color = Colors.BLUE

        holes_4 = [(1, 0), (1, 1)]
        holes_2 = [(4, 1), (5, 1), (5, 3), (6, 3)]
        for dx, dy in holes_4 + holes_2:
            if self.is_valid_cell(x_start + dx, y_start + dy):
                self.grid[y_start + dy][x_start + dx].value = 0
        return 0


if __name__ == "__main__":
    args = parse(argv)
    args.print_o()
    m = Maze(args)
    m.place_42()
    from generate import generate
    from render_ascii import render

    generate(m)
    render(m)
