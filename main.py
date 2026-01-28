import sys
from sys import argv, stdout
from parse import Entry, parse
from random import shuffle

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.setrecursionlimit(100000)


class Colors:
    # Styles
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    REVERSE = "\033[7m"

    # Couleurs de base (Standard)
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Couleurs étendues (Bright / Claires)
    GRAY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Couleurs spécifiques (utilisant les codes 256 couleurs)
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;205m"
    PURPLE = "\033[38;5;129m"
    BROWN = "\033[38;5;94m"

    # Couleurs de fond (Background) - Utile pour les murs du labyrinthe
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class Cell:
    def __init__(self, x, y):
        self.color = Colors.WHITE
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
        self.grid[self.entry[1]][self.entry[0]].color = Colors.BRIGHT_YELLOW
        self.grid[self.entry[1]][self.entry[0]].value = 2
        self.grid[self.exit[1]][self.exit[0]].value = 3
        self.grid[self.exit[1]][self.exit[0]].color = Colors.RED

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
                self.grid[y_start + dy][x_start + dx].color = Colors.BRIGHT_BLUE

        holes_4 = [(1, 0), (1, 1)]
        holes_2 = [(4, 1), (5, 1), (5, 3), (6, 3)]
        for dx, dy in holes_4 + holes_2:
            if self.is_valid_cell(x_start + dx, y_start + dy):
                self.grid[y_start + dy][x_start + dx].value = 0
        if not (self.is_valid_cell(*self.entry) and self.is_valid_cell(*self.exit)):
            raise ValueError(
                "Oh gros imbécile tu peux pas mettre l'entrée ou la sortie dans un mur"
            )
        return 0


def color_element(maze: Maze, colors: list[Colors]):
    if len(colors) != 6:
        raise ValueError("frr met assez de couleurs")
    for cols in maze.grid:
        for cell in cols:
            if cell.value == 0 and not colors[0] is None:
                cell.color = colors[0]
            elif cell.value == 1 and not colors[1] is None:
                cell.color = colors[1]
            elif cell.value == 2 and not colors[2] is None:
                cell.color = colors[2]
            elif cell.value == 3 and not colors[3] is None:
                cell.color = colors[3]
            elif cell.value == 4 and not colors[4] is None:
                cell.color = colors[4]
            elif cell.value == 42 and not colors[5] is None:
                cell.color = colors[5]


def menu(args) -> None:
    from generate import generate
    from render_ascii import render
    from solver import solver

    color_names = [attr for attr in dir(Colors) if not attr.startswith("__")]

    caca = 0
    while True:
        shuffle(color_names)
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Change maze colors")
        print("4. Quit")
        choice = input("Choice? (1-4): ")
        m = Maze(args)
        m.place_42()
        generate(m)
        tab = [None for i in range(6)]
        tab[0] = Colors.BLACK
        color_element(m, tab)
        solver(m)
        render(m)
        if choice == "1":
            generate(m)
            solver(m)
            render(m)
        elif choice == "2":
            if caca % 2 == 0:
                solver(m)
            else:
                color_element(m, tab)
            caca += 1
        elif choice == "3":
            print("\n\n")
            print("=== Color Menu ===")
            print("1. Random colors")
            print("2. Change the color of an element")
            choice2 = input("Choice? (1-2): ")
            if choice2 == "1":
                print("\n\n")
                print("1. Random color of all elements")
                print("2. Random color single element")
                choice3 = input("Choice? (1-2): ")
                print("\n\n")
                if choice3 == "1":
                    color_element(color_names[:6])
                if choice3 == "2":
                    print("\n\n")
                    print("1. Random color of the wall")
                    print("2. Random color of the path")
                    print("3. Random color of the entry")
                    print("4. Random color of the exit")
                    print("5. Random color of the solution")
                    print("6. Random color of the 42")
                    choice4 = input("Choice? (1-2): ")
                    tab = [None for i in range(6)]
                    if choice4 == "1":
                        tab[1] = getattr(Colors, color_names[1])
                        color_element(m, tab)
                    elif choice4 == "2":
                        tab[2] = getattr(Colors, color_names[0])
                        color_element(m, tab)
                    elif choice4 == "3":
                        tab[3] = getattr(Colors, color_names[2])
                        color_element(m, tab)
                    elif choice4 == "4":
                        tab[4] = getattr(Colors, color_names[3])
                        color_element(m, tab)
                    elif choice4 == "5":
                        tab[5] = getattr(Colors, color_names[4])
                        color_element(m, tab)
                    elif choice4 == "6":
                        tab[6] = getattr(Colors, color_names[5])
                        color_element(m, tab)
                    render(m)
            elif choice2 == "2":
                selected_colors = {}

                for key, label in color_element.items():
                    choice5 = input(
                        f"Choose the color for {label} (Options: {color_names}): "
                    )

                    if choice5.upper() in color_names:
                        selected_colors[key] = choice5
                        print(f"-> {key.capitalize()} color set to: {choice5}.\n")
                    else:
                        print(f"Error: '{choice5}' is not a valid option !\n")

        elif choice == "4":
            exit()
        else:
            print("\nInvalid option, try again...\n")


def main(argv):
    args = parse(argv)
    args.print_o()
    menu(args)


if __name__ == "__main__":
    main(argv)
