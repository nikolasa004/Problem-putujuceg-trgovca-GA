import pygame
import random
import os
import City
import math


# Veličina bloka i ekrana
TILE_SIZE = 32
TILES_X = 40
TILES_Y = 25
SCREEN_WIDTH = TILE_SIZE * TILES_X
SCREEN_HEIGHT = TILE_SIZE * TILES_Y
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Maksimalne vrednosti koordinata
max_city_x = 1740.0
max_city_y = 1175.0

# Skaliranje koordinata
scale_x = (SCREEN_WIDTH - TILE_SIZE) / max_city_x
scale_y = (SCREEN_HEIGHT - TILE_SIZE) / max_city_y
scale = min(scale_x, scale_y)

# Učitavanje ikona (ne koriste se direktno ovde, može se ukloniti ako nije potrebno)
for i in range(1, 11):
    icon = pygame.image.load(f"Pictures/Cities/City{i}.png").convert_alpha()
    icon = pygame.transform.scale(icon, (16, 16))

# Učitavanje blokova pozadine
block_images = []
for i in range(1, 11):
    image = pygame.image.load(f"Pictures/BackgroundBlocks/block{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    block_images.append(image)

# Učitavanje dekoracija
decor_images = []
for i in range(1, 11):
    image = pygame.image.load(f"Pictures/Decorations/Decor{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    decor_images.append(image)


# Učitavanje slika gradova
city_images = []
for i in range(1, 11):
    image = pygame.image.load(f"Pictures/Cities/city{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    city_images.append(image)

# Generisanje matrice nasumičnih blokova
background_map = [
    [random.randint(0, 9) for _ in range(TILES_X)]
    for _ in range(TILES_Y)
]

def compute_max_coordinates(cities):
    max_x = max(city.x for city in cities)
    max_y = max(city.y for city in cities)
    return max_x, max_y


def place_decorations(cities, num_decorations=30):
    global decor_positions    
    decor_positions = []  # Lista za čuvanje pozicija dekoracija
    attempts = 0
    max_attempts = num_decorations * 10  # da se ne zaglavi u petlji
    while len(decor_positions) < num_decorations and attempts < max_attempts:
        x = random.randint(1, TILES_X - 2) * TILE_SIZE + TILE_SIZE // 2
        y = random.randint(1, TILES_Y - 2) * TILE_SIZE + TILE_SIZE // 2

        too_close = False

        # Provera da li je preblizu gradu
        for city in cities:
            cx = int(city.x * scale)
            cy = int(city.y * scale)
            if abs(cx - x) < 64 and abs(cy - y) < 64:
                too_close = True
                break

        # Provera da li je preblizu postojećem ukrasu
        if not too_close:
            for dx, dy, _ in decor_positions:
                if abs(dx - x) < 64 and abs(dy - y) < 64:
                    too_close = True
                    break

        if not too_close:
            image = random.choice(decor_images)
            decor_positions.append((x, y, image))

        attempts += 1

# Funkcija za crtanje pozadine
def draw_background(screen):
    for y in range(TILES_Y):
        for x in range(TILES_X):
            block_index = background_map[y][x]
            screen.blit(block_images[block_index], (x * TILE_SIZE, y * TILE_SIZE))

    for x, y, image in decor_positions:
        screen.blit(image, (x - TILE_SIZE // 2, y - TILE_SIZE // 2))

# Funkcija za dodelu nasumičnih ikonica gradovima
def assign_random_icons(cities):
    return [random.choice(city_images) for _ in cities]

# Funkcija za crtanje gradova sa prethodno dodeljenim ikonama
def draw_cities(cities, city_icons, screen):
    pygame.font.init()  # Inicijalizuj pygame font modul
    font = pygame.font.SysFont(None, 14)  # Font veličine 14
    for i, city in enumerate(cities):
        x = int(city.x * scale)
        y = int(city.y * scale)
        screen.blit(city_icons[i], (x - TILE_SIZE // 2, y - TILE_SIZE // 2))
        
        name_surface = font.render(city.name, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(x, y + 12))  # malo ispod ikonice
        screen.blit(name_surface, name_rect)

def draw_path(cities, step, screen, color=(0, 0, 0), width=2):
    pygame.font.init()
    font = pygame.font.SysFont(None, 14)

    for i in range(step):
        if i >= len(cities) - 1:
            break
        city1 = cities[i]
        city2 = cities[i + 1]

        # Koordinate
        x1 = int(city1.x * scale)
        y1 = int(city1.y * scale)
        x2 = int(city2.x * scale)
        y2 = int(city2.y * scale)

        # Crtanje linije
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)

        # Prikaz razdaljine na sredini linije
        distance = math.sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)
        distance_text = font.render(f"{distance:.1f}", True, (255, 255, 255))
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        screen.blit(distance_text, (mid_x, mid_y))


# Glavna funkcija za prikaz rezultata
def draw_results(cities):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Problem putujućeg trgovca")
    city_icons = assign_random_icons(cities)
    max_x, max_y = compute_max_coordinates(cities)
    scale_x = (SCREEN_WIDTH - TILE_SIZE) / max_x
    scale_y = (SCREEN_HEIGHT - TILE_SIZE) / max_y
    scale = min(scale_x, scale_y)
    place_decorations(cities, num_decorations=30)
    running = True
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if step < len(cities) - 1:
                        step += 1

        draw_background(screen)
        draw_path(cities, step, screen)
        draw_cities(cities, city_icons, screen)

        pygame.display.flip()
    pygame.quit()
        