import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions (fullscreen)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Basket (player)
basket_width, basket_height = 100, 50
basket_speed = 10

# Falling objects
object_size = 50

# Score & Lives
font = pygame.font.SysFont(None, 48)

# Load images
basket_img = pygame.image.load("basket.png")
basket_img = pygame.transform.scale(basket_img, (basket_width, basket_height))

apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (object_size, object_size))

bomb_img = pygame.image.load("bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (object_size, object_size))

game_over_img = pygame.image.load("gameover.png")
game_over_img = pygame.transform.scale(game_over_img, (400, 150))

# Load sounds
catch_sound = pygame.mixer.Sound("catch.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Background music
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)  # Loop forever

# High score file
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def spawn_object(falling_objects):
    x = random.randint(0, WIDTH-object_size)
    rect = pygame.Rect(x, 0, object_size, object_size)
    obj_type = random.choice(["good", "bad"])  # Randomly choose type
    falling_objects.append((rect, obj_type))

def game_loop(high_score):
    basket = pygame.Rect(WIDTH//2, HEIGHT-80, basket_width, basket_height)
    falling_objects = []
    score = 0
    lives = 3
    object_speed = 6
    spawn_chance = 30

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket.left > 0:
            basket.x -= basket_speed
        if keys[pygame.K_RIGHT] and basket.right < WIDTH:
            basket.x += basket_speed

        # Difficulty scaling
        object_speed = 6 + score // 10
        spawn_chance = max(8, 30 - score//5)

        # Spawn objects randomly
        if random.randint(1, spawn_chance) == 1:
            spawn_object(falling_objects)

        # Move objects
        for obj in falling_objects[:]:
            rect, obj_type = obj
            rect.y += object_speed
            if rect.colliderect(basket):
                if obj_type == "good":
                    score += 1
                    catch_sound.play()
                else:  # bad object
                    lives -= 1
                    explosion_sound.play()
                falling_objects.remove(obj)
            elif rect.y > HEIGHT:
                falling_objects.remove(obj)

        # Draw everything
        screen.fill(WHITE)
        screen.blit(basket_img, basket)
        for rect, obj_type in falling_objects:
            if obj_type == "good":
                screen.blit(apple_img, rect)
            else:
                screen.blit(bomb_img, rect)

        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 70))
        screen.blit(high_score_text, (20, 120))

        # Game Over
        if lives <= 0:
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            screen.blit(game_over_img, (WIDTH//2 - 200, HEIGHT//2 - 100))
            restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
            screen.blit(restart_text, (WIDTH//2 - 250, HEIGHT//2 + 80))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Restart
                            return True, high_score
                        if event.key == pygame.K_q:  # Quit
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()
        clock.tick(30)

def start_screen(high_score):
    while True:
        screen.fill(WHITE)
        title_text = font.render("Catch the Falling Objects", True, BLACK)
        start_text = font.render("Press SPACE to Start", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(title_text, (WIDTH//2 - 250, HEIGHT//2 - 100))
        screen.blit(start_text, (WIDTH//2 - 200, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - 150, HEIGHT//2 + 60))
        screen.blit(high_score_text, (WIDTH//2 - 150, HEIGHT//2 + 120))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main loop
high_score = load_high_score()
while True:
    start_screen(high_score)
    restart, high_score = game_loop(high_score)
    if not restart:
        break
