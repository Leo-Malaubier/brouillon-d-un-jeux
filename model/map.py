from model.case import case
import heapq

class map:
    """Classe représentant une carte composée de cases."""
    def __init__(self, N_case=10):
        # N_case représente la taille de la carte, supposée carrée
        self.N_case = N_case
        self.map = self.create_map()

    def create_map(self):
        """Crée une carte de N_case x N_case avec des instances de la classe Case."""
        map = []
        for i in range(self.N_case):
            row = []
            for j in range(self.N_case):
                row.append(case())  # Utilisation correcte de la classe case pour créer des instances
            map.append(row)
        return map

    def initialize_from_text(self, text_representation):
        """Initialise la carte à partir d'une représentation textuelle."""
        print(text_representation)
        for y, row in enumerate(text_representation):
            print(row)
            for x, char in enumerate(row.split()):
                print(x,char)
                self.map[y][x].change_type(char)

    def print_map(self):
        """Affiche la carte actuelle avec les types de chaque case."""
        for row in self.map:
            row_str = " ".join(cell.see_type() if cell.see_type() else '.' for cell in row)
            print(row_str)

    def maping(self, elements):
        """Ajoute des éléments spécifiques à la carte."""
        for element in elements:
            x, y, type_ = element
            self.map[y][x].change_type(type_)

    def maping_routes(self, start, end):
        """Calcule la route optimale entre deux points en utilisant l'algorithme de Dijkstra."""
        def dijkstra(grid, start, end):
            N = len(grid)
            pq = [(0, start)]
            distances = {start: 0}
            parents = {start: None}
            while pq:
                current_distance, current_node = heapq.heappop(pq)
                if current_node == end:
                    break
                for neighbor in self.get_neighbors(current_node, N):
                    distance = current_distance + 1  # All moves have the same cost
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance
                        priority = distance
                        heapq.heappush(pq, (priority, neighbor))
                        parents[neighbor] = current_node
            return distances, parents

        def reconstruct_path(parents, start, end):
            path = []
            step = end
            while step is not None:
                path.append(step)
                step = parents.get(step)
            path.reverse()
            return path

        distances, parents = dijkstra(self.map, start, end)
        return reconstruct_path(parents, start, end)

    def get_neighbors(self, node, N):
        """Retourne les voisins valides d'une cellule dans la grille."""
        x, y = node
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                neighbors.append((nx, ny))
        return neighbors
"""
# Exemple d'utilisation
if __name__ == "__main__":
    # Représentation textuelle de la carte
    text_representation = [
        "y y y y y y y y y y",
        "y x x x y x x y g y",
        "y x x x y x x y x y",
        "y x x x y x x x x y",
        "y x x x x x x x x y",
        "y y y y x x x x x y",
        "y x x x x x x x x y",
        "y x x x x x x y y y",
        "y x x x x x x x t y",
        "y y y y e e y y y y"
    ]

    # Création et initialisation de la carte
    game_map = map(N_case=10)
    game_map.initialize_from_text(text_representation)
    game_map.print_map()


    # Ajout d'éléments spécifiques (par exemple, type 't' à la position (3, 3))
    elements_to_add = [
        (3, 3, 't'),
        (5, 5, 'e')
    ]
    game_map.maping(elements_to_add)
    game_map.print_map()

    # Calculer et afficher la route optimale entre deux points (par exemple, (0, 0) et (9, 9))
    start = (0, 0)
    end = (9, 9)
    path = game_map.maping_routes(start, end)
    print("Optimal path from {} to {}: {}".format(start, end, path))
"""
