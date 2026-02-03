import sys
from sys import argv
from random import shuffle, randint
from parse import Entry, parse
from time import sleep
from parse import error


sys.setrecursionlimit(100000)


class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    WHITE = "\033[37m"
    BRIGHT_YELLOW = "\033[93m"
    RED = "\033[31m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_GREEN = "\033[92m"
    ALL_NAMES = [
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "MAGENTA",
        "CYAN",
        "WHITE",
        "GRAY",
        "BRIGHT_RED",
        "BRIGHT_GREEN",
        "BRIGHT_YELLOW",
        "BRIGHT_BLUE",
        "BRIGHT_MAGENTA",
        "BRIGHT_CYAN",
        "BRIGHT_WHITE",
    ]
    ALL = [
        "\033[31m",
        "\033[32m",
        "\033[33m",
        "\033[34m",
        "\033[35m",
        "\033[36m",
        "\033[37m",
        "\033[90m",
        "\033[91m",
        "\033[92m",
        "\033[93m",
        "\033[94m",
        "\033[95m",
        "\033[96m",
        "\033[97m",
    ]


class Cell:
    def __init__(self, x, y):
        self.color = Colors.BLACK
        self.value = 1
        self.x = x
        self.y = y

    def dig(self):
        if self.value not in [2, 3, 42]:
            self.value = 0


class Maze:
    def __init__(self, args: Entry):
        self.solution = []
        self.width = args.width
        self.height = args.height
        self.entry = args.entry
        self.exit = args.exit
        self.output_file = args.output_file
        self.elements = ["PATH", "WALL", "ENTRY", "EXIT", "SOL", "42"]
        self.perfect = args.perfect
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.grid[self.entry[1]][self.entry[0]].value = 2
        self.grid[self.exit[1]][self.exit[0]].value = 3
        self.seed = args.seed

    def is_valid_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].value != 42
        return False

    def place_42(self):
        x_bloc, y_bloc = 7, 5
        if self.width < x_bloc or self.height < y_bloc:
            return -1
        x_start, y_start = (self.width - x_bloc) // 2, (self.height - y_bloc) // 2
        coords = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
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
        for dx, dy in coords:
            nx, ny = x_start + dx, y_start + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.exit[0] == nx and self.exit[1] == ny:
                    error(
                        f"Exit cannot be on coords {self.exit} "
                        "because 42 draw will be on it"
                    )
                self.grid[ny][nx].value = 42
                self.grid[ny][nx].color = Colors.BRIGHT_BLUE
        return 0


def get_tab_color(
    all_colors: list, id: str, elements: list[str], current_theme: list[str], rd: bool
) -> list:
    id = int(id) - 1
    result = [current_theme[i] for i in range(len(elements))]
    if rd:
        result[id] = all_colors[randint(0, len(all_colors) - 1)]
    else:
        result[id] = all_colors[0]
    return result


def apply_theme(maze, theme, show_sol):
    from render_ascii import render

    val_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 42: 5}
    for row in maze.grid:
        for cell in row:
            idx = val_map.get(cell.value)
            if idx is not None:
                if cell.value == 4 and not show_sol:
                    cell.color = theme[0]

                else:
                    if theme[idx] is not None:
                        if cell.value == 4:
                            sleep(0.03)
                            render(maze)
                        cell.color = theme[idx]


def color_menu(m: Maze, show_sol, current_theme):
    from render_ascii import render

    all_cols = list(Colors.ALL)
    print("=======Color menu=======")
    print("\n1. Random colors | 2. Choose colors")
    choice_colors_menu = input(">> ")
    if choice_colors_menu == "1":
        print("=======Random colors=======")
        print("0. Randomize all elements")
        for i, elt in enumerate(m.elements, start=1):
            print(f"{i}. Randomize color of '{elt}'")
        choose_elt = input(">> ")
        if choose_elt == "0":
            shuffle(all_cols)
            current_theme = all_cols[:6]
            apply_theme(m, current_theme, show_sol)
        else:
            current_theme = get_tab_color(
                all_cols, choose_elt, m.elements, current_theme, True
            )
            apply_theme(m, current_theme, show_sol)
    elif choice_colors_menu == "2":
        all_cols = list(Colors.ALL)
        for i, elt in enumerate(m.elements, start=1):
            print(f"{i}. Choose color of '{elt}'")
        choose_elt = input("\n\n>> ")
        for i, elt in enumerate(Colors.ALL_NAMES, start=1):
            print(f"{i}. '{elt}'")
        choose_color = input(">> ")
        all_cols[0] = Colors.ALL[int(choose_color) - 1]
        current_theme = get_tab_color(
            all_cols, choose_elt, m.elements, current_theme, False
        )
        apply_theme(m, current_theme, show_sol)

    render(m)
    return current_theme


def menu(args) -> None:
    from render_ascii import render
    from generate import generate
    from solver import solver
    from output import outpoute

    m = Maze(args)
    if m.seed != '0':
        from input import inp
        m = inp(m.seed)
    else:
        m.place_42()
        generate(m)
        m.solution = solver(m)

    current_theme = [
        Colors.BLACK,
        Colors.WHITE,
        Colors.BRIGHT_GREEN,
        Colors.RED,
        Colors.BRIGHT_YELLOW,
        Colors.BRIGHT_BLUE,
    ]
    show_sol = False

    apply_theme(m, current_theme, show_sol)
    render(m)

    while True:
        print(f"\n[ Sol: {'ON' if show_sol else 'OFF'} ]")
        print("1. New Maze | 2. Show/Hide Sol | 3. Color menu | 4. Quit")
        choice = input(">> ")

        if choice == "1":
            m = Maze(args)
            m.place_42()
            generate(m)
            m.solution = solver(m)
            apply_theme(m, current_theme, show_sol)
            render(m)
        elif choice == "2":
            show_sol = not show_sol
            apply_theme(m, current_theme, show_sol)
            render(m)
        elif choice == "3":
            current_theme = color_menu(m, show_sol, current_theme)
        elif choice == "4":
            outpoute(m)
            break


if __name__ == "__main__":
    args = parse(argv)
    menu(args)
