import pygame
import random
import math
from pygame import mixer

pygame.init()
# Screen
screen = pygame.display.set_mode((800, 600))
# Title and Icon
pygame.display.set_caption("Space Mission")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# background
background = pygame.image.load("Background.png").convert()
# background music
mixer.music.load("Dermot Kennedy - Outnumbered.mp3")
mixer.music.play(-1)
# player
PlayerImg = pygame.image.load("ufo.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
no_of_enemy = 6

for i in range(no_of_enemy):
    EnemyImg.append(pygame.image.load("alien.png"))
    EnemyX.append(random.randint(0, 800))
    EnemyY.append(random.randint(50, 100))
    EnemyX_change.append(0.6)
    EnemyY_change.append(50)

# Bullet
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletY_change = 2
Bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font("Brightly Crush Shine.ttf", 32)

textX = 10
textY = 10

# game khatam text
over_text = pygame.font.Font("Brightly Crush Shine.ttf", 72)


def game_over(x, y):
    over = over_text.render("GAME OVER ", True, (255, 255, 0))
    screen.blit(over, (x, y))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (250, 110, 50))
    screen.blit(score, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def bullet_fire(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 0.8
            if event.key == pygame.K_SPACE:
                if Bullet_state is "ready":
                    # bulletSound = mixer.Sound("laser.wav")
                    # bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    BulletX = PlayerX
                    bullet_fire(BulletX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

    PlayerX += PlayerX_change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # Enemy Movement
    for i in range(no_of_enemy):

        # Game Over
        if EnemyY[i] > 440:
            for j in range(no_of_enemy):
                EnemyY[j] = 2000

            game_over(300, 200)
            break

        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 1
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -1
            EnemyY[i] += EnemyY_change[i]

        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            BulletY = 480
            Bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"

    if Bullet_state is "fire":
        bullet_fire(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
