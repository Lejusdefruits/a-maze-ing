from pathlib import Path


class Entry:
    def validate(self, entry_tab: list) -> bool:
        names_already = {name for name, _ in entry_tab}
        names_missing = set(self.name_args) - names_already

        if len(names_missing) > 2:
            raise ValueError(
                f"{len(names_missing)} missing arguments :"
                f"{', '.join(names_missing)}"
            )
        elif len(names_missing) > 0:
            for miss in names_missing:
                if miss != self.name_args[6] and miss != self.name_args[7]:
                    raise ValueError(
                        f"{len(names_missing)} missing arguments :"
                        f"{', '.join(names_missing)}"
                    )
        return True

    def __init__(self, entry_tab):
        self.name_args = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "DISCO",
            "RENDER",
        ]

        data = dict(entry_tab)
        data["DISCO"] = "False"
        data["RENDER"] = "ascii"
        self.validate(entry_tab)
        self.width = int(data["WIDTH"])
        self.height = int(data["HEIGHT"])
        self.entry = tuple(map(int, data["ENTRY"].replace(",", " ").split()))
        self.exit = tuple(map(int, data["EXIT"].replace(",", " ").split()))
        self.output_file = data["OUTPUT_FILE"]
        self.perfect = data["PERFECT"] == "True"
        self.disco = data["DISCO"] == "True"
        self.render = data["RENDER"]

    def print_o(self):
        print("\n" + "=" * 30)
        print(f"{'MAZE CONFIGURATION':^30}")
        print("=" * 30)
        print(f"  Dimensions : {self.width}x{self.height}")
        print(f"  Entry      : {self.entry}")
        print(f"  Exit       : {self.exit}")
        print("-" * 30)
        print(f"  Perfect    : {self.perfect}")
        print(f"  Disco      : {self.disco}")
        print(f"  Render     : {self.render}")
        print(f"  Output     : {self.output_file}")
        print("=" * 30 + "\n")


def default_config(file_name: str):
    with open(file_name, "w") as f:
        buffer = (
            "WIDTH=51\nHEIGHT=50\nENTRY=1, 1\nEXIT=45, 44\n"
            "OUTPUT_FILE=output.txt\nPERFECT=True\n"
            "DISCO=True\nRENDER=ascii\n"
        )
        f.write(buffer)
    return buffer


def format_read(buffer: str) -> str:
    lines = [line.strip() for line in buffer.split("\n")]
    cleared_lines = []
    for line in lines:
        if line.startswith("#"):
            continue
        if len(line) == 0:
            continue
        if len(line.split("=")) != 2:
            raise ValueError("Format of entry file not valid")
        cleared_lines.append((line.split("=")[0].strip(), line.split("=")[1].strip()))
    return cleared_lines


def read(file_name: str) -> str:
    if not Path(file_name).exists():
        buffer = default_config(file_name)
    else:
        with open(file_name, "r", encoding="utf-8") as f:
            buffer: str = f.read()
    buffer = format_read(buffer)
    return buffer


def parse_coords(buffer: Entry) -> bool:
    return (
        buffer.exit[0] > buffer.width
        or buffer.exit[1] > buffer.height
        or buffer.entry[0] > buffer.width
        or buffer.entry[1] > buffer.height
        or any(n < 0 for n in [*buffer.entry, *buffer.exit])
    )


def parse(argv: str) -> Entry:
    if len(argv) != 2:
        raise ValueError("Usage: 'python3 a_maze_ing.py config.txt'")
    buffer = Entry(read(argv[1]))
    if parse_coords(buffer):
        raise ValueError("Coordinates not valid")
    buffer.width = buffer.width if buffer.width % 2 != 0 else buffer.width + 1
    buffer.height = buffer.height if buffer.height % 2 != 0 else buffer.height + 1
    return buffer
