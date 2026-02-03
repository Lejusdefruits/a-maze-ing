import sys

sys.set_int_max_str_digits(1000000000)


def get_seed(fichier_txt: str):
    with open(fichier_txt, "r") as f:
        contenu = f.read().strip().replace("\n", "|")

    seed = 0
    for char in contenu:
        seed = seed * 256 + ord(char)

    return seed


def get_lab(seed: str):
    seed = int(seed)
    if seed == 0:
        return ""

    caracteres = []
    while seed > 0:
        caracteres.append(chr(seed % 256))
        seed = seed // 256

    contenu = "".join(reversed(caracteres))
    contenu = contenu.replace("|", "\n")

    return contenu


seed = get_seed("output.txt")

labyrinthe = get_lab(seed)

with open("labyrinthe_reconstitue.txt", "w") as f:
    f.write(labyrinthe)

if __name__ == '__main__':
    print(get_seed('output.txt'))
