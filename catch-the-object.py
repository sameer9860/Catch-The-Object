import pygame
import random
import sys
import os
import math

# ── Init ────────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")
clock = pygame.time.Clock()

# ── Colors ───────────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
RED     = (220,  50,  50)
GREEN   = ( 50, 205,  50)
GOLD    = (255, 215,   0)
CYAN    = (  0, 220, 220)
PURPLE  = (150,  50, 220)
ORANGE  = (255, 140,   0)

# ── Fonts ────────────────────────────────────────────────────────────────────
FONT_BIG   = pygame.font.SysFont("segoeui", 56, bold=True)
FONT_MED   = pygame.font.SysFont("segoeui", 38, bold=True)
FONT_SMALL = pygame.font.SysFont("segoeui", 28)

# ── Basket ────────────────────────────────────────────────────────────────────
BASE_BASKET_W, BASKET_H = 120, 55
BASKET_SPEED = 10

# ── Object sizes ─────────────────────────────────────────────────────────────
OBJ_SIZE = 52

# ── Object type definitions ───────────────────────────────────────────────────
# Each type: (image_key, points, is_bad, power_up)
OBJECT_TYPES = {
    "apple":  dict(points=1,  bad=False, power=None,          weight=50),
    "golden": dict(points=3,  bad=False, power="double",      weight=15),
    "heart":  dict(points=0,  bad=False, power="extra_life",  weight=10),
    "wand":   dict(points=0,  bad=False, power="wide_basket", weight=8),
    "bomb":   dict(points=0,  bad=True,  power=None,          weight=17),
}

# ── Load assets ───────────────────────────────────────────────────────────────
def load_img(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)

basket_img     = load_img("basket.png",   (BASE_BASKET_W, BASKET_H))
apple_img      = load_img("apple.png",    (OBJ_SIZE, OBJ_SIZE))
bomb_img       = load_img("bomb.png",     (OBJ_SIZE, OBJ_SIZE))
game_over_img  = load_img("gameover.png", (480, 180))

# Golden apple: tint the apple image yellow
golden_img = apple_img.copy()
golden_surf = pygame.Surface((OBJ_SIZE, OBJ_SIZE), pygame.SRCALPHA)
golden_surf.fill((255, 200, 0, 100))
golden_img.blit(golden_surf, (0, 0))

# Heart: draw a simple red heart programmatically
heart_img = pygame.Surface((OBJ_SIZE, OBJ_SIZE), pygame.SRCALPHA)
pygame.draw.circle(heart_img, (220, 20, 60), (16, 16), 16)
pygame.draw.circle(heart_img, (220, 20, 60), (36, 16), 16)
points = [(0,20),(26,50),(52,20),(36,0),(26,10),(16,0)]
pygame.draw.polygon(heart_img, (220, 20, 60), points)

# Magic wand: purple star
wand_img = pygame.Surface((OBJ_SIZE, OBJ_SIZE), pygame.SRCALPHA)
center = (OBJ_SIZE//2, OBJ_SIZE//2)
for i in range(5):
    angle = math.radians(i * 72 - 90)
    outer = (center[0] + 24*math.cos(angle), center[1] + 24*math.sin(angle))
    angle2 = math.radians(i * 72 - 90 + 36)
    inner = (center[0] + 10*math.cos(angle2), center[1] + 10*math.sin(angle2))
star_points = []
for i in range(5):
    a_out = math.radians(i * 72 - 90)
    a_in  = math.radians(i * 72 - 90 + 36)
    star_points.append((center[0] + 24*math.cos(a_out), center[1] + 24*math.sin(a_out)))
    star_points.append((center[0] + 10*math.cos(a_in),  center[1] + 10*math.sin(a_in)))
pygame.draw.polygon(wand_img, PURPLE, star_points)
pygame.draw.polygon(wand_img, WHITE,  star_points, 2)

OBJ_IMAGES = {
    "apple":  apple_img,
    "golden": golden_img,
    "heart":  heart_img,
    "wand":   wand_img,
    "bomb":   bomb_img,
}

# Background images
backgrounds = []
for i in range(1, 6):
    bg = pygame.transform.scale(pygame.image.load(f"bg{i}.png"), (WIDTH, HEIGHT))
    backgrounds.append(bg)

# Sounds
catch_sound     = pygame.mixer.Sound("catch.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

HIGH_SCORE_FILE = "highscore.txt"

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            return int(open(HIGH_SCORE_FILE).read())
        except:
            pass
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def draw_text_shadow(surf, text, font, color, pos, shadow_color=(0,0,0), offset=2):
    shadow = font.render(text, True, shadow_color)
    surf.blit(shadow, (pos[0]+offset, pos[1]+offset))
    rendered = font.render(text, True, color)
    surf.blit(rendered, pos)

def weighted_choice(types_dict):
    keys   = list(types_dict.keys())
    weights = [types_dict[k]["weight"] for k in keys]
    return random.choices(keys, weights=weights, k=1)[0]

# ── Particle system ───────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -1)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.radius = random.randint(3, 7)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.25          # gravity
        self.life -= 1

    def draw(self, surf):
        alpha = int(255 * self.life / self.max_life)
        r = max(1, int(self.radius * self.life / self.max_life))
        col = (*self.color, alpha)
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (r, r), r)
        surf.blit(s, (int(self.x)-r, int(self.y)-r))

def spawn_particles(particles, x, y, color, count=20):
    for _ in range(count):
        particles.append(Particle(x, y, color))

# ── Power-up state ────────────────────────────────────────────────────────────
class PowerUp:
    def __init__(self):
        self.wide_basket_timer = 0
        self.wide_basket_active = False

    def activate(self, kind):
        if kind == "wide_basket":
            self.wide_basket_timer = 300   # ~10 seconds at 30fps
            self.wide_basket_active = True

    def update(self):
        if self.wide_basket_active:
            self.wide_basket_timer -= 1
            if self.wide_basket_timer <= 0:
                self.wide_basket_active = False

    @property
    def basket_width(self):
        return BASE_BASKET_W * 2 if self.wide_basket_active else BASE_BASKET_W

# ── HUD drawing ───────────────────────────────────────────────────────────────
def draw_hud(surf, score, lives, high_score, level, combo, power_up):
    # Semi-transparent panel at top
    panel = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 120))
    surf.blit(panel, (0, 0))

    draw_text_shadow(surf, f"Score: {score}",      FONT_MED, WHITE,  (20, 8))
    draw_text_shadow(surf, f"High: {high_score}",  FONT_MED, GOLD,   (250, 8))
    draw_text_shadow(surf, f"Level {level+1}",     FONT_MED, CYAN,   (500, 8))

    # Lives as heart icons
    for i in range(lives):
        surf.blit(heart_img, (WIDTH - 50 - i * 55, 8))

    # Combo badge
    if combo > 1:
        combo_col = GOLD if combo >= 5 else GREEN
        badge = FONT_BIG.render(f"x{combo} COMBO!", True, combo_col)
        badge.set_alpha(220)
        surf.blit(badge, (WIDTH//2 - badge.get_width()//2, 95))

    # Wide basket timer bar
    if power_up.wide_basket_active:
        bar_w = int((power_up.wide_basket_timer / 300) * 200)
        pygame.draw.rect(surf, PURPLE, (20, 95, 200, 12), border_radius=6)
        pygame.draw.rect(surf, WHITE,  (20, 95, bar_w, 12), border_radius=6)
        draw_text_shadow(surf, "Wide Basket!", FONT_SMALL, PURPLE, (230, 90))

# ── Game loop ─────────────────────────────────────────────────────────────────
def game_loop(high_score):
    power_up = PowerUp()
    basket_w = power_up.basket_width
    basket = pygame.Rect(WIDTH//2 - basket_w//2, HEIGHT - 90, basket_w, BASKET_H)

    falling_objects = []   # list of [rect, type_key, speed]
    particles       = []
    score       = 0
    lives       = 3
    combo       = 0
    shake_timer = 0

    spawn_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        # Level & difficulty
        level        = score // 20
        bg_image     = backgrounds[level % len(backgrounds)]
        object_speed = 5 + level * 2.5
        spawn_rate   = max(6, 28 - level * 2)   # frames between spawns

        # Move basket
        keys = pygame.key.get_pressed()
        basket_w = power_up.basket_width
        basket.width = basket_w
        if keys[pygame.K_LEFT]  and basket.left  > 0:     basket.x -= BASKET_SPEED
        if keys[pygame.K_RIGHT] and basket.right < WIDTH:  basket.x += BASKET_SPEED

        power_up.update()

        # Spawn
        spawn_timer += 1
        if spawn_timer >= spawn_rate:
            spawn_timer = 0
            x      = random.randint(0, WIDTH - OBJ_SIZE)
            kind   = weighted_choice(OBJECT_TYPES)
            rect   = pygame.Rect(x, -OBJ_SIZE, OBJ_SIZE, OBJ_SIZE)
            spd    = object_speed * random.uniform(0.85, 1.15)
            falling_objects.append([rect, kind, spd])

        # Move & collide
        for obj in falling_objects[:]:
            rect, kind, spd = obj
            rect.y += spd
            info_d = OBJECT_TYPES[kind]

            if rect.colliderect(basket):
                cx, cy = rect.centerx, rect.centery
                if info_d["bad"]:
                    lives -= 1
                    combo  = 0
                    shake_timer = 12
                    explosion_sound.play()
                    spawn_particles(particles, cx, cy, RED, 30)
                else:
                    pts = info_d["points"]
                    if pts == 0 and info_d["power"] is None:
                        pts = 1
                    combo += 1
                    multiplier = 1 + (combo // 3)
                    score += pts * multiplier
                    catch_sound.play()
                    p_col = GOLD if kind == "golden" else (WHITE if kind in ("heart","wand") else GREEN)
                    spawn_particles(particles, cx, cy, p_col, 18)
                    if info_d["power"] == "extra_life":
                        lives = min(lives + 1, 7)
                    elif info_d["power"]:
                        power_up.activate(info_d["power"])
                falling_objects.remove(obj)

            elif rect.y > HEIGHT:
                if not info_d["bad"]:
                    combo = 0        # missed a good object → reset combo
                falling_objects.remove(obj)

        # Update particles
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)

        # Screen shake offset
        ox = random.randint(-6, 6) if shake_timer > 0 else 0
        oy = random.randint(-4, 4) if shake_timer > 0 else 0
        if shake_timer > 0: shake_timer -= 1

        # ── Draw ──────────────────────────────────────────────────────────────
        screen.blit(bg_image, (ox, oy))

        # Basket (resize image on the fly if needed)
        b_img = pygame.transform.scale(basket_img, (basket_w, BASKET_H))
        screen.blit(b_img, basket)

        for rect, kind, _ in falling_objects:
            screen.blit(OBJ_IMAGES[kind], rect)

        for p in particles:
            p.draw(screen)

        draw_hud(screen, score, lives, high_score, level, combo, power_up)

        # Game Over
        if lives <= 0:
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            # Dim overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            screen.blit(game_over_img, (WIDTH//2 - 240, HEIGHT//2 - 130))
            draw_text_shadow(screen, f"Final Score: {score}", FONT_MED, GOLD,
                             (WIDTH//2 - 150, HEIGHT//2 + 70))
            draw_text_shadow(screen, "R  -  Restart     Q  -  Quit", FONT_SMALL, WHITE,
                             (WIDTH//2 - 190, HEIGHT//2 + 125))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return True, high_score
                        if event.key == pygame.K_q:
                            pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(30)

# ── Start screen ──────────────────────────────────────────────────────────────
def start_screen(high_score):
    bg_angle = 0
    while True:
        # Animated gradient background
        for y in range(HEIGHT):
            frac = y / HEIGHT
            r = int(10 + 30*frac)
            g = int(10 + 20*frac)
            b = int(40 + 80*frac)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # Floating title particles effect (simple twinkles)
        for _ in range(3):
            tx = random.randint(0, WIDTH)
            ty = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, (255, 255, 255, 80), (tx, ty), random.randint(1, 3))

        # Title
        title = FONT_BIG.render("🎯  Catch the Falling Objects", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 180))

        # Instruction box
        box = pygame.Surface((500, 240), pygame.SRCALPHA)
        box.fill((0, 0, 0, 140))
        pygame.draw.rect(box, GOLD, box.get_rect(), 2, border_radius=12)
        screen.blit(box, (WIDTH//2 - 250, HEIGHT//2 - 60))

        lines = [
            ("← → to move basket",     WHITE,  -20),
            ("Catch apples to score",   GREEN,   20),
            ("Golden apple  =  x3 pts", GOLD,    60),
            ("Heart  =  extra life",    RED,    100),
            ("Star  =  wide basket",    PURPLE, 140),
        ]
        for txt, col, dy in lines:
            t = FONT_SMALL.render(txt, True, col)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 50 + dy))

        draw_text_shadow(screen, f"🏆  High Score:  {high_score}", FONT_MED, GOLD,
                         (WIDTH//2 - 180, HEIGHT//2 + 210))

        # Pulsing start prompt
        pulse = abs(math.sin(pygame.time.get_ticks() / 500))
        col   = (int(50 + 205*pulse), int(205*pulse), int(50 + 100*pulse))
        draw_text_shadow(screen, "Press  SPACE  to Start", FONT_MED, col,
                         (WIDTH//2 - 210, HEIGHT//2 + 270))
        draw_text_shadow(screen, "Q  -  Quit", FONT_SMALL, (180, 180, 180),
                         (WIDTH//2 - 80, HEIGHT//2 + 320))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# ── Entry point ───────────────────────────────────────────────────────────────
high_score = load_high_score()
while True:
    start_screen(high_score)
    restart, high_score = game_loop(high_score)
    if not restart:
        break
