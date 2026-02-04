from typing import List, Tuple


class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    WHITE = "\033[37m"
    BRIGHT_YELLOW = "\033[93m"
    RED = "\033[31m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_GREEN = "\033[92m"
    ALL_NAMES = [
        "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "GRAY",
        "BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW", "BRIGHT_BLUE",
        "BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_WHITE"
    ]
    ALL = [
        "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m",
        "\033[37m", "\033[90m", "\033[91m", "\033[92m", "\033[93m", "\033[94m",
        "\033[95m", "\033[96m", "\033[97m"
    ]


class Cell:
    def __init__(self, x: int, y: int):
        self.color: str = Colors.WHITE
        self.value: int = 1
        self.x: int = x
        self.y: int = y
        self.north: int = 0
        self.south: int = 0
        self.east: int = 0
        self.west: int = 0

    def dig(self) -> None:
        if self.value not in [2, 3, 42]:
            self.value = 0


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        seed: str = "0",
        perfect: bool = True
    ):
        self.solution: List[Tuple[int, int]] = []
        self.width: int = width if width % 2 != 0 else width + 1
        self.height: int = height if height % 2 != 0 else height + 1
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.perfect: bool = perfect
        self.seed: str = seed
        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.grid[self.entry[1]][self.entry[0]].value = 2
        self.grid[self.exit[1]][self.exit[0]].value = 3
        self.elements: List[str] = [
            "PATH", "WALL", "ENTRY", "EXIT", "SOL", "42"
        ]

    def is_valid_cell(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].value != 42
        return False

    def place_42(self) -> int:
        x_bloc, y_bloc = 7, 5
        if self.width < x_bloc or self.height < y_bloc:
            return -1
        x_start = (self.width - x_bloc) // 2
        y_start = (self.height - y_bloc) // 2
        coords = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3),
            (2, 4), (4, 0), (5, 0), (6, 0), (6, 1), (4, 2), (5, 2), (6, 2),
            (4, 3), (4, 4), (5, 4), (6, 4)
        ]
        for dx, dy in coords:
            nx, ny = x_start + dx, y_start + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.exit == (nx, ny):
                    raise ValueError("Exit overlaps with '42' pattern")
                self.grid[ny][nx].value = 42
                self.grid[ny][nx].color = Colors.BRIGHT_BLUE
        return 0
