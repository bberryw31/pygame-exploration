import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self):
        keys = pygame.key.get_pressed()
        key_pressed = pygame.key.get_just_pressed()
        if key_pressed[pygame.K_SPACE]:
            print('fire missile')
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

# sprite group
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

# importing an image
# player_surf = pygame.image.load('images/player.png').convert_alpha()
# player_rect = player_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
# player_direction = pygame.math.Vector2()
# player_speed = 300

star_surf = pygame.image.load('images/star.png').convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load('images/laser.png').convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

while running:
    # delta time
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     print(event.key)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    # better input
    # print(pygame.mouse.get_pos())
    # print(pygame.mouse.get_pressed())

    # draw the game
    # fill the window with color
    display_surface.fill('darkgray')

    # stars
    for star_pos in star_positions:
        display_surface.blit(star_surf, star_pos)

    # player
    # if player_rect.right >= WINDOW_WIDTH:
    #     player_rect.right = WINDOW_WIDTH
    #     player_direction.x *= -1
    # elif player_rect.left <= 0:
    #     player_rect.left = 0
    #     player_direction.x *= -1
    # elif player_rect.bottom >= WINDOW_HEIGHT:
    #     player_rect.bottom = WINDOW_HEIGHT
    #     player_direction.y *= -1
    # elif player_rect.top <= 0:
    #     player_rect.top = 0
    #     player_direction.y *= -1
    # player_rect.center += player_direction * player_speed * dt

    all_sprites.update()

    # display
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)

    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()