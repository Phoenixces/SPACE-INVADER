import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# creating screen of width - 800px and height -600px
screen = pygame.display.set_mode((800, 600))  # This method uses tuples


# Background
# Background download from : https://www.freepik.com/
background = pygame.image.load('Additional Files/background3 (1).png')
# Background music
mixer.music.load('Additional Files/background.wav')
mixer.music.play(-1) # -1 is to play the sound in loop


# Caption and Icon
# Icon download from : https://www.flaticon.com/
pygame.display.set_caption("SPACE INVADERS...:)")
# icon = pygame.image.load('space-ship.png')
# pygame.display.set_icon(icon)


# load button image
start_img = pygame.image.load('Additional Files/start-button.png').convert_alpha()
exit_img = pygame.image.load('Additional Files/exit.png').convert_alpha()
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        # check mouseover buttons
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
# create button instances
start_button = Button(368, 200, start_img)
exit_button = Button(368, 325, exit_img)



# Player
playerImg = pygame.image.load('Additional Files/player.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = random.randint(5, 10)

for i in range(num_of_enemies):
    enemyImg.append(random.choice([pygame.image.load('Additional Files/alien.png'),pygame.image.load('Additional Files/alien2.png'),pygame.image.load('Additional Files/alien3.png')]))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.9)
    enemyY_change.append(40)


# Bullets
bulletImg = pygame.image.load('Additional Files/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"
# ready : ready to be fired
# fire : bullet currently moving


# score
# Font download from : https://www.dafont.com/

font = pygame.font.Font('Additional Files/Astral Sisters.ttf', 40)

textX = 10
textY = 10

over_font = pygame.font.Font('Additional Files/Astral Sisters.ttf', 64)
lost = pygame.font.Font('Additional Files/Astral Sisters.ttf', 32)

# Game over text
def game_over():
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = False
        screen.fill((0,0,0))
        game_over = over_font.render('GAME OVER', True, (205, 255, 205))
        screen.blit(game_over, (230, 250))
        base_lost = lost.render('Enemies  captured  your  base...:( ', True, (200, 205, 105))
        screen.blit(base_lost, (230, 200))
        if exit_button.draw(screen):
            exit()
        pygame.display.update()


def show_score(x, y, score_value):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def black_out():
    over = True
    while over:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if exit_button.draw(screen):
            over = False
            exit()
        pygame.display.update()


def player(x, y):
    screen.blit(playerImg, (x, y))  # let player appear


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # let player appear


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def button(run):
    global bullet_state,bulletX,playerX_change,playerX,bulletY
    while run:
        # RGB - Red , Green , Blue
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if start_button.draw(screen):
            score_value = 0
            running = True
            while running:

                # RGB - Red , Green , Blue
                screen.fill((0, 0, 0))
                # Background Image
                screen.blit(background, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False


                    # If keystroke pressed check whether its right or left
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            playerX_change = -2
                        if event.key == pygame.K_RIGHT:
                            playerX_change = 2
                        if event.key == pygame.K_SPACE:
                            if bullet_state == "ready":
                                bullet_sound = mixer.Sound('Additional Files/Bullet.wav')
                                bullet_sound.play()
                                bulletX = playerX  # Get the current x cordinate of spaceship
                                fire_bullet(bulletX, bulletY)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            playerX_change = 0

                playerX += playerX_change

                # Setting bounds for player
                if playerX <= 0:
                    playerX = 0
                elif playerX >= 736:
                    playerX = 736

                # Enemy Movement
                for i in range(num_of_enemies):

                    # Game over
                    if enemyY[i] > 420:
                        for j in range(num_of_enemies):
                            enemyY[i] = 2000
                        game_over()
                        break



                    enemyX[i] += enemyX_change[i]
                    if enemyX[i] <= 0:
                        enemyX_change[i] = 0.9
                        enemyY[i] += enemyY_change[i]
                    elif enemyX[i] >= 736:
                        enemyX_change[i] = -0.9
                        enemyY[i] += enemyY_change[i]

                    # Collision
                    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                    if collision:
                        explosion_sound = mixer.Sound('Additional Files/explosion.wav')
                        explosion_sound.play()
                        bulletY = 480
                        bullet_state = "ready"
                        score_value += 1
                        print(score_value)
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(0, 150)

                    enemy(enemyX[i], enemyY[i], i)

                # Bullet Movement
                if bulletY <= 0:
                    bulletY = 480
                    bullet_state = "ready"
                if bullet_state == 'fire':
                    fire_bullet(bulletX, bulletY)
                    bulletY -= bulletY_change

                player(playerX, playerY)
                show_score(textX, textY, score_value)
                pygame.display.update()
        if exit_button.draw(screen):
            exit()
        pygame.display.update()

run = True
button(run)




