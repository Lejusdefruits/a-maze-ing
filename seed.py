import sys
import lzma
import base64

sys.set_int_max_str_digits(1000000000)


def get_seed(fichier_txt: str):
    with open(fichier_txt, "r") as f:
        contenu = f.read().strip().replace("\n", "|")

    compressed_data = lzma.compress(contenu.encode())
    seed = base64.b85encode(compressed_data).decode()
    return seed


def get_lab(seed_str: str):
    try:
        if not seed_str:
            return ""

        compressed_data = base64.b85decode(seed_str)
        decompressed_data = lzma.decompress(compressed_data)
        contenu = decompressed_data.decode()

        contenu = contenu.replace("|", "\n")
        return contenu
    except (lzma.LZMAError, ValueError) as e:
        if ("overflow" in str(e) or "bad" in str(e).lower()
                or "padding" in str(e).lower()):
            raise ValueError("Seed is corrupted or incomplete.")
        raise ValueError(f"Invalid seed data: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error decoding seed: {e}")


if __name__ == '__main__':
    seed = get_seed("output.txt")
    print(f"Generated Seed: {seed}")
    labyrinthe = get_lab(seed)
    with open("labyrinthe_reconstitue.txt", "w") as f:
        f.write(labyrinthe)
    print("Reconstruction successful.")
