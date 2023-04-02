import pygame
from groups import all_sprites_group
from player import Player, PLAYER_1_SPRITE
from bullet import BULLET_1_SPRITE
from cameragroup import CameraGroup, COVER_SPRITE
from sys import exit
import settings


pygame.init()

# Checking of pause
pause = False

# Set clock rate for game
clock = pygame.time.Clock()

# Set screen
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

# Set name of window
pygame.display.set_caption('Game HM')

# Load images
# Have to use convert_alpha() for images with alpha channel
bg_img = pygame.image.load('assets/images/backgrounds/bg_1.png').convert()

# Make a pause text
pause_text = (pygame.font.SysFont('Consolas', 72).render('Pause', True, pygame.color.Color('White')))

# Camera group
camera_group = CameraGroup()

# Create object player
PLAYER_1_SPRITE.convert_alpha()
player = Player(camera_group)

# OLD (SOLUTION CAMERA'S PROBLEM CAN BE HERE)
# Create of group player and  bullet
# all_sprites_group.add(player)

# Convert alpha for images
COVER_SPRITE.convert_alpha()
BULLET_1_SPRITE.convert_alpha()

# Definition of camera (something like this)
display_scroll = [0, 0]


# Main game loop
run = True
while run:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Checking pause button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause

    if not pause:
        # Game is here
        screen.blit(bg_img, (0, 0))
        # screen.blit(player.image, player.rect)
        # player.update()
        all_sprites_group.update()
        camera_group.update()
        camera_group.custom_draw(player)
        all_sprites_group.draw(screen)
    elif pause:
        screen.fill((0, 0, 0))
        screen.blit(pause_text, (300, 300))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
exit()
