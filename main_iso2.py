import pygame
from pygame.locals import *
import heapq

from model.map import map
from model.player import player
from model.monster import monster
from model.object import object

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre Pygame
display_width = 800
display_height = 600

# Couleurs RVB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (80, 41, 0)

class GameIso:
    def __init__(self):
        # Initialisation de la carte
        self.game_map = map(N_case=10)
        self.game_map.initialize_from_text([
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
        ])

        # Création du joueur et des monstres
        self.player = player(name="Hero")
        self.monster1 = monster(name="Goblin", health=50, strength=8)
        self.monster2 = monster(name="Orc", health=80, strength=12)

        # Position initiale du joueur et des monstres sur la carte
        self.player_position = (1, 8)
        self.monster1_position = (7, 1)
        self.monster2_position = (9, 9)

        # Ajout des monstres à la carte
        self.game_map.map[self.monster1_position[1]][self.monster1_position[0]].move_monster(self.monster1)
        self.game_map.map[self.monster2_position[1]][self.monster2_position[0]].move_monster(self.monster2)

        # Initialisation de Pygame
        self.display = (display_width, display_height)
        self.screen = pygame.display.set_mode(self.display)
        pygame.display.set_caption('Game Iso')

        # File d'attente pour le chemin du joueur
        self.player_path = []

        # Boucle principale du jeu
        self.run()

    def draw_map(self):
        """Fonction pour dessiner la carte en 3D isométrique."""
        cell_width = 60
        cell_height = 30

        for y in range(self.game_map.N_case):
            for x in range(self.game_map.N_case):
                cell_type = self.game_map.map[y][x].see_type()
                screen_x, screen_y = self.iso_coords(x, y, cell_width, cell_height)

                if cell_type == 'y':
                    color = WHITE
                elif cell_type == 'x':
                    color = BLUE
                elif cell_type == 'g':
                    color = GREEN
                elif cell_type == 't':
                    color = RED
                else:
                    color = WHITE  # Couleur par défaut pour les autres cases

                pygame.draw.polygon(self.screen, color, [
                    (screen_x, screen_y),
                    (screen_x + cell_width // 2, screen_y + cell_height // 2),
                    (screen_x, screen_y + cell_height),
                    (screen_x - cell_width // 2, screen_y + cell_height // 2)
                ])

                # Dessiner le joueur si ses coordonnées correspondent
                if (x, y) == self.player_position:
                    pygame.draw.circle(self.screen, RED, (screen_x, screen_y + cell_height // 4), cell_height // 4)
                    self.player.move((x,y))
                    print(self.player.see_position())

                # Dessiner les monstres si leurs coordonnées correspondent
                for monster_pos, monster in [(self.monster1_position, self.monster1), (self.monster2_position, self.monster2)]:
                    if (x, y) == monster_pos:
                        pygame.draw.polygon(self.screen, BROWN, [
                            (screen_x, screen_y),
                            (screen_x + cell_width // 2, screen_y + cell_height // 2),
                            (screen_x, screen_y + cell_height),
                            (screen_x - cell_width // 2, screen_y + cell_height // 2)
                        ])

    def iso_coords(self, x, y, cell_width, cell_height):
        """Convertit les coordonnées cartésiennes en coordonnées isométriques."""
        screen_x = (x - y) * (cell_width // 2) + display_width // 2
        screen_y = (x + y) * (cell_height // 2) + display_height // 4
        return screen_x, screen_y

    def cartesian_coords(self, screen_x, screen_y, cell_width, cell_height):
        """Convertit les coordonnées isométriques en coordonnées cartésiennes."""
        x = (screen_x - display_width // 2) // (cell_width // 2)
        y = (screen_y - display_height // 4) // (cell_height // 2)
        return (x + y) // 2, (y - x) // 2

    def handle_player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] or keys[pygame.K_a]:  # Déplacement à gauche
            self.move_player(-1, 0)
        elif keys[pygame.K_d]:  # Déplacement à droite
            self.move_player(1, 0)
        elif keys[pygame.K_z] or keys[pygame.K_w]:  # Déplacement vers le haut
            self.move_player(0, -1)
        elif keys[pygame.K_s]:  # Déplacement vers le bas
            self.move_player(0, 1)

    def move_player(self, dx, dy):
        new_x = self.player_position[0] + dx
        new_y = self.player_position[1] + dy

        if 0 <= new_x < self.game_map.N_case and 0 <= new_y < self.game_map.N_case:
            if self.game_map.map[new_y][new_x].see_type() != 'y':  # Vérifie si la case n'est pas un mur
                self.player_position = (new_x, new_y)

    def handle_mouse_input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:  # Clic droit de la souris
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cart_x, cart_y = self.cartesian_coords(mouse_x, mouse_y, 60, 30)
            if 0 <= cart_x < self.game_map.N_case and 0 <= cart_y < self.game_map.N_case:
                if self.game_map.map[cart_y][cart_x].see_type() != 'y':  # Vérifie si la case n'est pas un mur
                    path = self.find_path(self.player_position, (cart_x, cart_y))
                    if path:
                        self.player_path = path

    def find_path(self, start, goal):
        """Trouve le chemin le plus court entre start et goal en utilisant l'algorithme A*."""
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def neighbors(node):
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            result = []
            for dir in dirs:
                neighbor = (node[0] + dir[0], node[1] + dir[1])
                if 0 <= neighbor[0] < self.game_map.N_case and 0 <= neighbor[1] < self.game_map.N_case:
                    if self.game_map.map[neighbor[1]][neighbor[0]].see_type() != 'y':  # Vérifie si la case n'est pas un mur
                        result.append(neighbor)
            return result

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def move_along_path(self):
        """Déplace le joueur d'une étape le long du chemin calculé."""
        if self.player_path:
            self.player_position = self.player_path.pop(0)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.handle_player_input()  # Gestion des entrées du joueur
            self.handle_mouse_input()   # Gestion des entrées de la souris

            self.screen.fill(WHITE)
            self.draw_map()
            self.move_along_path()      # Déplace le joueur le long du chemin

            pygame.display.update()
            clock.tick(30)

# Point d'entrée du programme
if __name__ == "__main__":
    game = GameIso()
