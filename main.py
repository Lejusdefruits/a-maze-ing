import sys
from sys import argv
from random import shuffle, randint
from parse import parse, Entry
from time import sleep
from models import Maze, Colors
from generate import generate
from solver import solver
from output import outpoute


sys.setrecursionlimit(100000)
try:
    sys.set_int_max_str_digits(1000000000)
except AttributeError:
    pass  # Older python versions don't have this but also don't have the limit


def get_tab_color(
    new_color: str, id: str, elements: list[str], current_theme: list[str],
    rd: bool, all_colors: list = []
) -> list[str]:
    """Return a new theme list with the updated color for the element."""
    idx = int(id) - 1
    result = [current_theme[i] for i in range(len(elements))]
    if rd:
        result[idx] = all_colors[randint(0, len(all_colors) - 1)]
    else:
        result[idx] = new_color
    return result


def apply_theme(maze: Maze, theme: list[str], show_sol: bool) -> None:
    """Apply the selected color theme to the maze grid cells."""
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


def color_menu(m: Maze, show_sol: bool, current_theme: list[str]) -> list[str]:
    """Handle the color selection menu interactions."""
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
                "", choose_elt, m.elements, current_theme, True, all_cols
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
        try:
            chosen_color_code = Colors.ALL[int(choose_color) - 1]
        except (ValueError, IndexError):
            chosen_color_code = Colors.WHITE

        current_theme = get_tab_color(
            chosen_color_code, choose_elt, m.elements, current_theme, False
        )
        apply_theme(m, current_theme, show_sol)

    render(m)
    return current_theme


def menu(args: Entry) -> None:
    """Main menu loop for the application."""
    from render_ascii import render

    m = Maze(args)
    if m.seed != '0':
        from input import inp
        m = inp(m.seed)
        m.place_42()
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
            if m.seed != '0':
                from input import inp
                m = inp(m.seed)
            else:
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
