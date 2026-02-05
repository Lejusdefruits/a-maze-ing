from pathlib import Path


from typing import NoReturn


class MazeError(Exception):
    """Custom exception for Maze application errors."""
    pass


def error(the_error: str) -> NoReturn:
    """Raise a MazeError with the given message."""
    raise MazeError("Error : " + the_error)


class Entry:
    """Class to parse and validate maze configuration entries."""

    def validate(self, entry_tab: list[tuple[str, str]]) -> bool:
        """Check if all required configuration arguments are present."""
        names_already = {name for name, _ in entry_tab}
        names_missing = set(self.name_args) - names_already

        if len(names_missing) > 2:
            error(
                f"{len(names_missing)} missing arguments :"
                f"{', '.join(names_missing)}"
            )
        elif len(names_missing) > 0:
            for miss in names_missing:
                if miss != self.name_args[6] and miss != self.name_args[7]:
                    error(
                        f"{len(names_missing)} missing arguments :"
                        f"{', '.join(names_missing)}"
                    )
        return True

    def __init__(self, entry_tab: list[tuple[str, str]]):
        self.name_args = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "RENDER",
            "SEED"
        ]

        data = dict(entry_tab)
        data.setdefault("RENDER", "ascii")
        self.validate(entry_tab)
        try:
            self.width = int(data["WIDTH"])
        except ValueError:
            error(f"Invalid WIDTH value: '{data['WIDTH']}'")

        try:
            self.height = int(data["HEIGHT"])
        except ValueError:
            error(f"Invalid HEIGHT value: '{data['HEIGHT']}'")

        try:
            self.entry = tuple(
                map(int, data["ENTRY"].replace(",", " ").split()))
            if len(self.entry) != 2:
                raise ValueError
        except ValueError:
            error(f"Invalid ENTRY format: '{data['ENTRY']}'. Expected 'x, y'")

        try:
            self.exit = tuple(map(int, data["EXIT"].replace(",", " ").split()))
            if len(self.exit) != 2:
                raise ValueError
        except ValueError:
            error(f"Invalid EXIT format: '{data['EXIT']}'. Expected 'x, y'")
        self.output_file = data["OUTPUT_FILE"]
        self.perfect = data["PERFECT"] == "True"
        self.render = data["RENDER"]
        self.seed = data["SEED"]

    def __str__(self) -> str:
        """Return the string representation of the maze configuration."""
        return (
            "\n" + "=" * 30 + "\n"
            f"{'MAZE CONFIGURATION':^30}\n"
            + "=" * 30 + "\n"
            f"  Dimensions : {self.width}x{self.height}\n"
            f"  Entry      : {self.entry}\n"
            f"  Exit       : {self.exit}\n"
            + "-" * 30 + "\n"
            f"  Perfect    : {self.perfect}\n"
            f"  Render     : {self.render}\n"
            f"  Output     : {self.output_file}\n"
            f"  Seed     : {self.seed}\n"
            + "=" * 30 + "\n"
        )

    def __repr__(self) -> str:
        return self.__str__()


def default_config(file_name: str) -> str:
    """Create a default configuration file if none exists."""
    with open(file_name, "w") as f:
        buffer = (
            "WIDTH=51\nHEIGHT=50\nENTRY=1, 1\nEXIT=45, 44\n"
            "OUTPUT_FILE=output.txt\nPERFECT=True\n"
            "RENDER=ascii\nSEED=0\n"
        )
        f.write(buffer)
    return buffer


def format_read(buffer: str) -> list[tuple[str, str]]:
    """Parse the configuration file content into a list of key-value pairs."""
    lines = [line.strip() for line in buffer.split("\n")]
    cleared_lines = []
    for line in lines:
        if line.startswith("#"):
            continue
        if len(line) == 0:
            continue
        if len(line.split("=", 1)) != 2:
            error(f"Invalid format line: '{line}'. Expected KEY=VALUE")
        cleared_lines.append(
            (line.split("=", 1)[0].strip(), line.split("=", 1)[1].strip()))
    return cleared_lines


def read(file_name: str) -> str:
    """Read content from the configuration file."""
    if not Path(file_name).exists():
        buffer = default_config(file_name)
    else:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                buffer = f.read()
        except PermissionError:
            error(
                f"STOP : Impossible acces to '{file_name}'. "
                "Verify permissions (chmod)."
            )
    return buffer


def validate_coords(buffer: Entry) -> None:
    """Check if entry and exit coordinates are within bounds."""
    if (
        buffer.entry[0] <= 0
        or buffer.entry[0] >= buffer.width - 1
        or buffer.entry[1] <= 0
        or buffer.entry[1] >= buffer.height - 1
    ):
        error(
            f"Entry {buffer.entry} cannot be on the border/walls "
            f"(Dimensions: {buffer.width}x{buffer.height})"
        )
    if (
        buffer.exit[0] <= 0
        or buffer.exit[0] >= buffer.width - 1
        or buffer.exit[1] <= 0
        or buffer.exit[1] >= buffer.height - 1
    ):
        error(
            f"Exit {buffer.exit} cannot be on the border/walls "
            f"(Dimensions: {buffer.width}x{buffer.height})"
        )
    if any(n < 0 for n in [*buffer.entry, *buffer.exit]):
        error("Coordinates cannot be negative")


def parse(argv: list[str]) -> Entry:
    """Parse command-line arguments and initialize configuration."""
    if len(argv) != 2:
        error("Usage: 'python3 a_maze_ing.py config.txt'")
    buffer = Entry(format_read(read(argv[1])))

    if buffer.width % 2 != 0:
        buffer.width = buffer.width
    else:
        print(
            f"Warning provided Width: {buffer.width} is even. "
            "Adjusting to odd number (Width + 1) for algorithm compatibility."
        )
        buffer.width += 1
    if buffer.height % 2 != 0:
        buffer.height = buffer.height
    else:
        print(
            f"Warning provided Height: {buffer.height} is even. "
            "Adjusting to odd number (Height + 1) for algorithm compatibility."
        )
        buffer.height += 1

    validate_coords(buffer)
    return buffer
