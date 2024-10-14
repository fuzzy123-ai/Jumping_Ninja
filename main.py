import pygame
import sys
from random import randint

# Pygame initialisieren
pygame.init()


# Fenstergröße festlegen
screen_width = 800
screen_height = 1400
screen = pygame.display.set_mode((screen_width, screen_height))

# Fenster-Titel
pygame.display.set_caption("Pygame Boilerplate")

# Farbe definieren (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (255, 0, 0)

# Spieler Variablen
player_posx = screen_width / 2
player_posy = screen_height - 100
player_x = 50
player_y = 70
player_vel = 200
player_jumpf = 580
moving_right = True
down =  pygame.image.load('player_up.png')
up = pygame.image.load('player_down.png')

# Ground Variablen
ground_x = screen_width
ground_y = 100
ground_posx = 0
ground_posy = screen_height - ground_y

# Umgebungs Variablen
gravity = 1000
y_vel = 0
x_vel = 20
on_ground = False
is_jumping = False

# Bricks-Variablen
bricks = []
rows = 20
brick_number = 5
brick_x = 80
brick_y = 20
initial_brick_posx = 20
initial_brick_posy = screen_height - ground_y

# Schüsse
shots = []
delay = 150  # Zeit zwischen den Schüssen in Millisekunden
last_shot_time = 0
size = 35
shot_posx = player_posx + (size // 2) - (size // 2)
shot_sprite = pygame.image.load('shot.png')
shot_sprite = pygame.transform.scale(shot_sprite, (size, size))

def drawplayer():
    global player, player_sprite, y_vel
    if y_vel > 0:
        player_sprite = up
    if y_vel <=0:
        player_sprite = down
    player_sprite = pygame.transform.scale(player_sprite, (player_x, player_y))
    player = pygame.draw.rect(screen, WHITE,pygame.Rect(player_posx, player_posy, player_x, player_y) )
def drawground():
    global ground
    ground = pygame.draw.rect(screen, BLACK, pygame.Rect(ground_posx, ground_posy, ground_x, ground_y))
def initialize_bricks():
    global bricks
    bricks = []
    for row in range(rows):
        # Zufällige X-Position für die gesamte Reihe
        brick_posx = initial_brick_posx + randint(-150, 150)  
        brick_posy = initial_brick_posy - row * (brick_y + 100)  # Y-Position für die aktuelle Reihe
        num_bricks = randint (3, brick_number)
        for _ in range(num_bricks):
            brick_rect = pygame.Rect(brick_posx, brick_posy, brick_x, brick_y)
            bricks.append(brick_rect)
            brick_posx += 300  # Abstand zwischen den Bricks in der gleichen Reihe
def draw_brick():
    for brick in bricks:
        pygame.draw.rect(screen, BLACK, brick)

def jump():
    global y_vel, is_jumping, player_posy, on_ground, is_jumping

    if on_ground: #and keys_pressed[pygame.K_SPACE]:
        y_vel = -player_jumpf
        #player_posy -= y_vel
        on_ground = False
        is_jumping = True
        print("Jump!")
def move():
    global player_posx, player_sprite, moving_right

    if keys_pressed[pygame.K_a] and player_posx > 20:
        player_posx -= x_vel
        moving_right = False
    elif keys_pressed[pygame.K_d] and player_posx < screen_width - player_x - 20:
        player_posx += x_vel
        moving_right = True
    else:
        ...
    if not moving_right:
        player_sprite = pygame.transform.flip(player_sprite, True, False)

def shoot(current_time):
    global last_shot_time
    if keys_pressed[pygame.K_SPACE] and current_time - last_shot_time >= delay:
        shot = {
            'rect': pygame.Rect(player_posx + (player_x // 2) - (size // 2), player_posy, size, size),  # Schuss mittig zum Spieler
            'speed': 5,
            'angle': 0,  # Initialer Winkel für die Drehung
        } 
        shots.append(shot)
        last_shot_time = current_time
def move_shots():
    for shot in shots[:]:  # Kopie der Liste für sicheres Entfernen
        # if y_vel > 0: #runter
        #     shot['rect'].y += shot['speed']
        # if y_vel <=0: #hoch
        #     shot['rect'].y -= shot['speed']  # Bewege den Schuss nach oben 
        shot['rect'].y -= shot['speed'] 
        shot['angle'] += 5  # Erhöhe den Winkel für die Drehung
        # Entferne den Schuss, wenn er den oberen Rand des Bildschirms verlässt
        if shot['rect'].y < 0:
            shots.remove(shot)
def draw_shots():
    for shot in shots:
        rotated_shot_sprite = pygame.transform.rotate(shot_sprite, shot['angle'])  # Drehe das Bild
        # Berechne die neue Position, um den Mittelpunkt des Schusses zu zentrieren
        new_rect = rotated_shot_sprite.get_rect(center=(shot['rect'].x + size // 2, shot['rect'].y + size // 2))
        screen.blit(rotated_shot_sprite, new_rect.topleft)  # Blit das gedrehte Bild an die aktuelle Position
    for shot in shots:
        screen.blit(shot_sprite, (shot['rect'].x, shot['rect'].y))  # Blit das Schussbild an die aktuelle Position


def collide_brick():
    global on_ground, player_posy, y_vel, is_jumping, player_posx
    on_ground = False
    player_rect = pygame.Rect(player_posx, player_posy, player_x, player_y)

    for brick in bricks:
        if player_rect.colliderect(brick):
            # Kollision von oben
            if y_vel >= 0 and player_rect.bottom <= brick.top + y_vel:
                on_ground = True
                player_posy = brick.top - player_y  # Setze den Spieler auf die Plattform
                y_vel = 0
                break
            
            # Kollision von unten
            elif y_vel < 0 and player_rect.top <= brick.bottom and player_rect.bottom >= brick.top:
                player_posy = brick.bottom  # Spieler bleibt oben auf der Plattform
                y_vel = 0

            # Kollision von der Seite
            if player_rect.right > brick.left and player_rect.left < brick.right:
                if player_rect.right > brick.left and player_rect.left < brick.left:  # Von links
                    player_posx = brick.left - player_x  # Spieler wird links vom Brick positioniert
                elif player_rect.left < brick.right and player_rect.right > brick.right:  # Von rechts
                    player_posx = brick.right  # Spieler wird rechts vom Brick positioniert

            # Optional: Sicherstellen, dass der Spieler nicht weiter nach unten gedrückt wird
            # Wir setzen die Y-Position, falls die Kollision von unten kommt
            if player_rect.bottom >= brick.top and player_rect.top < brick.top and y_vel >= 0:
                player_posy = brick.top - player_y
                y_vel = 0
                on_ground = True
def collide_ground():
    global is_jumping, on_ground, y_vel, player_posy
    player_rect = pygame.Rect(player_posx, player_posy, player_x, player_y)

    if player_rect.colliderect(ground) and y_vel > 0:
        is_jumping = False
        on_ground = True
        player_posy = ground.top - player_y 
        y_vel = 0
def collide_shots():
    global shots
    for shot in shots[:]:  # Kopie der Liste für sicheres Entfernen
        for brick in bricks:
            if shot['rect'].colliderect(brick):
                shots.remove(shot)  # Schuss entfernen
                break  # Bei Kollision mit einer Plattform abbrechen
    ...           



clock = pygame.time.Clock()
fps = 60
# Hauptschleife
initialize_bricks()
running = True
while running:
    global star
    current_time = pygame.time.get_ticks()
    keys_pressed = pygame.key.get_pressed()
    # Ereignisschleife
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys_pressed[pygame.K_ESCAPE]:
        running = False
    dt = clock.tick(fps) / 1000.0



    # Bildschirm füllen
    screen.fill(WHITE)
    drawplayer()
    drawground()

    draw_brick()
    # Spieler Bewegung
    jump()
    move()
    shoot(current_time)
    move_shots()
    draw_shots()
    # Kollision
    collide_brick()
    collide_ground()
    collide_shots()

    screen.blit(player_sprite, (player_posx, player_posy))

    # Gravitation anwenden
    if not on_ground:
        y_vel += gravity * dt
        player_posy += y_vel * dt

    # Display aktualisieren
    pygame.display.flip() 
    clock.tick(60)

    # print(y_vel)
# Pygame beenden
pygame.quit()
sys.exit()
