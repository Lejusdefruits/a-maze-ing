class Vector2D:
    """Une classe pour comprendre les opérateurs mathématiques."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        print(f"🪄  __init__ appelé : Création d'un vecteur ({x}, {y})")

    def __str__(self):
        # Appelée par print()
        return f"Vecteur({self.x}, {self.y})"

    def __repr__(self):
        # Appelée par le debugger ou la console
        return f"Vector2D(x={self.x}, y={self.y})"

    def __add__(self, other):
        # Appelée par le signe +
        print(f"🪄  __add__ appelé : {self} + {other}")
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # Appelée par le signe -
        print(f"🪄  __sub__ appelé : {self} - {other}")
        return Vector2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        # Appelée par ==
        print(f"🪄  __eq__ appelé : Est-ce que {self} == {other} ?")
        return self.x == other.x and self.y == other.y


class MagicBag:
    """Une classe pour comprendre les conteneurs (len, [], in)"""

    def __init__(self, items):
        self.items = items

    def __str__(self):
        return f"Sac magique contenant : {self.items}"

    def __len__(self):
        # Appelée par len()
        print("🪄  __len__ appelé")
        return len(self.items)

    def __getitem__(self, index):
        # Appelée par obj[index]
        print(f"🪄  __getitem__ appelé avec l'index {index}")
        return self.items[index]

    def __contains__(self, item):
        # Appelée par 'in'
        print(f"🪄  __contains__ appelé pour '{item}'")
        return item in self.items

    def __call__(self):
        # Appelée par obj()
        print(
            "🪄  __call__ appelé : "
            "Je suis un objet mais on m'appelle comme une fonction !"
        )


def main():
    print("\n--- 1. INITIALISATION & AFFICHAGE ---")
    v1 = Vector2D(2, 3)
    v2 = Vector2D(5, 10)
    print(f"Affichage (__str__) : {v1}")
    print(f"Représentation (__repr__) : {repr(v1)}")

    print("\n--- 2. MATHÉMATIQUES ---")
    v3 = v1 + v2  # Appelle __add__
    print(f"Résultat : {v3}")

    v4 = v2 - v1  # Appelle __sub__
    print(f"Résultat : {v4}")

    print("\n--- 3. COMPARAISON ---")
    v_test = Vector2D(2, 3)
    print(f"Egalité ? {v1 == v_test}")  # Appelle __eq__
    print(f"Egalité ? {v1 == v2}")

    print("\n--- 4. CONTENEUR (LISTES) ---")
    sac = MagicBag(["Potion", "Épée", "Bouclier"])
    print(sac)

    print(f"Taille du sac : {len(sac)}")  # Appelle __len__

    item = sac[1]  # Appelle __getitem__
    print(f"L'objet à l'index 1 est : {item}")

    print(f"A-t-on une 'Potion' ? {'Potion' in sac}")  # Appelle __contains__

    print("\n--- 5. OBJET APPELABLE ---")
    sac()  # Appelle __call__


if __name__ == "__main__":
    main()
