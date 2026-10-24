import pygame
import random
import os
import City
import math

# Konstantne dimenzije
TILE_SIZE = 32
TILES_X = 40
TILES_Y = 25
SCREEN_WIDTH = TILE_SIZE * TILES_X
SCREEN_HEIGHT = TILE_SIZE * TILES_Y

# Skaliranje koordinata
max_city_x = 1740.0
max_city_y = 1175.0
scale_x = (SCREEN_WIDTH - TILE_SIZE) / max_city_x
scale_y = (SCREEN_HEIGHT - TILE_SIZE) / max_city_y
scale = min(scale_x, scale_y)

def compute_max_coordinates(cities):
    max_x = max(city.x for city in cities)
    max_y = max(city.y for city in cities)
    return max_x, max_y

def load_block_images():
    images = []
    for i in range(1, 11):
        image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pictures", "BackgroundBlocks", f"block{i}.png")).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        images.append(image)
    return images

def load_decor_images():
    images = []
    for i in range(1, 11):
        image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pictures", "Decorations", f"Decor{i}.png")).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        images.append(image)
    return images

def load_city_images():
    images = []
    for i in range(1, 11):
        image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pictures", "Cities", f"City{i}.png")).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        images.append(image)
    return images

# Generisanje pozadine
background_map = [
    [random.randint(0, 9) for _ in range(TILES_X)]
    for _ in range(TILES_Y)
]

def place_decorations(cities, decor_images, num_decorations=30):
    decor_positions = []
    attempts = 0
    max_attempts = num_decorations * 10
    while len(decor_positions) < num_decorations and attempts < max_attempts:
        x = random.randint(1, TILES_X - 2) * TILE_SIZE + TILE_SIZE // 2
        y = random.randint(1, TILES_Y - 2) * TILE_SIZE + TILE_SIZE // 2

        too_close = False
        for city in cities:
            cx = int(city.x * scale)
            cy = int(city.y * scale)
            if abs(cx - x) < 64 and abs(cy - y) < 64:
                too_close = True
                break

        if not too_close:
            for dx, dy, _ in decor_positions:
                if abs(dx - x) < 64 and abs(dy - y) < 64:
                    too_close = True
                    break

        if not too_close:
            image = random.choice(decor_images)
            decor_positions.append((x, y, image))

        attempts += 1
    return decor_positions

def draw_background(screen, block_images, decor_positions):
    for y in range(TILES_Y):
        for x in range(TILES_X):
            block_index = background_map[y][x]
            screen.blit(block_images[block_index], (x * TILE_SIZE, y * TILE_SIZE))

    for x, y, image in decor_positions:
        screen.blit(image, (x - TILE_SIZE // 2, y - TILE_SIZE // 2))

def assign_random_icons(cities, city_images):
    return [random.choice(city_images) for _ in cities]

def draw_cities(cities, city_icons, screen):
    font = pygame.font.SysFont(None, 14)
    for i, city in enumerate(cities):
        x = int(city.x * scale)
        y = int(city.y * scale)
        screen.blit(city_icons[i], (x - TILE_SIZE // 2, y - TILE_SIZE // 2))
        name_surface = font.render(city.name, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(x, y + 12))
        screen.blit(name_surface, name_rect)

def draw_path(cities, step, screen, color=(0, 0, 0), width=2):
    font = pygame.font.SysFont(None, 14)
    for i in range(step):
        city1 = cities[i]
        city2 = cities[(i + 1) % len(cities)]
        x1 = int(city1.x * scale)
        y1 = int(city1.y * scale)
        x2, y2 = int(city2.x * scale), int(city2.y * scale)
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)
        distance = math.sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)
        distance_text = font.render(f"{distance:.1f}", True, (255, 255, 255))
        screen.blit(distance_text, ((x1 + x2) // 2, (y1 + y2) // 2))

def draw_results(cities):
    global scale
    max_city_x, max_city_y = compute_max_coordinates(cities)
    scale = min((SCREEN_WIDTH - TILE_SIZE) / max(max_city_x, 1), (SCREEN_HEIGHT - TILE_SIZE) / max(max_city_y, 1))
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Problem putujućeg trgovca")

    block_images = load_block_images()
    decor_images = load_decor_images()
    city_images = load_city_images()

    city_icons = assign_random_icons(cities, city_images)
    decor_positions = place_decorations(cities, decor_images)

    running = True
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if step < len(cities):
                        step += 1

        draw_background(screen, block_images, decor_positions)
        draw_path(cities, step, screen)
        draw_cities(cities, city_icons, screen)

        pygame.display.flip()

    pygame.quit()
