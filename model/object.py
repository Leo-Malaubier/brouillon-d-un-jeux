# object.py

class object:
    """Classe représentant un objet dans le jeu."""
    def __init__(self, name, obj_type, description=""):
        self.name = name  # Nom de l'objet
        self.obj_type = obj_type  # Type de l'objet (par exemple, 'weapon', 'potion', etc.)
        self.description = description  # Description de l'objet (facultatif)

    def __str__(self):
        return f"{self.name} ({self.obj_type})"

    def see_name(self):
        return self.name

    def see_type(self):
        return self.obj_type

    def see_description(self):
        return self.description

    def change_description(self, new_description):
        self.description = new_description
"""
# Exemple d'utilisation
if __name__ == "__main__":
    sword = Object(name="Sword", obj_type="Weapon", description="A sharp blade.")
    potion = Object(name="Potion", obj_type="Consumable", description="Heals 50 HP.")

    print(sword)
    print(potion)
    print("Description:", sword.see_description())
    sword.change_description("A very sharp blade.")
    print("Updated Description:", sword.see_description())
"""
