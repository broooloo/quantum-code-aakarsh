"""
🌌 Birthday Protocol

A cinematic birthday experience built with Python and Pygame.

Features:

* Animated starfield
* Dynamic night-sky gradients
* Shooting stars
* Fireworks system
* Background music
* Constellation effects
* Typewriter-style name reveal
* Cinematic storytelling sequence

Created as a personalized birthday gift and creative coding project.

A combination of animation, visual effects, music, and storytelling designed to turn a simple birthday message into an interactive experience.
"""

import pygame
import random
import math
import time
import os

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h
6
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.FULLSCREEN
)

pygame.display.set_caption(
    "Birthday Protocol"
)

clock = pygame.time.Clock()

FPS = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)
PURPLE = (216, 150, 255)


script_dir = os.path.dirname(
    os.path.abspath(__file__)
)

music_path = os.path.join(
    script_dir,
    "..",
    "Assets",
    "Piano Instrumental.mp3"
)

music_path = os.path.abspath(music_path)

try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)
except:
    print("Music not found.")

NAME = "Birthday_Boy/Girl"

big_font = pygame.font.SysFont(
    "Georgia",
    58,
    bold=True
)

mid_font = pygame.font.SysFont(
    "Georgia",
    40
)

small_font = pygame.font.SysFont(
    "Georgia",
    36
)

tiny_font = pygame.font.SysFont(
    "Arial",
    26,
    "bold",
    "italic"
)

STAR_COUNT = 300

stars = []

for _ in range(STAR_COUNT):

    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.randint(1, 3),
        "speed": random.uniform(0.05, 0.35),
        "phase": random.uniform(0, math.pi * 2)
    })

particles = []

def create_firework():

    x = random.randint(250, WIDTH - 250)

    y = random.randint(100, HEIGHT // 2)

    colors = [
        (0,255,255),
        (255,255,255),
        (138,43,226),
        (135,206,250),
        (186,85,211)
    ]

    color = random.choice(colors)

    for angle in range(0, 360, 8):

        speed = random.uniform(2, 6)

        dx = math.cos(
            math.radians(angle)
        ) * speed

        dy = math.sin(
            math.radians(angle)
        ) * speed

        particles.append({
            "x": x,
            "y": y,
            "dx": dx,
            "dy": dy,
            "life": 80,
            "color": color
        })

shooting_stars = []

def spawn_shooting_star():

    shooting_stars.append({
        "x": random.randint(-200, 0),
        "y": random.randint(0, HEIGHT // 2),
        "dx": random.uniform(18, 26),
        "dy": random.uniform(6, 10),
        "life": 60
    })

gradient_surface = pygame.Surface(
    (WIDTH, HEIGHT)
)

for y in range(HEIGHT):

    blend = y / HEIGHT

    r = int(1 + blend * 6)
    g = int(2 + blend * 10)
    b = int(8 + blend * 22)

    pygame.draw.line(
        gradient_surface,
        (r, g, b),
        (0, y),
        (WIDTH, y)
    )

def draw_glow(surface, color, pos, radius):

    for i in range(3):

        alpha = max(10, 90 - i * 18)

        glow_surface = pygame.Surface(
            (radius * 4, radius * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow_surface,
            (*color, alpha),
            (radius * 2, radius * 2),
            radius + i * 10
        )

        surface.blit(
            glow_surface,
            (
                pos[0] - radius * 2,
                pos[1] - radius * 2
            )
        )

moon_x = WIDTH - 180
moon_y = 160

def draw_text(text, font, color, y):

    render = font.render(
        text,
        True,
        color
    )

    rect = render.get_rect(
        center=(WIDTH // 2, y)
    )

    screen.blit(render, rect)

def draw_stars():

    current = time.time()

    for star in stars:

        star["x"] += star["speed"]

        if star["x"] > WIDTH:
            star["x"] = 0

        pulse = abs(
            math.sin(
                current * 2 + star["phase"]
            )
        )

        brightness = int(
            150 + pulse * 105
        )

        size = star["size"] + pulse * 1.5

        color = (
            brightness,
            brightness,
            brightness
        )

        pygame.draw.circle(
            screen,
            color,
            (
                int(star["x"]),
                int(star["y"])
            ),
            int(size)
        )

def update_shooting_stars():

    alive = []

    for s in shooting_stars:

        s["x"] += s["dx"]
        s["y"] += s["dy"]

        s["life"] -= 1

        for i in range(200):

            trail_x = s["x"] - i * 16
            trail_y = s["y"] - i * 6

            alpha = max(
                0,
                255 - i * 25
            )

            trail_surface = pygame.Surface(
                (20,20),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                trail_surface,
                (255,255,255,alpha),
                (10,10),
                max(1, 5 - i//2)
            )

            screen.blit(
                trail_surface,
                (trail_x, trail_y)
            )

        if s["life"] > 0:
            alive.append(s)

    shooting_stars[:] = alive

def update_fireworks():

    alive = []

    for p in particles:

        p["x"] += p["dx"]
        p["y"] += p["dy"]

        p["dy"] += 0.05

        p["dx"] *= 0.99
        p["dy"] *= 0.99

        p["life"] -= 1

        if p["life"] > 0:

            radius = max(
                1,
                p["life"] // 10
            )

            glow = pygame.Surface(
                (radius * 8, radius * 8),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow,
                (*p["color"], 50),
                (radius * 4, radius * 4),
                radius * 3
            )

            screen.blit(
                glow,
                (
                    p["x"] - radius * 4,
                    p["y"] - radius * 4
                )
            )

            pygame.draw.circle(
                screen,
                p["color"],
                (
                    int(p["x"]),
                    int(p["y"])
                ),
                radius
            )

            alive.append(p)

    particles[:] = alive

constellation = [
    (200, 220),
    (260, 260),
    (330, 310),
    (400, 350),
    (470, 420),
    (560, 500)
]

def render_scene():

    screen.blit(
        gradient_surface,
        (0,0)
    )

    draw_stars()

    for i in range(len(constellation)-1):

        pygame.draw.line(
            screen,
            (120,200,255),
            constellation[i],
            constellation[i+1],
            2
        )

    for point in constellation:

        draw_glow(
            screen,
            (120,200,255),
            point,
            4
        )

        pygame.draw.circle(
            screen,
            (180,230,255),
            point,
            3
        )

    draw_glow(
    screen,
    (140,140,145),
    (moon_x, moon_y),
    110
)

    pygame.draw.circle(
    screen,
    (245,245,220),
    (moon_x, moon_y),
    110
)

    pygame.draw.circle(
    screen,
    (8,10,20),
    (moon_x + 45, moon_y),
    100
)

    update_shooting_stars()

    update_fireworks()

intro_lines = [
    "Connecting To Sky...",
    "Scanning Constellations...",
    "Searching Rare Signals...",
    "Searching Calendar...",
    "Finding Important Event..."
]

running = True

for line in intro_lines:

    start = time.time()

    while time.time() - start < 1.2:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

        render_scene()

        draw_text(
            line,
            mid_font,
            CYAN,
            180
        )

        pygame.display.update()

        clock.tick(FPS)

start = time.time()

while time.time() - start < 2:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    render_scene()

    draw_text(
        "✨ RARE SKY EVENT FOUND ✨",
        big_font,
        GOLD,
        HEIGHT // 2 - 50
    )

    pygame.display.update()

    clock.tick(FPS)

start = time.time()

while time.time() - start < 2:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    render_scene()

    draw_text(
        f"🚨 {NAME.upper()} BIRTHDAY DETECTED 🚨",
        mid_font,
        CYAN,
        HEIGHT // 2
    )

    pygame.display.update()

    clock.tick(FPS)

start = time.time()

while time.time() - start < 2:

    render_scene()

    draw_text(
        "Among billions of stars ✨",
        small_font,
        WHITE,
        HEIGHT // 2 - 20
    )

    draw_text(
        "A rare light still stands apart.",
        small_font,
        WHITE,
        HEIGHT // 2 + 20
    )

    pygame.display.update()

    clock.tick(FPS)

current = ""

for letter in NAME:

    current += letter

    start = time.time()

    while time.time() - start < 0.16:

        render_scene()

        draw_text(
            f"✨ Happy Birthday, {current} ✨",
            big_font,
            GOLD,
            HEIGHT // 2 + 80
        )

        pygame.display.update()

        clock.tick(FPS)

for _ in range(8):

    spawn_shooting_star()

start = time.time()

while time.time() - start < 3:

    render_scene()

    draw_text(
        "🌙 A night like this visits only once...",
        small_font,
        (170,170,170),
        HEIGHT - 120
    )

    pygame.display.update()

    clock.tick(FPS)

for _ in range(3):

    create_firework()

    timer = time.time()

    while time.time() - timer < 1.2:

        render_scene()

        pygame.display.update()

        clock.tick(FPS)

start = time.time()

while time.time() - start < 7:

    render_scene()

    if random.randint(0, 100) < 2:
        spawn_shooting_star()

    if random.randint(0, 100) < 3:
        create_firework()

    draw_text(
        "🌙 THE STARS CELEBRATE YOU TONIGHT 🌙",
        big_font,
        PURPLE,
        HEIGHT // 2 - 40
    )

    draw_text(
        f"✨ HAPPY BIRTHDAY {NAME.upper()} ✨",
        mid_font,
        GOLD,
        HEIGHT // 2 + 40
    )

    fps_text = tiny_font.render(
        f"FPS : {int(clock.get_fps())}",
        True,
        (90,90,90)
    )

    screen.blit(
        fps_text,
        (WIDTH - 120, 30)
    )

    pygame.display.update()

    clock.tick(FPS)

pygame.mixer.music.fadeout(3000)

fade = pygame.Surface((WIDTH, HEIGHT))

fade.fill(BLACK)

for alpha in range(0, 255, 4):

    render_scene()

    fade.set_alpha(alpha)

    screen.blit(fade, (0,0))

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
