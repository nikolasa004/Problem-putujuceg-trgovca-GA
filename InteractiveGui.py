import pygame
import random
from City import City
from Individual import Individual
# Konstantne vrednosti
tile_size = 32
screen_width = tile_size * 40
screen_height = tile_size * 25

# Boje
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
# Učitavanje dekoracija
decor_images = []
for i in range(1, 11):
    image = pygame.image.load(f"Pictures/Decorations/Decor{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (tile_size, tile_size))
    decor_images.append(image)

block_images = []
for i in range(1, 11):
    image = pygame.image.load(f"Pictures/BackgroundBlocks/block{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (tile_size, tile_size))
    block_images.append(image)
# Inicijalizacija pygame-a
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Interaktivni TSP GUI")
font = pygame.font.SysFont(None, 16)

background_map = [
    [random.randint(0, 9) for _ in range(screen_width // tile_size)]
    for _ in range( screen_height // tile_size)
]
# Skaliranje koordinata
def calculate_scale(cities):
    max_x = max(city.x for city in cities)
    max_y = max(city.y for city in cities)
    scale_x = (screen_width - tile_size) / max_x
    scale_y = (screen_height - tile_size) / max_y
    return min(scale_x, scale_y)

# Dodela ikona gradovima
def assign_city_icons(cities):
    city_images = []
    for i in range(1, 11):
        img = pygame.image.load(f"Pictures/Cities/city{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (tile_size, tile_size))
        city_images.append(img)
    return [random.choice(city_images) for _ in cities]
def place_decorations(cities, num_decorations=30):
    global decor_positions2    
    decor_positions2 = []  # Lista za čuvanje pozicija dekoracija
    attempts = 0
    max_attempts = num_decorations * 10  # da se ne zaglavi u petlji
    while len(decor_positions2) < num_decorations and attempts < max_attempts:
        x = random.randint(1, screen_width - 2) * tile_size +  tile_size // 2
        y = random.randint(1, screen_height - 2) * tile_size + tile_size // 2

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
            for dx, dy, _ in decor_positions2:
                if abs(dx - x) < 64 and abs(dy - y) < 64:
                    too_close = True
                    break

        if not too_close:
            image = random.choice(decor_images)
            decor_positions2.append((x, y, image))

        attempts += 1

def draw_background(screen,scale):
    for y in range(screen_height//32):
        for x in range(screen_width//32):
            block_index = background_map[y][x]
            screen.blit(block_images[block_index], (x * tile_size, y * tile_size))

    for x, y, image in decor_positions2:
        screen.blit(image, (x - tile_size // 2, y - tile_size // 2))

# Crtanje svih gradova i njihovih imena
def draw_cities(cities, city_icons):
    for i, city in enumerate(cities):
        x = int(city.x * scale)
        y = int(city.y * scale)
        screen.blit(city_icons[i], (x - tile_size // 2, y - tile_size // 2))
        name_surface = font.render(city.name, True, BLACK)
        screen.blit(name_surface, (x - tile_size // 2, y + tile_size // 2))

# Crtanje linija između izabranih gradova
def draw_player_path(path):
    for i in range(len(path) - 1):
        x1, y1 = int(path[i].x * scale), int(path[i].y * scale)
        x2, y2 = int(path[i + 1].x * scale), int(path[i + 1].y * scale)
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)

# Pronalazak najbližeg grada prema kliku
def find_clicked_city(cities, pos):
    mouse_x, mouse_y = pos
    click_range = tile_size //2  # Povecano sa tile_size // 2 na tile_size
    for city in cities:
        x = int(city.x * scale)
        y = int(city.y * scale)
        if abs(mouse_x - x) < click_range and abs(mouse_y - y) < click_range:
            return city
    return None

# Glavna funkcija
def run_interactive_mode(cities, algorithm_result):
    global scale
    scale = calculate_scale(cities)
    place_decorations(cities)
    city_icons = assign_city_icons(cities)

    selected_path = []
    selected_names = set()
    undo_stack = []  # Stack za undo operacije
    done = False

    while not done:
        screen.fill(WHITE)
        draw_background(screen,scale)
        draw_cities(cities, city_icons)
        draw_player_path(selected_path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # U MOUSEBUTTONDOWN delu:
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_city = find_clicked_city(cities, pygame.mouse.get_pos())
                if clicked_city and clicked_city.name not in selected_names:
                    # zapamti prethodno stanje
                    undo_stack.append((selected_path.copy(), selected_names.copy()))
                    if len(undo_stack) > 5:
                        undo_stack.pop(0)

                    selected_path.append(clicked_city)
                    selected_names.add(clicked_city.name)
                    print(f"Grad '{clicked_city.name}' dodat u putanju.")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(selected_path) == len(cities):
                    selected_path.append(selected_path[0])  # zatvaranje kruga
                    user_individual = Individual(selected_path)
                    user_distance = user_individual.distance
                    result_distance = algorithm_result
                    print("Vasa distanca:", round(user_distance, 2))
                    print("Najbolja distanca algoritma:", round(result_distance, 2))
                    if user_distance < result_distance:
                        print("Cestitamo! Vas put je bolji od algoritma!")
                    elif user_distance == result_distance:
                        print("Vas put je jednako udaljen kao put algoritma!")
                    else:
                        print("Nazalost, vas put je losiji od puta algoritma.")
                    done = True

                elif event.key == pygame.K_r:
                    selected_path.clear()
                    selected_names.clear()
                    print("Putanja je resetovana. Mozete poceti ispocetka.")
                elif event.key == pygame.K_z:
                    if undo_stack:
                        selected_path, selected_names = undo_stack.pop()
                        print("Vraćen je prethodni korak.")
                    else:
                        print("Nema više koraka za vraćanje.")


        pygame.display.flip()
        

    pygame.quit()
