import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 500

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 100

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time

        self.laser_timer()
        key_pressed = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.rect.centery -= 1000 * delta_time
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, meteor_sprites, True):
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(100, WINDOW_WIDTH - 100), -200))
        self.born = pygame.time.get_ticks()
        self.span = 2000
        self.direction = pygame.math.Vector2()
        self.direction.x = random.randint(-50, 50)
        self.direction.y = random.randint(100, 200)
        self.direction = self.direction.normalize()
        self.speed = 500
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        current_time = pygame.time.get_ticks()
        if current_time - self.born >= self.span:
            self.kill()

def display_score():
    current_time = pygame.time.get_ticks()
    text_surf = font.render(str(current_time // 100), True, 'white')
    text_rect = text_surf.get_frect(midtop=(WINDOW_WIDTH / 2, 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(30, 15).move(0, -8), 10, 5)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# imports
star_surf = pygame.image.load('images/star.png').convert_alpha()
meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()
laser_surf = pygame.image.load('images/laser.png').convert_alpha()
font = pygame.font.Font('images/Oxanium-Bold.ttf', 50)


# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for _ in range(20):
    Star(star_surf, all_sprites)
player = Player(all_sprites)

# custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 100)

while running:
    # delta time
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (all_sprites, meteor_sprites))

    # update
    all_sprites.update(dt)

    # draw the game
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)
    display_score()

    # draw test


    pygame.display.update()

pygame.quit()