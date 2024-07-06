import pygame
import random
import math

def lerp(a, b, t):
    return a + t * (b - a)

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def grad(hash, x, y):
    h = hash & 3
    u = x if h & 1 else -x
    v = y if h & 2 else -y
    return u + v

def perlin(x, y, seed):
    p = [n for n in range(256)]
    random.Random(seed).shuffle(p)
    p += p
    xi = int(x) & 255
    yi = int(y) & 255
    xf = x - int(x)
    yf = y - int(y)
    u = fade(xf)
    v = fade(yf)
    n00 = grad(p[p[xi] + yi], xf, yf)
    n01 = grad(p[p[xi] + yi + 1], xf, yf - 1)
    n10 = grad(p[p[xi + 1] + yi], xf - 1, yf)
    n11 = grad(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)

def generate_perlin_noise_map(seed, width, height, scale=10):
    perlin_map = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            perlin_map[y][x] = (perlin(x / scale, y / scale, seed) + 1) / 2
    return perlin_map

def generate_terrain_map(seed, width, height):
    perlin_map = generate_perlin_noise_map(seed, width, height)
    terrain_map = []
    for y in range(height):
        row = []
        for x in range(width):
            if perlin_map[y][x] < 0.3:
                terrain = 'water'
            elif perlin_map[y][x] < 0.6:
                terrain = 'plains'
            elif perlin_map[y][x] < 0.8:
                terrain = 'forest'
            else:
                terrain = 'mountain'
            row.append(terrain)
        terrain_map.append(row)
    return terrain_map

def display_terrain_map(terrain_map):
    pygame.init()
    width = len(terrain_map[0])
    height = len(terrain_map)
    screen = pygame.display.set_mode((width * 10, height * 10))
    colors = {
        'water': (0, 0, 255),
        'plains': (0, 255, 0),
        'forest': (34, 139, 34),
        'mountain': (139, 137, 137)
    }
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for y in range(height):
            for x in range(width):
                pygame.draw.rect(screen, colors[terrain_map[y][x]], pygame.Rect(x * 10, y * 10, 10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Exemple d'utilisation
seed = "ma_seed_unique"
width = 100
height = 100

terrain_map = generate_terrain_map(seed, width, height)
display_terrain_map(terrain_map)
