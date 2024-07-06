try:
    from Class_player import class_player
    from statistique import statistique
except ValueError:
    from model.Class_player import class_player
    from model.statistique import statistique



class player(class_player,statistique):
    """Classe représentant un joueur dans le jeu."""
    def __init__(self, name, position=(0, 0), health=100):
        self.name = name  # Nom du joueur
        self.position = position  # Position du joueur sur la carte (x, y)
        self.health = health  # Santé du joueur
        self.inventory = []  # Inventaire des objets du joueur

    def __str__(self):
        return f"{self.name} at {self.position} with {self.health} health"

    def move(self, new_position):
        """Déplace le joueur à une nouvelle position."""
        self.position = new_position

    def take_damage(self, amount):
        """Réduit la santé du joueur."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Augmente la santé du joueur."""
        self.health += amount
        if self.health > 100:
            self.health = 100

    def add_to_inventory(self, item):
        """Ajoute un objet à l'inventaire du joueur."""
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        """Retire un objet de l'inventaire du joueur."""
        if item in self.inventory:
            self.inventory.remove(item)

    def see_inventory(self):
        """Retourne l'inventaire du joueur."""
        return self.inventory

    def see_position(self):
        """Retourne la position actuelle du joueur."""
        return self.position

    def see_health(self):
        """Retourne la santé actuelle du joueur."""
        return self.health
"""
# Exemple d'utilisation
if __name__ == "__main__":
    player = Player(name="Hero")
    print(player)

    player.move((5, 5))
    print("Moved to:", player.see_position())

    player.take_damage(20)
    print("Health after damage:", player.see_health())

    player.heal(15)
    print("Health after healing:", player.see_health())

    sword = Object(name="Sword", obj_type="Weapon", description="A sharp blade.")
    player.add_to_inventory(sword)
    print("Inventory:", player.see_inventory())

    player.remove_from_inventory(sword)
    print("Inventory after removing sword:", player.see_inventory())
"""
