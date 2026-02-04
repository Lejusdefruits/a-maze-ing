import sys

sys.set_int_max_str_digits(1000000000)


def get_seed(fichier_txt: str):
    with open(fichier_txt, "r") as f:
        contenu = f.read().strip().replace("\n", "|")

    seed = 0
    for char in contenu:
        seed = seed * 256 + ord(char)

    return seed


def get_lab(seed_str: str):
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


if __name__ == '__main__':
    seed = get_seed("output.txt")
    labyrinthe = get_lab(seed)
    with open("labyrinthe_reconstitue.txt", "w") as f:
        f.write(labyrinthe)
    print(get_seed('output.txt'))
