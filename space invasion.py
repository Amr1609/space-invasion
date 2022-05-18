import pygame
from pygame import mixer
import math
import random
# intialize pygame

pygame.init()

# creat screen window

width, height = 800, 600

screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load("background.jpg")

# Background sounds
mixer.music.load("Clip-Birth-Day-Muslim-_-كليب-عيد-ميلاد-_هنقلبهالك-عيد-ميلاد_-مسلم-_192-kbps_.wav")
mixer.music.play(-1)

# Title and icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#score

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 37)

score_textX = 10
score_textY = 10

def show_score (scorex, scorey):
    score = font.render("score : " + str(score_val), True,(250, 250, 250))
    screen.blit(score, (scorex, scorey))

#Health

Health_val = 1
font = pygame.font.Font('freesansbold.ttf', 37)

Health_textX = 650
Health_textY = 10

def show_Health (Healthx, Healthy):
    Health = font.render("Health : " + str(Health_val), True,(25, 250, 50))
    screen.blit(Health, (Healthx, Healthy))

 #Lavel

Lavel_val = score_val % 10 + 1
font = pygame.font.Font('freesansbold.ttf', 30)

Lavel_textX = 10
Lavel_textY = 40
def show_Lavel (Lavelx, Lavely):
    Lavel = font.render("lavel : " + str(int(Lavel_val)), True,(50, 125, 250))
    screen.blit(Lavel, (Lavelx, Lavely))

# player

player = pygame.image.load("astronomy.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy =  10
for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY .append(random.randint(50, 150))
    enemyX_change .append(0.2)
    enemyY_change .append(40)

# bullet

# ready: bullet is under the space ship
# fire : bullet is realsed

bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

def Player(x, y):
    screen.blit(player, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def isCollision (enemyX , enemyY , bulletX , bulletY):
    distance =  math.sqrt((math.pow(enemyX - bulletX , 2)) +(math.pow(enemyY - bulletY , 2)))
    if distance < 27:
        return True
    else:
        return False
def isCollision_of_plyer (enemyX , enemyY , plyerX , plyerY):
    distance =  math.sqrt((math.pow(enemyX - plyerX , 2)) +(math.pow(enemyY - plyerY , 2)))
    if distance < 27:
        return True
    else:
        return False



# Game Loop

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or Health_val == 0:
            running = False

        # if keystrok is pressed check weather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key ==pygame.K_a :
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT or event.key ==pygame.K_d :
                playerX_change = 0.5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_change = 0.5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound =  mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet_fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_d or event.key == pygame.K_a:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w \
                    or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_change = 0

    # space ship boundry
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    playerY += playerY_change
    if playerY < 250:
        playerY = 250
    elif playerY > 520:
        playerY = 520

    # enemy movement
    for i in range(num_of_enemy):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val +=1
            Lavel_val = score_val / 10 + 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)

        # collision_of_plyer
        collision_of_plyer = isCollision_of_plyer(enemyX[i], enemyY[i], playerX, playerY)
        if collision_of_plyer:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            Health_val -= 1

    # bullet movement
    if bulletY < 0:
        bulletY = playerY
        bullet_state = "ready"


    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change


    Player(playerX, playerY)
    show_score(score_textX, score_textY)
    show_Health(Health_textX, Health_textY)
    show_Lavel(Lavel_textX, Lavel_textY)
    pygame.display.update()
