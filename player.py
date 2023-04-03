import pygame
import math
from groups import *
from bullet import Bullet
from settings import *


PLAYER_1_SPRITE = pygame.image.load('assets/images/sprites/player_1.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        group.add(self)
        self.bullet = None
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.velocity_x = 0
        self.velocity_y = 0
        # Third argument allow change scale of object
        self.image = pygame.transform.rotozoom(PLAYER_1_SPRITE, 0, PLAYER_SIZE)
        self.base_player_image = self.image

        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)

    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - self.hitbox_rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.velocity_y = self.speed
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.velocity_x = self.speed
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity_x = -self.speed

        if self.velocity_x != 0 and self.velocity_y != 0:  # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed()[0]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            # all_sprites_group.add(self.bullet)
            camera_group.add(self.bullet)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
