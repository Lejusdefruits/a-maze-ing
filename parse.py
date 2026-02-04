from pathlib import Path
from sys import exit


from typing import NoReturn


def error(the_error: str) -> NoReturn:
    """Print an error message and exit the program."""
    exit("Error : " + the_error)


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

        print(entry_tab)
        data = dict(entry_tab)
        data.setdefault("RENDER", "ascii")
        self.validate(entry_tab)
        self.width = int(data["WIDTH"])
        self.height = int(data["HEIGHT"])
        self.entry = tuple(map(int, data["ENTRY"].replace(",", " ").split()))
        self.exit = tuple(map(int, data["EXIT"].replace(",", " ").split()))
        self.output_file = data["OUTPUT_FILE"]
        self.perfect = data["PERFECT"] == "True"
        self.render = data["RENDER"]
        self.seed = data["SEED"]

    def print_o(self) -> None:
        """Display the current maze configuration."""
        print("\n" + "=" * 30)
        print(f"{'MAZE CONFIGURATION':^30}")
        print("=" * 30)
        print(f"  Dimensions : {self.width}x{self.height}")
        print(f"  Entry      : {self.entry}")
        print(f"  Exit       : {self.exit}")
        print("-" * 30)
        print(f"  Perfect    : {self.perfect}")
        print(f"  Render     : {self.render}")
        print(f"  Output     : {self.output_file}")
        print(f"  Seed     : {self.seed}")
        print("=" * 30 + "\n")


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
        if len(line.split("=")) != 2:
            error("Format of entry file not valid")
        cleared_lines.append(
            (line.split("=")[0].strip(), line.split("=")[1].strip()))
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


def parse_coords(buffer: Entry) -> bool:
    """Check if entry and exit coordinates are within bounds."""
    return (
        buffer.exit[0] >= buffer.width
        or buffer.exit[1] >= buffer.height
        or buffer.entry[0] >= buffer.width
        or buffer.entry[1] >= buffer.height
        or any(n < 0 for n in [*buffer.entry, *buffer.exit])
    )


def parse(argv: list[str]) -> Entry:
    """Parse command-line arguments and initialize configuration."""
    if len(argv) != 2:
        error("Usage: 'python3 a_maze_ing.py config.txt'")
    buffer = Entry(format_read(read(argv[1])))
    if parse_coords(buffer):
        error("Coordinates not valid")
    if buffer.width % 2 != 0:
        buffer.width = buffer.width
    else:
        print(
            f"Width: {buffer.width} is pair "
            "so algo is not gonna work i add one"
        )
        buffer.width += 1
    if buffer.height % 2 != 0:
        buffer.height = buffer.height
    else:
        print(
            f"Height: {buffer.height} is pair "
            "so algo is not gonna work i add one"
        )
        buffer.height += 1
    return buffer
