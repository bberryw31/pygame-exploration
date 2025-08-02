import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 590
SCREEN_HEIGHT = 800
FPS = 60
PIXEL_SCALE = 3

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Road Rampage")
clock = pygame.time.Clock()


def upscale_image(image, scale):
    width = image.get_width() * scale
    height = image.get_height() * scale
    return pygame.transform.scale(image, (width, height))


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)

# Load and upscale images
# Car images
car_straight_raw = pygame.image.load('images/car.png').convert_alpha()
car_left_raw = pygame.image.load('images/car_left.png').convert_alpha()
car_right_raw = pygame.image.load('images/car_right.png').convert_alpha()
# Upscale car images
car_straight = upscale_image(car_straight_raw, PIXEL_SCALE)
car_left = upscale_image(car_left_raw, PIXEL_SCALE)
car_right = upscale_image(car_right_raw, PIXEL_SCALE)

# Road image
road_img_raw = pygame.image.load('images/road.png').convert_alpha()
road_img = upscale_image(road_img_raw, PIXEL_SCALE)
road_width = road_img.get_width()
road_height = road_img.get_height()
# Center road on screen
road_x_offset = (SCREEN_WIDTH - road_width) // 2 if road_width < SCREEN_WIDTH else 0

# Load zombie images
zombie1_frames = {
    'front': [],
    'left': [],
    'right': [],
    'back': []
}

zombie2_frames = {
    'front': [],
    'left': [],
    'right': [],
    'back': []
}

# Load zombie1 (normal zombie)
for i in range(1, 10):
    img = pygame.image.load(f'images/zombie1/{i}.png').convert_alpha()
    img_scaled = upscale_image(img, PIXEL_SCALE)

    if i <= 3:  # Front facing
        zombie1_frames['front'].append(img_scaled)
    elif i <= 6:  # Left facing
        zombie1_frames['left'].append(img_scaled)
        # Create right facing by flipping left
        zombie1_frames['right'].append(pygame.transform.flip(img_scaled, True, False))
    else:  # Back facing
        zombie1_frames['back'].append(img_scaled)

# Load zombie2 (fat zombie)
for i in range(1, 10):
    img = pygame.image.load(f'images/zombie2/{i}.png').convert_alpha()
    img_scaled = upscale_image(img, PIXEL_SCALE)

    if i <= 3:  # Front facing
        zombie2_frames['front'].append(img_scaled)
    elif i <= 6:  # Left facing
        zombie2_frames['left'].append(img_scaled)
        # Create right facing by flipping left
        zombie2_frames['right'].append(pygame.transform.flip(img_scaled, True, False))
    else:  # Back facing
        zombie2_frames['back'].append(img_scaled)

# Game variables
score = 0
game_time = 60
time_left = game_time
game_over = False
road_y = 0
road_speed = 7
difficulty_multiplier = 1.0


class BloodParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 10)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.randint(1, 3) * PIXEL_SCALE // 2
        self.lifetime = random.randint(15, 30)
        self.color = random.choice([RED, DARK_RED])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.5  # Gravity
        self.lifetime -= 1
        self.vx *= 0.96  # Friction

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))


# Player car class
class Car:
    def __init__(self):
        self.image = car_straight
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 100
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = "straight"

        # Calculate road boundaries
        self.left_bound = road_x_offset + 20
        self.right_bound = road_x_offset + road_width - self.width - 20

    def move_left(self):
        if self.x > self.left_bound:
            self.x -= self.speed
            self.rect.x = self.x
            self.direction = "left"
            self.image = car_left

    def move_right(self):
        if self.x < self.right_bound:
            self.x += self.speed
            self.rect.x = self.x
            self.direction = "right"
            self.image = car_right

    def update(self):
        # Reset to straight
        if self.direction != "straight":
            self.direction = "straight"
            self.image = car_straight

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# Zombie class
class Zombie:
    def __init__(self, zombie_type='zombie1', x_offset=0, y_offset=0):
        # Determine zombie type
        self.zombie_type = zombie_type
        if zombie_type == 'zombie1':
            self.frames_dict = zombie1_frames
            self.points = 10
            self.base_speed = random.uniform(2, 5)
        else:  # zombie2 (fat zombie)
            self.frames_dict = zombie2_frames
            self.points = 15  # More points for fat zombies
            self.base_speed = random.uniform(1, 3)  # Slower

        # Animation setup
        self.current_frame = 0
        self.animation_speed = random.uniform(0.1, 0.3)
        self.animation_timer = 0

        # Position and movement
        self.direction = 'front'  # Start facing front
        self.width = self.frames_dict['front'][0].get_width()
        self.height = self.frames_dict['front'][0].get_height()

        left_spawn = road_x_offset + 20
        right_spawn = road_x_offset + road_width - self.width - 20
        self.x = random.randint(left_spawn, right_spawn) + x_offset
        self.y = -self.height - 50 + y_offset

        # Movement direction (for animations)
        self.vx = random.uniform(-1, 1)  # Slight horizontal movement
        self.speed = self.base_speed + road_speed

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.alive = True

    def move(self):
        # Move zombie
        self.y += self.speed
        self.x += self.vx

        # Keep within road boundaries
        left_bound = road_x_offset + 20
        right_bound = road_x_offset + road_width - self.width - 20
        if self.x < left_bound or self.x > right_bound:
            self.vx = -self.vx
            self.x = max(left_bound, min(self.x, right_bound))

        self.rect.x = self.x
        self.rect.y = self.y

        # Update direction based on movement
        if abs(self.vx) < 0.3:
            if self.speed > road_speed:
                self.direction = 'front'
            else:
                self.direction = 'back'
        elif self.vx < -0.3:
            self.direction = 'left'
        else:
            self.direction = 'right'

        # Animate
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 3

    def draw(self, surface):
        if self.alive:
            current_frames = self.frames_dict[self.direction]
            surface.blit(current_frames[self.current_frame], (self.x, self.y))


# Zombie spawn patterns
def spawn_single_zombie():
    # 70% chance for normal zombie, 30% for fat zombie
    zombie_type = 'zombie1' if random.random() < 0.7 else 'zombie2'
    return [Zombie(zombie_type=zombie_type)]


def spawn_horizontal_line(count=3):
    zombies = []
    spacing = (road_width - 40) // (count + 1)
    # Mixed zombie types
    for i in range(count):
        x_offset = (i - count // 2) * spacing
        zombie_type = 'zombie1' if random.random() < 0.8 else 'zombie2'
        zombies.append(Zombie(zombie_type=zombie_type, x_offset=x_offset))
    return zombies


def spawn_v_formation():
    zombies = []
    # Create V shape with mostly normal zombies
    for i in range(5):
        x_offset = (i - 2) * 40
        y_offset = abs(i - 2) * 30
        zombie_type = 'zombie1' if i != 2 else 'zombie2'  # Fat zombie in center
        zombies.append(Zombie(zombie_type=zombie_type, x_offset=x_offset, y_offset=y_offset))
    return zombies


def spawn_cluster():
    zombies = []
    # Random cluster of zombies
    count = random.randint(4, 7)
    has_fat_zombie = False
    for _ in range(count):
        x_offset = random.randint(-60, 60)
        y_offset = random.randint(-40, 40)
        # Ensure at least one fat zombie in cluster
        if not has_fat_zombie and _ == count - 1:
            zombie_type = 'zombie2'
        else:
            zombie_type = 'zombie1' if random.random() < 0.7 else 'zombie2'
            if zombie_type == 'zombie2':
                has_fat_zombie = True
        zombies.append(Zombie(zombie_type=zombie_type, x_offset=x_offset, y_offset=y_offset))
    return zombies


# Spawn pattern list
spawn_patterns = [
    spawn_single_zombie,
    spawn_horizontal_line,
    spawn_v_formation,
    spawn_cluster
]

# Create game objects
player_car = Car()
zombies = []
blood_particles = []

# Fonts - Load Silkscreen font
font_large = pygame.font.Font('Silkscreen/slkscr.ttf', 48)
font_medium = pygame.font.Font('Silkscreen/slkscr.ttf', 24)
font_small = pygame.font.Font('Silkscreen/slkscr.ttf', 16)

# Game loop
running = True
spawn_timer = 0
spawn_delay = 40
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event and not game_over:
            time_left -= 1
            if time_left <= 0:
                game_over = True
            # Increase difficulty
            if time_left % 10 == 0 and spawn_delay > 15:
                spawn_delay -= 5
                difficulty_multiplier += 0.2

    # Get keyboard input
    keys = pygame.key.get_pressed()

    if not game_over:
        # Update player car
        player_car.update()

        # Move player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_car.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_car.move_right()

        # Spawn zombies
        spawn_timer += 1
        if spawn_timer > spawn_delay:
            pattern = random.choice(spawn_patterns)
            new_zombies = pattern()
            zombies.extend(new_zombies)
            spawn_timer = 0

        # Move zombies and check collisions
        for zombie in zombies[:]:
            zombie.move()

            # Check collision with player
            if zombie.alive and player_car.rect.colliderect(zombie.rect):
                zombie.alive = False
                score += int(zombie.points * difficulty_multiplier)

                # Create blood explosion
                collision_x = zombie.x + zombie.width // 2
                collision_y = zombie.y + zombie.height // 2
                # More particles for fat zombies
                particle_count = 35 if zombie.zombie_type == 'zombie2' else 25
                for _ in range(particle_count):
                    blood_particles.append(BloodParticle(collision_x, collision_y))

            # Remove off-screen zombies
            if zombie.y > SCREEN_HEIGHT:
                zombies.remove(zombie)

        # Update blood particles
        for particle in blood_particles[:]:
            particle.update()
            if particle.lifetime <= 0 or particle.y > SCREEN_HEIGHT:
                blood_particles.remove(particle)

    # Scroll road
    road_y += road_speed
    if road_y >= road_height:
        road_y = 0

    # Draw everything
    screen.fill(BLACK)

    # Draw scrolling road
    screen.blit(road_img, (road_x_offset, road_y))
    screen.blit(road_img, (road_x_offset, road_y - road_height))

    # Draw zombies
    for zombie in zombies:
        zombie.draw(screen)

    # Draw blood particles
    for particle in blood_particles:
        particle.draw(screen)

    # Draw player car
    player_car.draw(screen)

    # Draw UI - Simple white on black
    # Score
    score_text = font_medium.render(f"SCORE: {score}", True, WHITE)
    score_bg = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10))
    score_bg.fill(BLACK)
    screen.blit(score_bg, (10, 10))
    screen.blit(score_text, (20, 15))

    # Timer
    time_text = font_medium.render(f"TIME: {time_left}", True, WHITE)
    time_bg = pygame.Surface((time_text.get_width() + 20, time_text.get_height() + 10))
    time_bg.fill(BLACK)
    screen.blit(time_bg, (SCREEN_WIDTH - time_bg.get_width() - 10, 10))
    screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 15))

    # Game over screen
    if game_over:
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Game over box
        box_width = 400
        box_height = 250
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2

        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 3)

        # Game over text
        game_over_text = font_large.render("GAME OVER!", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(game_over_text, text_rect)

        final_score_text = font_medium.render(f"FINAL SCORE: {score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(final_score_text, score_rect)

        restart_text = font_small.render("PRESS SPACE TO RESTART", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)

        quit_text = font_small.render("PRESS ESC TO QUIT", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(quit_text, quit_rect)

        if keys[pygame.K_SPACE]:
            # Reset game
            score = 0
            time_left = game_time
            game_over = False
            zombies.clear()
            blood_particles.clear()
            spawn_timer = 0
            spawn_delay = 40
            difficulty_multiplier = 1.0

        if keys[pygame.K_ESCAPE]:
            running = False

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit game
pygame.quit()