class case:
    def __init__(self):
        self.player = False
        self.objects = []
        self.monster = None
        self.practical = True
        self.type = None
        self.hauteur = 0

    def move_player(self):
        """Toggle the player presence in the case."""
        self.player = not self.player

    def add_object(self, obj):
        """Add an object to the case."""
        self.objects.append(obj)

    def del_object(self, obj):
        """Remove an object from the case."""
        try:
            self.objects.remove(obj)
        except ValueError:
            print(f"{obj} not found in objects. Removing by index instead.")
            if isinstance(obj, int) and 0 <= obj < len(self.objects):
                self.objects.pop(obj)
            else:
                print(f"Invalid index: {obj}")

    def see_objects(self):
        """Return the list of objects in the case."""
        return self.objects

    def move_monster(self, monster):
        """Set the monster in the case."""
        self.monster = monster

    def see_monster(self):
        """Return the monster in the case."""
        return self.monster

    def change_practical(self):
        """Toggle the practical state of the case."""
        self.practical = not self.practical

    def see_practical(self):
        """Return the practical state of the case."""
        return self.practical

    def see_type(self):
        """Return the type of the case."""
        return self.type

    def change_type(self, case_type):
        """Set the type of the case."""
        self.type = case_type

    def see_all(self):
        """Return all attributes of the case."""
        return self.player, self.objects, self.monster, self.practical, self.type

    def change_hauteur(self, hauteur):
        """Set the height of the case."""
        self.hauteur = hauteur

    def see_hauteur(self):
        """Return the height of the case."""
        return self.hauteur
"""
# Usage example:
case = case()
case.move_player()
case.add_object("sword")
case.add_object("shield")
print(case.see_all())
"""
