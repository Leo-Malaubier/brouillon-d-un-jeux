# main.py

import pygame
from pygame.locals import *

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
BROWN=(80,41,0)

# Classe principale pour gérer l'affichage 2D avec Pygame
class Game2D:
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
        pygame.display.set_caption('Game 2D')

        # Boucle principale du jeu
        self.run()

    def draw_map(self):
        """Fonction pour dessiner la carte en 2D."""
        cell_size = 30  # Taille des cellules en pixels

        for y in range(self.game_map.N_case):
            for x in range(self.game_map.N_case):
                cell_type = self.game_map.map[y][x].see_type()

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

                pygame.draw.rect(self.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

                # Dessiner le joueur si ses coordonnées correspondent
                if (x, y) == self.player_position:
                    pygame.draw.circle(self.screen, RED, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 3)
                    # Dessin du joueur (cercle rouge ici)
                    self.player.move((x,y))
                    print(self.player.see_position())
                # Dessiner les monstres si leurs coordonnées correspondent
                for monster_pos, monster in [(self.monster1_position, self.monster1), (self.monster2_position, self.monster2)]:
                    if (x, y) == monster_pos:
                        pygame.draw.rect(self.screen, BROWN, (x * cell_size, y * cell_size, cell_size, cell_size))
                        # Ici, nous dessinons un rectangle bleu pour représenter le monstre. Vous pouvez ajuster la forme et les couleurs selon vos besoins.

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

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.handle_player_input()  # Gestion des entrées du joueur

            self.screen.fill(WHITE)
            self.draw_map()

            pygame.display.update()
            clock.tick(30)

# Point d'entrée du programme
if __name__ == "__main__":
    game = Game2D()
