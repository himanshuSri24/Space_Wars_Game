import sys

import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Hello Spider from the future.
# This is my first project in pygame so expect a ton of comments about everything for documentation and clarity.
# Might be irritating cause too many comments but obvio will be there for first project. Please bear.
WIDTH, HEIGHT = 900, 500
# Setting the width and the height for the game window. Caps cause they're constants. (U know this obvio)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Creating a display window and setting mode using a tuple of width and height.
pygame.display.set_caption("Space Wars")
# Setting the name of the game to be displayed in the title bar
WHITE = (255, 255, 255)  # Creating a constant for RGB of white for easy use
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
# Setting FPS to 60 using python.clock.tick(FPS)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40
SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
BACKGROUND = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
# Loading the image so image.load ... os.path.join joins the folders according to diff OS so compatibility is there
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
# Setting the size of spaceships to what I prefer so u can change it easily later. Using new variables for new ones.
YELLOW_SPACESHIP = pygame.transform.rotate((pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                                                   (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))), 90)
RED_SPACESHIP = pygame.transform.rotate((pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                                                (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))), 270)
VEL = 5  # Setting a velocity for spaceships
BULLET_VEL = 7  # Setting velocity for bullets
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
MAX_BULLETS = 3

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

YELLOW_HIT = pygame.USEREVENT + 1  # Creating 2 events to check if any spaceship was hit or not
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0, 0))
    # This fills the entire window with white color
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()
#   updates the window so we can actually see it updated. Need to update manually in pygame
#   blit is to put an image on screen, pass the variable and a tuple containing x,y co-ordinates.
#   co-ordinates start from top left. So top left is 0,0 and inc. going right and down.


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # If a is pressed yellow should go left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 5 < HEIGHT:
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # If a is pressed yellow should go left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # If a is pressed yellow should go left
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # If a is pressed yellow should go left
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 5 < HEIGHT:  # If a is pressed yellow should go left
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x + bullet.width >= WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x <= 0:
            red_bullets.remove(bullet)


# We are making the main function do major tasks. Other tasks done by respective functions for clean code.
def main():
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(800, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health, yellow_health = 10, 10
    run = True
    clock = pygame.time.Clock()
    # Setting a variable for infinite loop to keep our game open and not close unless we press the close icon.
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # This gets all of the events in the game including but not limited to
            # clicks, hover, typing etc
            if event.type == pygame.QUIT:
                # In case user presses quit button, we set run to false.
                # A pygame.quit() function is called at end of while loop
                # That closes the window if we exit the loop.
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)  # Creating 2 rectangles to rep the spaceships. passing it while drawing
    main()


# Ensuring that the main function is run only when called from this program directly and not when imported elsewhere.
if __name__ == "__main__":
    main()
