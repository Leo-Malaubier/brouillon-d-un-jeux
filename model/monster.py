# monster.py
class monster:
    """Classe représentant un monstre dans le jeu."""
    def __init__(self, name, health=100, strength=10):
        self.name = name  # Nom du monstre
        self.health = health  # Santé du monstre
        self.strength = strength  # Force du monstre

    def __str__(self):
        return f"{self.name} (Health: {self.health}, Strength: {self.strength})"

    def take_damage(self, amount):
        """Réduit la santé du monstre."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def attack(self):
        """Simule une attaque du monstre."""
        return self.strength

    def see_health(self):
        """Retourne la santé actuelle du monstre."""
        return self.health
"""
# Exemple d'utilisation
if __name__ == "__main__":
    monster = Monster(name="Orc", health=150, strength=15)
    print(monster)

    monster.take_damage(20)
    print("Health after damage:", monster.see_health())

    damage_dealt = monster.attack()
    print(f"{monster.name} dealt {damage_dealt} damage.")
"""
