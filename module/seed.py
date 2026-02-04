import sys


# Removed set_int_max_str_digits side effect from module level
# Users should ensure their environment handles large ints if needed


def get_seed(fichier_txt: str) -> int:
    """Read a file and convert its content to a seed integer."""
    with open(fichier_txt, "r") as f:
        contenu = f.read().strip().replace("\n", "|")

    seed = 0
    for char in contenu:
        seed = seed * 256 + ord(char)

    return seed


def get_seed_from_str(text: str) -> int:
    """Convert a string directly to a seed integer."""
    contenu = text.strip().replace("\n", "|")
    seed = 0
    for char in contenu:
        seed = seed * 256 + ord(char)
    return seed


def get_lab(seed_str: str) -> str:
    """Recover the original string content from a seed."""
    try:
        sys.set_int_max_str_digits(1000000000)
    except AttributeError:
        pass

    seed = int(seed_str)
    if seed == 0:
        return ""

    caracteres = []
    while seed > 0:
        caracteres.append(chr(seed % 256))
        seed = seed // 256

    contenu = "".join(reversed(caracteres))
    contenu = contenu.replace("|", "\n")

    return contenu
