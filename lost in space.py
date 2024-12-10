import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lost in Space")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Game Variables
clock = pygame.time.Clock()
FPS = 60

# Assets
font = pygame.font.Font(None, 36)
spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
asteroid_img = pygame.image.load("asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
laser_img = pygame.image.load("laser.png")
laser_img = pygame.transform.scale(laser_img, (10, 40))

# Game State
levels = [{"unlocked": i == 0, "stars": 0} for i in range(11)]  # 10 levels + 1 boss
current_level = 0

# Functions
def draw_text(text, x, y, color=WHITE, size=36, center=False):
    font = pygame.font.Font(None, size)
    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect.topleft)
    else:
        screen.blit(label, (x, y))

def main_menu():
    start_bg = pygame.image.load("start_bg.png")
    start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        # Draw the background
        screen.blit(start_bg, (0, 0))

        # Menu options
        draw_text("LOST IN SPACE", SCREEN_WIDTH // 2, 100, YELLOW, 72, center=True)
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 200, 200, 50))
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 300, 200, 50))
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 400, 200, 50))

        draw_text("Play", SCREEN_WIDTH // 2, 225, WHITE, 36, center=True)
        draw_text("High Scores", SCREEN_WIDTH // 2, 325, WHITE, 36, center=True)
        draw_text("Quit", SCREEN_WIDTH // 2, 425, WHITE, 36, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if SCREEN_WIDTH // 2 - 100 <= mx <= SCREEN_WIDTH // 2 + 100:
                    if 200 <= my <= 250:
                        level_menu()
                    elif 300 <= my <= 350:
                        pass  # High Scores (to be implemented)
                    elif 400 <= my <= 450:
                        pygame.quit()
                        sys.exit()
def level_menu():
    global current_level
    scroll_offset = 0  # Tracks vertical scrolling
    scroll_speed = 0  # Current scrolling speed (smooth scrolling effect)
    path_nodes = []  # List to hold level node positions
    max_scroll = 0  # Maximum scrollable height

    # Load the level menu background
    level_bg = pygame.image.load("level_bg.png")
    level_bg = pygame.transform.scale(level_bg, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))  # Make it taller for scrolling

    # Load planet images for levels
    planet_images = [pygame.image.load(f"planet_{i + 1}.png") for i in range(len(levels))]
    planet_images = [pygame.transform.scale(img, (80, 80)) for img in planet_images]

    # Precompute node positions for the path
    for i in range(len(levels)):
        x = 100 + (i % 2) * 300  # Alternates between left and right
        y = 150 + i * 150  # Staggered vertically
        path_nodes.append((x, y))

    # Set maximum scroll height
    max_scroll = max(0, path_nodes[-1][1] - SCREEN_HEIGHT + 200)

    while True:
        screen.fill(BLACK)

        # Handle scrolling input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            scroll_speed = -10
        elif keys[pygame.K_DOWN]:
            scroll_speed = 10
        else:
            scroll_speed = 0  # Stop scrolling when no input

        # Update scroll offset
        scroll_offset += scroll_speed
        scroll_offset = max(0, min(scroll_offset, max_scroll))  # Clamp to valid range

        # Draw the background with sliding effect
        bg_y = -scroll_offset % SCREEN_HEIGHT
        screen.blit(level_bg, (0, bg_y - SCREEN_HEIGHT))
        screen.blit(level_bg, (0, bg_y))

        # Draw the path
        for i in range(1, len(path_nodes)):
            start = (path_nodes[i - 1][0], path_nodes[i - 1][1] - scroll_offset)
            end = (path_nodes[i][0], path_nodes[i][1] - scroll_offset)
            pygame.draw.line(screen, GRAY, start, end, 5)

        # Draw the planets (nodes for levels)
        for i, (x, y) in enumerate(path_nodes):
            y -= scroll_offset
            if y < -50 or y > SCREEN_HEIGHT + 50:
                continue  # Skip nodes outside the screen

            planet_rect = planet_images[i].get_rect(center=(x, y))
            screen.blit(planet_images[i], planet_rect)

            # Overlay locked status if the level is locked
            if not levels[i]["unlocked"]:
                pygame.draw.circle(screen, BLACK, (x, y), 40)
                draw_text("X", x, y, RED, 48, center=True)

            # Draw stars below the node
            for s in range(levels[i]["stars"]):
                pygame.draw.circle(screen, YELLOW, (x - 20 + s * 20, y + 50), 8)

            # Draw the level number
            draw_text(str(i + 1), x, y + 50, WHITE, 24, center=True)

        # Draw the title
        draw_text("SELECT LEVEL", SCREEN_WIDTH // 2, 50, YELLOW, 48, center=True)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, (x, y) in enumerate(path_nodes):
                    y -= scroll_offset
                    if (x - mx) ** 2 + (y - my) ** 2 <= 40 ** 2:
                        if levels[i]["unlocked"]:
                            current_level = i
                            level_screen()

        clock.tick(FPS)




def level_screen():
    global current_level
    spaceship = pygame.Rect(375, 500, 50, 50)
    asteroids = [pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), -50, 50, 50) for _ in range(5 + current_level)]
    lasers = []
    boss = None
    boss_health = 10 + (current_level - 10) * 5 if current_level == 10 else 0
    boss_projectiles = []
    score = 0
    stars = 0
    move_x = 0

    # Score thresholds for stars
    min_score_for_1_star = 20 + (current_level * 10)
    score_for_2_stars = min_score_for_1_star * 2
    score_for_3_stars = min_score_for_1_star * 3

    running = True
    while running:
        screen.fill(BLACK)

        # Draw spaceship
        spaceship.x += move_x
        spaceship.x = max(0, min(SCREEN_WIDTH - spaceship.width, spaceship.x))
        screen.blit(spaceship_img, spaceship)

        # Handle asteroids
        asteroid_speed = 5 + current_level  # Speed increases with level
        for asteroid in asteroids:
            asteroid.y += asteroid_speed
            if asteroid.y > SCREEN_HEIGHT:
                asteroid.x, asteroid.y = random.randint(0, SCREEN_WIDTH - 50), -50
                score += 1
            screen.blit(asteroid_img, asteroid)

        # Collision detection for asteroids
        for asteroid in asteroids:
            if spaceship.colliderect(asteroid):
                running = False
                break

        # Boss level mechanics
        if current_level == 10:
            if boss is None:
                boss = pygame.Rect(300, 50, 200, 50)
            pygame.draw.rect(screen, RED, boss)
            boss.x += random.choice([-3, 3])
            boss.x = max(0, min(SCREEN_WIDTH - boss.width, boss.x))

            # Boss projectiles
            if random.random() < 0.02:  # Boss fires projectiles randomly
                boss_projectiles.append(pygame.Rect(boss.x + boss.width // 2, boss.y + boss.height, 10, 20))

            for projectile in boss_projectiles:
                projectile.y += 7
                if projectile.colliderect(spaceship):
                    running = False
                if projectile.y > SCREEN_HEIGHT:
                    boss_projectiles.remove(projectile)
                else:
                    pygame.draw.rect(screen, YELLOW, projectile)

            for laser in lasers:
                if laser.colliderect(boss):
                    lasers.remove(laser)
                    boss_health -= 1
                    score += 5
                    if boss_health <= 0:
                        running = False
                        stars = 3

        # Handle lasers
        for laser in lasers:
            laser.y -= 10
            screen.blit(laser_img, laser)
            if laser.y < 0:
                lasers.remove(laser)

        # Draw score and stars
        draw_text(f"Score: {score}", 10, 10, WHITE, 28)
        draw_text(f"Stars: {stars}", 10, 40, WHITE, 28)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_x = -7
                elif event.key == pygame.K_RIGHT:
                    move_x = 7
                elif event.key == pygame.K_SPACE:
                    lasers.append(pygame.Rect(spaceship.x + 20, spaceship.y, 10, 40))
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    move_x = 0

        # Determine stars based on score
        if score >= min_score_for_1_star:
            if score >= score_for_3_stars:
                stars = 3
                if current_level != 10:
                    running = False  # End normal levels when 3 stars are achieved
            elif score >= score_for_2_stars:
                stars = 2
            else:
                stars = 1

    # Save progress and unlock the next level
    if stars >= 1:
        levels[current_level]["stars"] = max(levels[current_level]["stars"], stars)
        if current_level + 1 < len(levels):
            levels[current_level + 1]["unlocked"] = True



# Main Game Loop
main_menu()
