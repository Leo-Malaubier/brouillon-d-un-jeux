import random
import pygame
import sys

def generate_map(seed, width, height):
    # Initialiser le générateur de nombres aléatoires avec la seed
    random.seed(seed)

    # Générer une carte de 'width' par 'height' avec des terrains aléatoires
    terrain_types = [0,1]
    game_map = []

    # Remplir la carte ligne par ligne
    for _ in range(height):
        # Initialiser une ligne vide
        row = []
        for _ in range(width):
            # Choisir un type de terrain aléatoire pour chaque cellule de la ligne
            terrain = random.choice(terrain_types)
            # Ajouter ce terrain à la ligne
            row.append(terrain)
        # Ajouter la ligne complète à la carte
        game_map.append(row)

    return game_map

# Exemple d'utilisation
seed = "ma_seed_unique"
width = 1000
height = 1000


#------------------------------------------------------ affichage
# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre et de la grille
largeur_fenetre = 800
hauteur_fenetre = 800
taille_case = 7  # Taille de chaque case de la grille

# Créer la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Grille avec Pygame")

# Couleur de la grille (R, G, B)
couleur_grille = (200, 200, 200)

# Exemple de liste représentant la grille (1 pour une case colorée, 0 pour une case vide)
# Vous pouvez remplacer cette liste par votre propre grille
grille = generate_map(seed, width, height)

# Couleurs pour les cases
couleur_case = (100, 100, 255)
couleur_vide = (255, 255, 255)

# Fonction pour dessiner la grille avec couleurs
def dessiner_grille_avec_couleurs():
    for y, ligne in enumerate(grille):
        for x, case in enumerate(ligne):
            couleur = couleur_case if case == 1 else couleur_vide
            rect = pygame.Rect(x * taille_case, y * taille_case, taille_case, taille_case)
            pygame.draw.rect(fenetre, couleur, rect)
            pygame.draw.rect(fenetre, couleur_grille, rect, 1)  # Dessiner les lignes de la grille

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'arrière-plan avec une couleur blanche
    fenetre.fill((255, 255, 255))

    # Dessiner la grille avec couleurs
    dessiner_grille_avec_couleurs()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
