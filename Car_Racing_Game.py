"""
========================================
Aakarsh Racer 
========================================

Requirements:
    pip install pygame

Optional Sound Setup:
    1. Download a .wav engine sound
    2. Rename it to: engine.wav
    3. Put it beside this script

OR

    Set ENABLE_SOUND = False

and the game will run perfectly without sound.
"""

import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

FPS = 60

ENABLE_SOUND = False
ENGINE_SOUND_FILE = "engine.wav"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ROAD_COLOR = (60, 60, 60)
LINE_COLOR = (255, 255, 255)

RED = (255, 50, 50)
BLUE = (0, 180, 255)
YELLOW = (255, 255, 100)

ORANGE = (255, 165, 0)


class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-10, 10)

        self.life = 30

        self.color = random.choice(
            [RED, YELLOW, ORANGE]
        )

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.life -= 1

    def draw(self, screen):

        if self.life > 0:

            size = max(
                1,
                int(3 * (self.life / 30))
            )

            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                size
            )


class Car:

    def __init__(
        self,
        x,
        y,
        color,
        speed=0
    ):

        self.x = x
        self.y = y

        self.width = 50
        self.height = 80

        self.color = color
        self.speed = speed

        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )

        self.vx = 0
        self.vy = 0

        self.acceleration = 2.2
        self.friction = 0.94

    def update_player(self, keys):

        if keys[pygame.K_LEFT]:
            self.vx -= self.acceleration

        if keys[pygame.K_RIGHT]:
            self.vx += self.acceleration

        if keys[pygame.K_UP]:
            self.vy -= self.acceleration

        if keys[pygame.K_DOWN]:
            self.vy += self.acceleration

        self.vx = max(
            min(self.vx, 15),
            -15
        )

        self.vy = max(
            min(self.vy, 15),
            -15
        )

        self.vx *= self.friction
        self.vy *= self.friction

        self.x += self.vx
        self.y += self.vy

        self.x = max(
            100,
            min(
                SCREEN_WIDTH - 150,
                self.x
            )
        )

        self.y = max(
            200,
            min(
                SCREEN_HEIGHT - 100,
                self.y
            )
        )

        self.rect.topleft = (
            self.x,
            self.y
        )

    def move(self, dy):

        self.y += dy

        self.rect.y = self.y

    def draw(self, screen):

        for i in range(5):

            trail = self.rect.copy()

            trail.y += i * 5

            pygame.draw.rect(
                screen,
                (50, 50, 255),
                trail,
                1
            )

        pygame.draw.polygon(
            screen,
            self.color,
            [
                (self.x, self.y),

                (
                    self.x + self.width,
                    self.y
                ),

                (
                    self.x + self.width - 10,
                    self.y + self.height
                ),

                (
                    self.x + 10,
                    self.y + self.height
                )
            ]
        )


class Road:
    def __init__(self):

        self.lines = [
            {'y': i * 40}
            for i in range(20)
        ]

    def update(self, speed_multiplier):

        speed = (
            8 +
            speed_multiplier * 4
        )

        for line in self.lines:

            line['y'] += speed

            if line['y'] > SCREEN_HEIGHT:
                line['y'] = -40

    def draw(self, screen):

        for line in self.lines:

            pygame.draw.rect(
                screen,
                LINE_COLOR,
                (
                    SCREEN_WIDTH // 2 - 5,
                    line['y'],
                    10,
                    40
                )
            )


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

        pygame.display.set_caption(
            "🔥 Aakarsh Racer ULTRA V2 🔥"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(
            None,
            36
        )

        self.big_font = pygame.font.Font(
            None,
            80
        )

        self.engine_sound = None

        if ENABLE_SOUND:

            try:

                pygame.mixer.init()

                self.engine_sound = pygame.mixer.Sound(
                    ENGINE_SOUND_FILE
                )

                self.engine_sound.play(-1)

            except Exception:

                print(
                    f"Sound file '{ENGINE_SOUND_FILE}' not found."
                )

                self.engine_sound = None

        self.high_score = 0
        self.paused = False

        self.reset()

    def reset(self):

        self.player = Car(
            375,
            650,
            BLUE
        )

        self.enemies = []
        self.particles = []

        self.road = Road()

        self.score = 0
        self.lives = 3

        self.speed_multiplier = 1

        self.game_over = False

    def spawn_enemy(self):

        if random.randint(1, 35) == 1:

            lane = random.choice(
                [
                    150,
                    350,
                    550
                ]
            )

            speed = random.randint(
                4,
                10
            )

            self.enemies.append(
                Car(
                    lane,
                    -80,
                    RED,
                    speed
                )
            )

    def update(self):

        if self.paused:
            return

        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        self.player.update_player(
            keys
        )

        self.road.update(
            self.speed_multiplier
        )

        self.spawn_enemy()

        if random.randint(1, 5) == 1:

            self.particles.append(
                Particle(
                    random.randint(
                        100,
                        700
                    ),
                    random.randint(
                        0,
                        SCREEN_HEIGHT
                    )
                )
            )

        for enemy in self.enemies[:]:

            enemy.move(
                enemy.speed *
                self.speed_multiplier
            )

            if enemy.y > SCREEN_HEIGHT:

                self.enemies.remove(
                    enemy
                )

                self.score += 10

            if self.player.rect.colliderect(
                enemy.rect
            ):

                self.lives -= 1

                self.enemies.remove(
                    enemy
                )

                for _ in range(40):

                    self.particles.append(
                        Particle(
                            enemy.x,
                            enemy.y
                        )
                    )

        for particle in self.particles[:]:

            particle.update()

            if particle.life <= 0:

                self.particles.remove(
                    particle
                )

        if self.engine_sound:

            speed = (
                abs(self.player.vx)
                +
                abs(self.player.vy)
            )

            volume = min(
                1.0,
                speed / 15
            )

            self.engine_sound.set_volume(
                volume
            )

        self.score += 1

        self.high_score = max(
            self.high_score,
            self.score
        )

        self.speed_multiplier += 0.002

        self.speed_multiplier = min(
            self.speed_multiplier,
            6
        )

        if self.lives <= 0:

            self.game_over = True

    def draw(self):

        for i in range(
            SCREEN_HEIGHT
        ):

            val = int(
                (
                    i /
                    SCREEN_HEIGHT
                ) * 255
            )

            color = (
                val // 3,
                0,
                val
            )

            pygame.draw.line(
                self.screen,
                color,
                (0, i),
                (
                    SCREEN_WIDTH,
                    i
                )
            )

        pygame.draw.rect(
            self.screen,
            ROAD_COLOR,
            (
                100,
                0,
                600,
                SCREEN_HEIGHT
            )
        )

        pygame.draw.rect(
            self.screen,
            (0, 100, 255),
            (
                100,
                0,
                600,
                SCREEN_HEIGHT
            ),
            3
        )

        for _ in range(20):

            x = random.randint(
                100,
                700
            )

            y = random.randint(
                0,
                SCREEN_HEIGHT
            )

            pygame.draw.line(
                self.screen,
                WHITE,
                (x, y),
                (
                    x,
                    y + 10
                )
            )

        self.road.draw(
            self.screen
        )

        self.player.draw(
            self.screen
        )

        for enemy in self.enemies:

            for i in range(5):

                pygame.draw.rect(
                    self.screen,
                    RED,
                    enemy.rect.inflate(
                        i * 4,
                        i * 4
                    ),
                    1
                )

            enemy.draw(
                self.screen
            )

        for particle in self.particles:

            particle.draw(
                self.screen
            )

        self.screen.blit(
            self.font.render(
                f"Score: {self.score}",
                True,
                WHITE
            ),
            (10, 10)
        )

        self.screen.blit(
            self.font.render(
                f"Lives: {self.lives}",
                True,
                WHITE
            ),
            (10, 50)
        )

        self.screen.blit(
            self.font.render(
                f"High Score: {self.high_score}",
                True,
                WHITE
            ),
            (10, 90)
        )

        if self.paused:

            text = self.big_font.render(
                "PAUSED",
                True,
                YELLOW
            )

            self.screen.blit(
                text,
                (
                    220,
                    350
                )
            )

        if self.game_over:

            text = self.big_font.render(
                "GAME OVER",
                True,
                RED
            )

            self.screen.blit(
                text,
                (
                    110,
                    320
                )
            )

            restart = self.font.render(
                "Press R to Restart",
                True,
                WHITE
            )

            self.screen.blit(
                restart,
                (
                    280,
                    420
                )
            )

        pygame.display.flip()

    def run(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                if (
                    event.type ==
                    pygame.KEYDOWN
                ):

                    if event.key == pygame.K_p:

                        self.paused = (
                            not self.paused
                        )

                    if (
                        event.key ==
                        pygame.K_r
                        and
                        self.game_over
                    ):

                        self.reset()

            self.update()

            self.draw()

            self.clock.tick(
                FPS
            )


if __name__ == "__main__":

    Game().run()
