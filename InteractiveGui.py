import pygame
import random
from City import City
from Individual import Individual

# Konstantne vrednosti
tile_size = 32
tiles_x = 40
tiles_y = 25
screen_width = tile_size * tiles_x
screen_height = tile_size * tiles_y

# Boje
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def calculate_scale(cities):
    max_x = max(city.x for city in cities)
    max_y = max(city.y for city in cities)
    scale_x = (screen_width - tile_size) / max_x
    scale_y = (screen_height - tile_size) / max_y
    return min(scale_x, scale_y)

def assign_city_icons(cities):
    city_images = []
    for i in range(1, 11):
        img = pygame.image.load(f"Pictures/Cities/city{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (tile_size, tile_size))
        city_images.append(img)
    return [random.choice(city_images) for _ in cities]

def place_decorations(cities, decor_images, scale, num_decorations=30):
    decor_positions = []
    attempts = 0
    max_attempts = num_decorations * 10
    while len(decor_positions) < num_decorations and attempts < max_attempts:
        x = random.randint(1, tiles_x - 2) * tile_size + tile_size // 2
        y = random.randint(1, tiles_y - 2) * tile_size + tile_size // 2

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

def generate_background():
    return [
        [random.randint(0, 9) for _ in range(tiles_x)]
        for _ in range(tiles_y)
    ]

def draw_background(screen, background_map, block_images, decor_positions):
    for y in range(tiles_y):
        for x in range(tiles_x):
            block_index = background_map[y][x]
            screen.blit(block_images[block_index], (x * tile_size, y * tile_size))

    for x, y, image in decor_positions:
        screen.blit(image, (x - tile_size // 2, y - tile_size // 2))

def draw_cities(screen, cities, city_icons, scale, font):
    for i, city in enumerate(cities):
        x = int(city.x * scale)
        y = int(city.y * scale)
        screen.blit(city_icons[i], (x - tile_size // 2, y - tile_size // 2))
        name_surface = font.render(city.name, True, BLACK)
        screen.blit(name_surface, (x - tile_size // 2, y + tile_size // 2))

def draw_player_path(screen, path, scale):
    for i in range(len(path) - 1):
        x1, y1 = int(path[i].x * scale), int(path[i].y * scale)
        x2, y2 = int(path[i + 1].x * scale), int(path[i + 1].y * scale)
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)

def draw_remaining_info(screen, cities, selected_names, font):
    remaining = [city for city in cities if city.name not in selected_names]
    remaining_count = len(remaining)
    
    # Prikaži broj preostalih gradova u gornjem desnom uglu
    info_text = f"Preostalo gradova: {remaining_count}"
    text_surface = font.render(info_text, True, (0, 0, 0))
    screen.blit(text_surface, (screen_width - text_surface.get_width() - 10, 10))

    # Ako ih je 5 ili manje, prikaži njihova imena ispod
    if remaining_count <= 5 and remaining_count > 0:
        for i, city in enumerate(remaining):
            name_surface = font.render(city.name, True, (0, 0, 0))
            screen.blit(name_surface, (screen_width - name_surface.get_width() - 10, 30 + i * 18))

def show_result_popup(user_distance, result_distance):
    pygame.init()
    popup_width = 600
    popup_height = 200
    popup = pygame.display.set_mode((popup_width, popup_height))
    pygame.display.set_caption("Rezultat")

    font_large = pygame.font.SysFont(None, 32)
    font_small = pygame.font.SysFont(None, 24)

    # Priprema teksta
    user_text = font_small.render(f"Vaša distanca: {round(user_distance, 2)}", True, (0, 0, 0))
    algo_text = font_small.render(f"Distanca algoritma: {round(result_distance, 2)}", True, (0, 0, 0))

    if user_distance < result_distance:
        result_msg = "Čestitamo! Vaš put je bolji od algoritma!"
    elif user_distance == result_distance:
        result_msg = "Vaš put je jednako dobar kao algoritamski!"
    else:
        result_msg = "Nažalost, vaš put je lošiji od algoritma."

    result_text = font_large.render(result_msg, True, (0, 100, 0))

    # Prikaz prozora dok korisnik ne klikne
    running = True
    while running:
        popup.fill((255, 255, 255))
        popup.blit(user_text, (20, 40))
        popup.blit(algo_text, (20, 80))
        popup.blit(result_text, (20, 130))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.flip()

    pygame.quit()



def find_clicked_city(cities, pos, scale):
    mouse_x, mouse_y = pos
    click_range = tile_size // 2
    for city in cities:
        x = int(city.x * scale)
        y = int(city.y * scale)
        if abs(mouse_x - x) < click_range and abs(mouse_y - y) < click_range:
            return city
    return None

# Glavna funkcija
def run_interactive_mode(cities, algorithm_result):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Interaktivni TSP GUI")
    font = pygame.font.SysFont(None, 16)

    # Učitavanje slika
    block_images = []
    for i in range(1, 11):
        img = pygame.image.load(f"Pictures/BackgroundBlocks/block{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (tile_size, tile_size))
        block_images.append(img)

    decor_images = []
    for i in range(1, 11):
        img = pygame.image.load(f"Pictures/Decorations/Decor{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (tile_size, tile_size))
        decor_images.append(img)

    background_map = generate_background()
    scale = calculate_scale(cities)
    decor_positions = place_decorations(cities, decor_images, scale)
    city_icons = assign_city_icons(cities)

    selected_path = []
    selected_names = set()
    undo_stack = []
    done = False

    while not done:
        screen.fill(WHITE)
        draw_background(screen, background_map, block_images, decor_positions)
        draw_cities(screen, cities, city_icons, scale, font)
        draw_player_path(screen, selected_path, scale)
        draw_remaining_info(screen, cities, selected_names, font)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_city = find_clicked_city(cities, pygame.mouse.get_pos(), scale)
                if clicked_city and clicked_city.name not in selected_names:
                    undo_stack.append((selected_path.copy(), selected_names.copy()))
                    if len(undo_stack) > 5:
                        undo_stack.pop(0)
                    selected_path.append(clicked_city)
                    selected_names.add(clicked_city.name)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(selected_path) == len(cities):
                    selected_path.append(selected_path[0])
                    user_individual = Individual(selected_path)
                    user_distance = user_individual.distance
                    result_distance = algorithm_result
                    pygame.quit()
                    show_result_popup(user_distance, result_distance)
                    return

                elif event.key == pygame.K_r:
                    selected_path.clear()
                    selected_names.clear()
                    print("Putanja resetovana.")
                elif event.key == pygame.K_z:
                    if undo_stack:
                        selected_path, selected_names = undo_stack.pop()
                        print("Vraćen je prethodni korak.")
                    else:
                        print("Nema više koraka za vraćanje.")

        pygame.display.flip()

    pygame.quit()
