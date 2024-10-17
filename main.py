import pygame
import sys
import time
from random import randint
from random import choice


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
YELLOW = (255, 215, 0)

# Spieler Variablen
player_posx = screen_width / 2

player_posy = screen_height - 100
player_startposx = screen_width / 2
player_startposy = screen_height - 100
player_x = 50
player_y = 70
player_vel = 20000
player_jumpf = 56000
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
x_vel = 1000
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

# Punkte
stars = []
points = 0
star_image = pygame.image.load('star.png')
star_image = pygame.transform.scale(star_image, (size, size))

# Stones
falling_stones = []

def reset():
    global player_posx, player_posy
    player_posx = player_startposx
    player_posy = player_startposy
    new_star = place_star_on_top_platform()
    initialize_bricks()
    draw_brick()    
    falling_stones.clear()  
    stars.clear()
    stars.append(new_star)
def blink_color(color):
    # Fülle den Bildschirm mit der angegebenen Farbe
    screen.fill(color)
    pygame.display.flip()  # Aktualisiere das Display, um die Farbe anzuzeigen
    time.sleep(0.2)  # Lass den Bildschirm für 0,1 Sekunden in dieser Farbe stehen
    # Danach wird der normale Bildschirm wieder gezeichnet (hier weiß als Beispiel)
    screen.fill(WHITE)  # Oder deine Szene/Standardfarbe
    pygame.display.flip()  # Aktualisiere das Display erneut
# Draw all the stuff
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
    brick_posy = screen_height - ground_y  # Beginne am unteren Bildschirmrand

    for row in range(rows):
        if brick_posy < 0:  # Abbruchbedingung: Stoppe, wenn die y-Position negativ ist (über den oberen Rand hinaus)
            break

        # Zufällige horizontale Position und Abstand zwischen den Plattformen
        brick_posx = initial_brick_posx + randint(-150, 150)  
        num_bricks = randint(2, brick_number)  # Anzahl der Bricks pro Reihe
        row_spacing = randint(100, 150)  # Zufälliger Abstand zwischen den Reihen

        for _ in range(num_bricks):
            # Setze die Bricks nicht zu dicht aneinander
            brick_rect = pygame.Rect(brick_posx, brick_posy, brick_x, brick_y)
            bricks.append(brick_rect)
            brick_posx += randint(300, 400)  # Zufälliger Abstand zwischen den Bricks in der gleichen Reihe
        
        brick_posy -= (brick_y + row_spacing)  # Zufälliger Abstand zur nächsten Reihe
def draw_brick():
    for brick in bricks:
        pygame.draw.rect(screen, BLACK, brick)

# Player
def jump(dt):
    global y_vel, is_jumping, player_posy, on_ground, is_jumping

    if on_ground: #and keys_pressed[pygame.K_SPACE]:
        y_vel = -player_jumpf * dt
        #player_posy -= y_vel
        on_ground = False
        is_jumping = True
        print("Jump!")
def move(dt):
    global player_posx, player_sprite, moving_right
    border = 10
    if keys_pressed[pygame.K_a] and player_posx > border:
        player_posx -= x_vel * dt
        moving_right = False
    elif keys_pressed[pygame.K_d] and player_posx < screen_width - player_x - border:
        player_posx += x_vel * dt
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
def move_shots(dt):
    for shot in shots[:]:  # Kopie der Liste für sicheres Entfernen
        # if y_vel > 0: #runter
        #     shot['rect'].y += shot['speed']
        # if y_vel <=0: #hoch
        #     shot['rect'].y -= shot['speed']  # Bewege den Schuss nach oben 
        shot['rect'].y -= shot['speed'] 
        shot['angle'] += 500 * dt  # Erhöhe den Winkel für die Drehung
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

# Point counter
def initialize_points(num_stars):
    global stars
    stars = []  # Leere Liste, um Sterne hinzuzufügen
    for _ in range(num_stars):
        star_rect = place_star_on_top_platform()  # Setze den Stern auf eine Plattform
        stars.append(star_rect)
def draw_points():
    # Sterne zeichnen
    for star in stars:  # Zeichne alle Sterne aus der Liste
        pygame.draw.rect(screen, (255, 215, 0), star)  # Goldene Farbe für die Sterne
        screen.blit(star_image, (star.x, star.y))
        print(star.x,",", star.y)
def count_points():
    global points
    player_rect = pygame.Rect(player_posx, player_posy, player_x, player_y)
    for star in stars[:]:  # Kopie der Liste für sicheres Entfernen
        if player_rect.colliderect(star):  # Kollision überprüfen
            stars.remove(star)  # Stern entfernen
            points += 1  # Punkte erhöhen
            print(f"Points: {points}")
            # Setze einen neuen Stern auf eine der letzten (höchsten) Plattformen
            blink_color(YELLOW)
            reset()

def place_star_on_top_platform():
    if len(bricks) > 0:
        top_platforms = bricks[-5:]  # Die letzten 5 Plattformen (höchste)
        selected_platform = choice(top_platforms)

        # Setze den Stern auf die ausgewählte Plattform
        star_rect = pygame.Rect(
            selected_platform.x + selected_platform.width // 2 - size // 2,  # Mitte der Plattform
            selected_platform.y - size,  # Oberhalb der Plattform
            size, size  # Größe des Sterns
        )

        # Überprüfe, ob der Stern außerhalb des Bildschirms ist und korrigiere die Position
        if star_rect.x < 0:
            star_rect.x = 0  # Setze den Stern an den linken Rand
        elif star_rect.right > screen_width:
            star_rect.x = screen_width - size  # Setze den Stern an den rechten Rand

        if star_rect.y < 0:
            star_rect.y = 0  # Setze den Stern an den oberen Rand

        return star_rect

    # Stern auf eine der obersten Plattformen setzen
    # Wähle zufällig eine der obersten Plattformen aus
    if len(bricks) > 0:
        top_platforms = bricks[-5:]  # Nehme die ersten 5 Plattformen als "oberste"
        selected_platform = choice(top_platforms)  # Wähle eine Plattform aus

        # Setze den Stern auf die ausgewählte Plattform
        star_rect = pygame.Rect(
            selected_platform.x + selected_platform.width // 2 - size // 2,  # Mitte der Plattform
            selected_platform.y - size,  # Oberhalb der Plattform
            size, size  # Größe des Sterns
        )
        return star_rect



# Collision
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

# Falling Stones
def initialize_stone():
    stone_posx = player_posx + randint(-50, 50)  # Zufällige X-Position für den Stein
    stone_rect = pygame.Rect(stone_posx, 0, 50, 50)  # Steingröße (50x50) und Startposition oben
    falling_stones.append(stone_rect)
def move_stones(dt):
    # Steine bewegen
    for stone in falling_stones[:]:  # Kopie der Liste
        stone.y += 500 * dt # Geschwindigkeit des fallenden Steins
        if stone.y > screen_height:  # Stein aus dem Bildschirm entfernen, wenn er unten ist
            falling_stones.remove(stone)
def draw_stones():
    # Steine zeichnen
    for stone in falling_stones:
        pygame.draw.rect(screen, (255, 0, 0), stone)  # Zeichne den Stein in Rot
def collide_with_stone():
# Kollision mit Steinen prüfen
    global running, player_posx, player_posy, player_startposx, player_startposy
    player_rect = pygame.Rect(player_posx, player_posy, player_x, player_y)
    for stone in falling_stones:
        if player_rect.colliderect(stone):  # Spieler wird von Stein getroffen
            print("Player hit by stone!")
            blink_color(RED)
            reset()


clock = pygame.time.Clock()
fps = 60
stone_spawn_time = 0  # Zeit zum Erzeugen neuer Steine
initialize_bricks()

initialize_points(1)
# Hauptschleife
running = True
while running:
    current_time = pygame.time.get_ticks()
    keys_pressed = pygame.key.get_pressed()
    # Ereignisschleife
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys_pressed[pygame.K_ESCAPE]:
        running = False
    dt = clock.tick(fps) / 1000.0

    if current_time - stone_spawn_time > 2000:  # 2000 Millisekunden = 2 Sekunden
        initialize_stone()
        stone_spawn_time = current_time


    # Bildschirm füllen
    screen.fill(WHITE)
    drawplayer()
    drawground()

    draw_brick()
    # Spieler Bewegung
    jump(dt)
    move(dt)
    
    #Schüsse
    shoot(current_time)
    move_shots(dt)
    draw_shots()

    #Punktezähler
    draw_points()
    count_points()

    # Kollision
    collide_brick()
    collide_ground()
    collide_shots()

      # Steine bewegen, zeichnen und auf Kollision prüfen
    move_stones(dt)
    draw_stones()
    collide_with_stone()  # Spieler trifft auf Stein?

    screen.blit(player_sprite, (player_posx, player_posy))

    # Gravitation anwenden
    if not on_ground:
        y_vel += gravity * dt
        player_posy += y_vel * dt

    # Display aktualisierena
    pygame.display.flip() 
    clock.tick(60)

    # print(y_vel)
# Pygame beenden
pygame.quit()
sys.exit()
