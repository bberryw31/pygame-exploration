from settings import *

# player
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../images/player/down/0.png").convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))


# initiate
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vampire Survivor")
clock = pygame.time.Clock()
running = True

# imports


# groups
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

while running:
    # dt
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('gray')
    all_sprites.draw(display_surface)
    display_surface.blit(player.image, player.rect)

pygame.quit()