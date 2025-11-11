import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('planet.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)

# window title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load('player.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    if i % 2 == 0:
        EnemyImg.append(pygame.image.load('enemyType1.png'))
    else:
        EnemyImg.append(pygame.image.load('enemyType2.png'))

    EnemyX.append(random.randint(0, 780))
    EnemyY.append(random.randint(40, 150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)

# Bullet
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480 # PlayerY = 480
BulletY_change = 10 # speed of the bullet
Bullet_state = "ready" # stationary

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 27)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over = False  # game over flag

small_font = pygame.font.Font('freesansbold.ttf', 30)


def game_over_text(x, y):
    over_text = over_font.render(" GAME OVER ", True, (255, 120, 190))
    screen.blit(over_text, (x, y))
    final_score(10, 10)

def restart_text(x, y):
    restart_msg = small_font.render("Press ENTER to play again", True, (255, 255, 255))
    screen.blit(restart_msg, (x, y))

def show_score(x, y):
    score = font.render(f" Score : {str(score_value)}", True, (255, 150, 150))
    screen.blit(score, (x, y))

def final_score(x,y):
    credit_msg = ""
    if score_value >= 10:
        credit_msg = "Impressive! "
    elif score_value >= 5:
        credit_msg = "Good Play! "
    final_score_msg = small_font.render(f"{credit_msg} Final Score : {str(score_value)}", True, (255, 255, 0))
    screen.blit(final_score_msg, (x, y))

def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX, 2) + math.pow(EnemyY - BulletY, 2))
    return distance < 27 # If distance btw enemy and bullet < 27, it's a hit.


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))

# firing bullets
def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))

# play again, reset values
def reset_game():
    global PlayerX, PlayerY, PlayerX_change, BulletY, Bullet_state, score_value, EnemyX, EnemyY, game_over
    PlayerX = 370
    PlayerY = 480
    PlayerX_change = 0
    BulletY = 480
    Bullet_state = "ready"
    score_value = 0
    game_over = False
    for i in range(no_of_enemies):
        EnemyX[i] = random.randint(0, 780)
        EnemyY[i] = random.randint(40, 150)
    mixer.music.play(-1)

# Game Loop
running = True
while running:
    screen.fill((50, 0, 50))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            # Movement
            # keystrokes left or right controls
            if event.type == pygame.KEYDOWN:  # enable key
                if event.key == pygame.K_LEFT:
                    PlayerX_change = -1.5
                if event.key == pygame.K_RIGHT:
                    PlayerX_change = 1.5
                if event.key == pygame.K_SPACE and Bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)

            if event.type == pygame.KEYUP: # stationary
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerX_change = 0

        else:
            # restart game on ENTER key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:
        # Player movement
        PlayerX += PlayerX_change
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 736:
            PlayerX = 736 # 800 - 64 = 736

        # Bullet movement
        if Bullet_state == "fire":
            fire_bullet(BulletX, BulletY)
            BulletY -= BulletY_change

        if BulletY <= 0:
            BulletY = 480 # back to original position
            Bullet_state = "ready"  # next new bullet to shoot

        # Enemy movement
        for i in range(no_of_enemies):
            if EnemyY[i] > 450:
                game_over = True
                mixer.music.stop()
                break

            EnemyX[i] += EnemyX_change[i]
            if EnemyX[i] <= 0:
                EnemyX_change[i] = 2
                EnemyY[i] += EnemyY_change[i]
            elif EnemyX[i] >= 736:
                EnemyX_change[i] = -2
                EnemyY[i] += EnemyY_change[i]

            # Collision check
            collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
            if collision:
                explode_sound = mixer.Sound('explosion.wav')
                explode_sound.play()
                BulletY = 480
                Bullet_state = "ready"
                score_value += 1 # increase score after hitting enemy
                EnemyX[i] = random.randint(0, 780)
                EnemyY[i] = random.randint(30, 70)

            enemy(EnemyX[i], EnemyY[i], i)

        # Show elements
        show_score(textX, textY)
        player(PlayerX, PlayerY)

    else:
        # Game over screen
        game_over_text(220, 220)
        restart_text(210, 400)

    pygame.display.update()