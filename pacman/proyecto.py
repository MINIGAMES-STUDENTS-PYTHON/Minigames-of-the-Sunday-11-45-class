import pygame
import sys
import random
import math

# ---------------------------- CONFIGURACIÓN INICIAL ----------------------------
pygame.init()
TILE_SIZE   = 24
MAP_WIDTH   = 28    # 28 columnas
MAP_HEIGHT  = 31    # 31 filas
TOP_MARGIN  = 40
WIDTH       = MAP_WIDTH * TILE_SIZE
HEIGHT      = MAP_HEIGHT * TILE_SIZE + TOP_MARGIN
FPS         = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# ---------------------------- COLORES ----------------------------
BLACK   = (0, 0, 0)
YELLOW  = (255, 255, 0)
BLUE    = (0, 0, 255)
WHITE   = (255, 255, 255)
PINK    = (255, 105, 180)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
CYAN    = (0, 255, 255)
ORANGE  = (255, 165, 0)

# ---------------------------- LAYOUT DEL MAPA (31 filas x 28 columnas) ----------------------------
# Cada fila tiene EXACTAMENTE 28 caracteres.
# "#"  = pared  
# "."  = camino con pellet  
# "o"  = camino con power pellet  
# " "  = camino sin pellet (por ejemplo, para portales o para la ghost house)
maze_layout = [
       # row 28
    "############################",   # row  0
    "#............##............#",   # row  1
    "#.####.#####.##.#####.####.#",   # row  2
    "#o####.#####.##.#####.####o#",   # row  3
    "#.####.#####.##.#####.####.#",   # row  4
    "#..........................#",   # row  5
    "#.####.##.########.##.####.#",   # row  6
    "#.####.##.########.##.####.#",   # row  7
    "#......##....##....##......#",   # row  8
    " .####.#####.##.#####.###. #",   # row  9
    "#..........................#",   # row 10
    "#..........................#",   # row 11
    "#..........................#",   # row 12
    "#.####.##..........##.####.#",   # row 13
    "#...........####...........#",   # row 14 -> Zona de la ghost house
    "#..#####............#####..#",   # row 15 -> Zona de la ghost house
    "#..........................#",   # row 16 -> Zona de la ghost house
    " .####.#####.##.#####.###.  ",  # row 17 -> Portales laterales (espacios en ambos extremos)
    "#......##....##....##......#",   # row 18
    "#.####.##.########.##.####.#",   # row 19
    "#o..##................##..o#",   # row 20
    "###.##.##.########.##.##.###",   # row 21
    "#......##....##....##......#",   # row 22
    "#.##########.##.##########.#",   # row 23
    "#..........................#",   # row 24
    "############################",   # row 25
    "############################",   # row 26
    "############################",
    "############################",
    "############################",
    "############################",   # row 27
   # row 30
]

# Comprobar que cada fila tenga 28 caracteres
for idx, row in enumerate(maze_layout):
    if len(row) != 28:
        print(f"Error en row {idx}: longitud {len(row)}")
        sys.exit(1)

# Convertir el layout en un mapa numérico: 1 = pared, 0 = camino.
game_map = [[1 if ch == "#" else 0 for ch in row] for row in maze_layout]

# ---------------------------- FUNCIONES UTILITARIAS ----------------------------
def can_move(x, y):
    """Retorna True si la celda (x, y) es transitable (no es pared)."""
    return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and game_map[y][x] == 0

def is_wall(x, y):
    """Retorna True si la celda (x, y) es una pared."""
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return game_map[y][x] == 1
    return False

# ---------------------------- CASA DE FANTASMAS ----------------------------
# Para acercarnos al original, definimos la ghost house en la región central.
# La asignamos a un rectángulo de 8 columnas x 4 filas centrado horizontalmente.
# Calculamos: left = (MAP_WIDTH - 8)//2 * TILE_SIZE, top = 10 * TILE_SIZE + TOP_MARGIN (por ejemplo).
ghost_house_rect = pygame.Rect(((MAP_WIDTH - 8) // 2) * TILE_SIZE,
                               10 * TILE_SIZE + TOP_MARGIN,
                               8 * TILE_SIZE,
                               4 * TILE_SIZE)
# La base para resucitar fantasmas se define en el centro de la ghost house.
# Dado que ghost_house_rect.left = (28-8)//2 * 24 = 10 * 24, ghost_house_rect.top = 10 * 24 + TOP_MARGIN,
# su centro en tile se calcula como:
#   center_x = 10 + 8/2 = 14 y center_y = 10 + 4/2 = 12
ghost_house_center = (14, 12)

# ---------------------------- VARIABLES DEL JUEGO ----------------------------
player_pos = [1, 1]         # (col, fila)
player_direction = (1, 0)   # Inicialmente a la derecha
score = 0
lives = 3
pellets = []                # Lista de pellets (cada uno [x, y])
power_pellets = []          # Lista de power pellets
fruit = None
fruit_timer = 0
ghost_vulnerable = False
vulnerable_timer = 0
animation_timer = 0         # Para animar la boca de Pac-Man

ghost_move_counter = 0
ghost_move_interval = 3     # Actualización de fantasmas cada 3 frames

# ---------------------------- INICIALIZAR PELLETS ----------------------------
def init_pellets():
    global pellets, power_pellets
    pellets = []
    power_pellets = []
    # Excluir la zona de la ghost house: filas 10 ≤ y < 14 y columnas 10 ≤ x < 18.
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if 10 <= y < 14 and 10 <= x < 18:
                continue
            ch = maze_layout[y][x]
            if ch == '.':
                pellets.append([x, y])
            elif ch == 'o':
                power_pellets.append([x, y])
init_pellets()

# ---------------------------- DIBUJAR ELEMENTOS DEL MAPA ----------------------------
def draw_map():
    border_thickness = 3
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            # Saltar la zona de la ghost house
            if 10 <= y < 14 and 10 <= x < 18:
                continue
            if is_wall(x, y):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TOP_MARGIN, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLACK, rect)
                if not is_wall(x, y - 1):
                    pygame.draw.line(screen, BLUE, (rect.left, rect.top), (rect.right, rect.top), border_thickness)
                if not is_wall(x, y + 1):
                    pygame.draw.line(screen, BLUE, (rect.left, rect.bottom), (rect.right, rect.bottom), border_thickness)
                if not is_wall(x - 1, y):
                    pygame.draw.line(screen, BLUE, (rect.left, rect.top), (rect.left, rect.bottom), border_thickness)
                if not is_wall(x + 1, y):
                    pygame.draw.line(screen, BLUE, (rect.right, rect.top), (rect.right, rect.bottom), border_thickness)

def draw_ghost_house():
    # Dibujar la ghost house con un diseño más fiel al original:
    # Se dibuja un rectángulo azul, se le añade un "domo" en la parte superior y se crea una puerta central
    pygame.draw.rect(screen, BLUE, ghost_house_rect)
    # Domo: dibujar un arco semicircular en la parte superior de la ghost house
    dome_rect = pygame.Rect(ghost_house_rect.left,
                            ghost_house_rect.top - ghost_house_rect.width // 2,
                            ghost_house_rect.width,
                            ghost_house_rect.width)
    pygame.draw.arc(screen, BLUE, dome_rect, math.pi, 2*math.pi, 3)
    # Puerta: una interrupción en el borde inferior central
    door_width = TILE_SIZE
    door_rect = pygame.Rect(ghost_house_rect.centerx - door_width // 2,
                            ghost_house_rect.bottom - 3,
                            door_width,
                            3)
    pygame.draw.rect(screen, BLACK, door_rect)

def draw_pellets():
    for p in pellets:
        cx = p[0] * TILE_SIZE + TILE_SIZE // 2
        cy = p[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
        pygame.draw.circle(screen, WHITE, (cx, cy), 4)
    for p in power_pellets:
        cx = p[0] * TILE_SIZE + TILE_SIZE // 2
        cy = p[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
        pygame.draw.circle(screen, WHITE, (cx, cy), 8)

def draw_fruit():
    if fruit:
        cx = fruit[0] * TILE_SIZE + TILE_SIZE // 2
        cy = fruit[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
        pygame.draw.circle(screen, GREEN, (cx, cy), 6)

# ---------------------------- PANTALLA Y ANIMACIONES DE PAC-MAN ----------------------------
def draw_player():
    global animation_timer
    cx = player_pos[0] * TILE_SIZE + TILE_SIZE // 2
    cy = player_pos[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
    r = TILE_SIZE // 2 - 3
    pygame.draw.circle(screen, YELLOW, (cx, cy), r)
    gap = math.radians(20 + 10 * abs(math.sin(animation_timer)))
    angle = math.atan2(player_direction[1], player_direction[0]) if player_direction != (0,0) else 0
    a1 = angle + gap
    a2 = angle - gap
    p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
    p2 = (cx + r * math.cos(a2), cy + r * math.sin(a2))
    pygame.draw.polygon(screen, BLACK, [(cx, cy), p1, p2])

def animate_defeat():
    defeat_frames = 60
    for i in range(defeat_frames):
        screen.fill(BLACK)
        draw_map()
        draw_ghost_house()
        draw_pellets()
        draw_fruit()
        for ghost in ghosts:
            ghost.draw(ghost_vulnerable)
        progress = i / defeat_frames
        current_gap = math.radians(30) * (1 - progress) + math.radians(150) * progress
        cx = player_pos[0] * TILE_SIZE + TILE_SIZE // 2
        cy = player_pos[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
        r = TILE_SIZE // 2 - 3
        pygame.draw.circle(screen, YELLOW, (cx, cy), r)
        angle = math.atan2(player_direction[1], player_direction[0]) if player_direction != (0,0) else 0
        a1 = angle + current_gap/2
        a2 = angle - current_gap/2
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        p2 = (cx + r * math.cos(a2), cy + r * math.sin(a2))
        pygame.draw.polygon(screen, BLACK, [(cx, cy), p1, p2])
        pygame.display.flip()
        clock.tick(FPS)

# ---------------------------- SPRITES DE FANTASMAS ----------------------------
def draw_ghost_eyes(pos):
    """Dibuja los ojos de un fantasma en modo 'eaten'."""
    cx = pos[0] * TILE_SIZE + TILE_SIZE // 2
    cy = pos[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
    offset = 4
    r_eye = 3
    left_eye = (cx - offset, cy - offset)
    right_eye = (cx + offset, cy - offset)
    pygame.draw.circle(screen, WHITE, left_eye, r_eye)
    pygame.draw.circle(screen, WHITE, right_eye, r_eye)
    pygame.draw.circle(screen, BLACK, left_eye, 1)
    pygame.draw.circle(screen, BLACK, right_eye, 1)

def draw_ghost_sprite(cx, cy, r, color):
    """Dibuja un sprite personalizado para el fantasma con cabeza circular y base ondulada."""
    # Dibujar la cabeza
    pygame.draw.circle(screen, color, (cx, cy), r)
    # Dibujar la base ondulada mediante zigzags
    num_zig = 5
    zig_width = (2 * r) / num_zig
    bottom = cy + r
    pts = [(cx - r, bottom)]
    for i in range(num_zig + 1):
        x = cx - r + i * zig_width
        y = bottom - 5 if i % 2 == 0 else bottom
        pts.append((x, y))
    pygame.draw.polygon(screen, color, pts)
    pygame.draw.circle(screen, WHITE, (cx, cy), r, 2)

def draw_ghost_final(ghost, vulnerable):
    if ghost.mode == "eaten":
        draw_ghost_eyes(ghost.pos)
    else:
        col = BLUE if vulnerable else ghost.color
        cx = ghost.pos[0] * TILE_SIZE + TILE_SIZE // 2
        cy = ghost.pos[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_MARGIN
        draw_ghost_sprite(cx, cy, TILE_SIZE // 2 - 4, col)

def draw_all_ghosts(vulnerable):
    for ghost in ghosts:
        draw_ghost_final(ghost, vulnerable)

# ---------------------------- CLASE GHOST ----------------------------
class Ghost:
    def __init__(self, x, y, color):
        self.start_pos = [x, y]
        self.pos = [x, y]
        self.color = color
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.mode = "normal"  # "normal" o "eaten"
    def reset(self):
        self.pos = self.start_pos.copy()
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.mode = "normal"
    def update(self, target, vulnerable):
        if self.mode == "eaten":
            # Revivir: si la distancia a la base es menor a 0.5, cambia a "normal"
            if math.hypot(self.pos[0] - ghost_house_center[0], self.pos[1] - ghost_house_center[1]) < 0.5:
                self.mode = "normal"
            else:
                best_move = None
                best_dist = float('inf')
                for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_x = self.pos[0] + move[0]
                    new_y = self.pos[1] + move[1]
                    if can_move(new_x, new_y):
                        dist = math.hypot(new_x - ghost_house_center[0], new_y - ghost_house_center[1])
                        if dist < best_dist:
                            best_dist = dist
                            best_move = move
                if best_move:
                    self.pos[0] += best_move[0]
                    self.pos[1] += best_move[1]
        else:
            # Modo vulnerable: movimiento aleatorio
            if vulnerable:
                possible_moves = []
                for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_x = self.pos[0] + move[0]
                    new_y = self.pos[1] + move[1]
                    if can_move(new_x, new_y):
                        possible_moves.append(move)
                if possible_moves:
                    choice = random.choice(possible_moves)
                    self.pos[0] += choice[0]
                    self.pos[1] += choice[1]
            else:
                # Modo normal: con vacilación aleatoria y búsqueda de la dirección óptima hacia Pac-Man.
                if random.random() < 0.2:
                    return  # Vacilación: no se mueve este frame
                valid_moves = []
                for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_x = self.pos[0] + move[0]
                    new_y = self.pos[1] + move[1]
                    if can_move(new_x, new_y):
                        valid_moves.append(move)
                if valid_moves and random.random() < 0.3:
                    choice = random.choice(valid_moves)
                    self.pos[0] += choice[0]
                    self.pos[1] += choice[1]
                else:
                    best_move = None
                    best_dist = float('inf')
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        new_x = self.pos[0] + dx
                        new_y = self.pos[1] + dy
                        if can_move(new_x, new_y):
                            dist = math.hypot(new_x - target[0], new_y - target[1])
                            if dist < best_dist:
                                best_dist = dist
                                best_move = (dx, dy)
                    if best_move:
                        self.pos[0] += best_move[0]
                        self.pos[1] += best_move[1]
    def draw(self, vulnerable):
        draw_ghost_final(self, vulnerable)

# ---------------------------- CREAR FANTASMAS ----------------------------
# Iniciar los fantasmas en la ghost house (por ejemplo, en la base de la casa).
ghosts = [
    Ghost(13, 13, RED),    # Blinky
    Ghost(14, 13, PINK),   # Pinky
    Ghost(13, 14, CYAN),   # Inky
    Ghost(14, 14, ORANGE)  # Clyde
]

# ---------------------------- FUNCIONES ADICIONALES ----------------------------
def spawn_fruit():
    empty = [p for p in pellets if p != player_pos]
    return random.choice(empty) if empty else None

def reset_game():
    global player_pos, player_direction, fruit, fruit_timer, ghost_vulnerable, vulnerable_timer
    player_pos = [1, 1]
    player_direction = (1, 0)
    for ghost in ghosts:
        ghost.reset()
    fruit = None
    fruit_timer = 0
    ghost_vulnerable = False
    vulnerable_timer = 0

def draw_ui():
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    lives_text = font.render(f"Vidas: {lives}", True, WHITE)
    screen.blit(score_text, (10, 5))
    screen.blit(lives_text, (WIDTH - 120, 5))

# ---------------------------- BUCLE PRINCIPAL ----------------------------
running = True
while running:
    screen.fill(BLACK)
    draw_map()
    draw_ghost_house()
    draw_pellets()
    draw_fruit()
    draw_player()
    draw_all_ghosts(ghost_vulnerable)
    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)
    
    animation_timer += 0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de Pac-Man (con portales laterales)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx, dy = -1, 0
        player_direction = (-1, 0)
    elif keys[pygame.K_RIGHT]:
        dx, dy = 1, 0
        player_direction = (1, 0)
    elif keys[pygame.K_UP]:
        dx, dy = 0, -1
        player_direction = (0, -1)
    elif keys[pygame.K_DOWN]:
        dx, dy = 0, 1
        player_direction = (0, 1)
        
    new_x = (player_pos[0] + dx) % MAP_WIDTH
    new_y = (player_pos[1] + dy) % MAP_HEIGHT
    if can_move(new_x, new_y):
        player_pos = [new_x, new_y]

    if player_pos in pellets:
        pellets.remove(player_pos)
        score += 10
    if player_pos in power_pellets:
        power_pellets.remove(player_pos)
        score += 50
        ghost_vulnerable = True
        vulnerable_timer = FPS * 10

    if fruit and player_pos == fruit:
        score += 100
        fruit = None

    for ghost in ghosts:
        if player_pos == ghost.pos:
            if ghost.mode == "eaten":
                continue
            elif ghost_vulnerable:
                score += 200
                ghost.mode = "eaten"

            else:
                lives -= 1
                if lives == 0:
                    animate_defeat()
                    font = pygame.font.SysFont("Arial", 48)
                    go_text = font.render("¡Game Over!", True, RED)
                    screen.blit(go_text, (WIDTH // 3, HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    running = False
                else:
                    reset_game()

    ghost_move_counter += 1
    if ghost_move_counter % ghost_move_interval == 0:
        for ghost in ghosts:
            ghost.update(player_pos, ghost_vulnerable)

    if ghost_vulnerable:
        vulnerable_timer -= 1
        if vulnerable_timer <= 0:
            ghost_vulnerable = False

    fruit_timer += 1
    if fruit_timer > 100 and not fruit:
        fruit = spawn_fruit()
        fruit_timer = 0

    if not pellets and not power_pellets:
        font = pygame.font.SysFont("Arial", 48)
        lvl_text = font.render("¡Nivel Completado!", True, WHITE)
        screen.fill(BLACK)
        screen.blit(lvl_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        init_pellets()
        reset_game()

pygame.quit()
sys.exit()
