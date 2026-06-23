import random
import pygame
import sys
import os
from game.powerup import PowerUp
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    BLACK,
    WHITE,
    MAX_PADDLE_WIDTH,
    MIN_BALL_SPEED,
    EXPAND_DURATION,
    SLOW_DURATION,
    COMBO_RESET_TIME
)
from game.paddle import Paddle
from game.ball import Ball
from game.brick import create_bricks, check_brick_collision
from game.particles import Particle


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")

        self.clock = pygame.time.Clock()

        self.paddle = Paddle()
        self.ball = Ball(self.paddle.rect)
        self.bricks = create_bricks()

        self.score = 0
        self.combo = 0
        self.last_brick_hit_time = 0
        self.lives = 3
        self.state = "playing"

        # Particles
        self.particles = []
        #powerups
        self.powerups = []
        # effect timer
        self.expand_timer = 0
        self.slow_timer = 0

        # Sounds
        self.paddle_sound = pygame.mixer.Sound(
            os.path.join("sounds", "paddle.wav")
        )

        self.brick_sound = pygame.mixer.Sound(
            os.path.join("sounds", "brick.wav")
        )

        self.lose_sound = pygame.mixer.Sound(
            os.path.join("sounds", "lose.wav")
        )

        self.win_sound = pygame.mixer.Sound(
            os.path.join("sounds", "win.wav")
        )
        
    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        self.paddle.move(keys)

        if not self.ball.launched and keys[pygame.K_SPACE]:
            self.ball.launch()

        self.ball.move(self.paddle.rect)

        # Ball trail particles
        self.particles.append(
            Particle(
                self.ball.rect.centerx,
                self.ball.rect.centery,
                WHITE
            )
        )

        # Paddle collision
        if self.ball.launched and self.ball.rect.colliderect(self.paddle.rect):
            old_vy = self.ball.vy
            self.ball.bounce_paddle(self.paddle.rect)

            if old_vy != self.ball.vy:
                self.paddle_sound.play()

                # Paddle spark particles
                for _ in range(8):
                    self.particles.append(
                        Particle(
                            self.ball.rect.centerx,
                            self.ball.rect.bottom,
                            (0, 255, 255)
                        )
                    )

        # Brick collision
        result = check_brick_collision(
            self.ball,
            self.bricks
        )

        if result is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_brick_hit_time <= COMBO_RESET_TIME:
                self.combo += 1
            else:
                self.combo = 1

            self.last_brick_hit_time = current_time
            self.score += result * self.combo
            drop_chance = random.random()
            if drop_chance < 0.12:
                self.powerups.append(
                    PowerUp(
                        self.ball.rect.centerx,
                        self.ball.rect.centery,
                        "expand"
                    )
                )

            elif drop_chance < 0.20:
                self.powerups.append(
                    PowerUp(
                        self.ball.rect.centerx,
                        self.ball.rect.centery,
                        "slow"
                    )
                )

            elif drop_chance < 0.25:
                self.powerups.append(
                    PowerUp(
                        self.ball.rect.centerx,
                        self.ball.rect.centery,
                        "life"
                    )
                )
            self.brick_sound.play()

            # Brick explosion particles
            for _ in range(12):
                self.particles.append(
                    Particle(
                        self.ball.rect.centerx,
                        self.ball.rect.centery,
                        (255, 100, 100)
                    )
                )

        # Ball falls below screen
        if self.ball.rect.top > HEIGHT:
            self.lives -= 1
            self.combo = 0
            if self.lives <= 0:
                self.state = "game_over"
                self.lose_sound.play()
            else:
                self.ball.reset(self.paddle.rect)

        # Win condition
        if len(self.bricks) == 0:
            self.state = "won"
            self.win_sound.play()
        #powerup update
        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(self.paddle.rect):
                if powerup.type == "expand":
                    self.paddle.rect.width = min(
                        self.paddle.rect.width + 40,
                        MAX_PADDLE_WIDTH
                    )
                    self.expand_timer = pygame.time.get_ticks()

                elif powerup.type == "slow":
                    self.ball.vx = (
                        -max(abs(self.ball.vx * 0.8), MIN_BALL_SPEED)
                        if self.ball.vx < 0
                        else max(abs(self.ball.vx * 0.8), MIN_BALL_SPEED)
                    )

                    self.ball.vy = (
                        -max(abs(self.ball.vy * 0.8), MIN_BALL_SPEED)
                        if self.ball.vy < 0
                        else max(abs(self.ball.vy * 0.8), MIN_BALL_SPEED)
                    )

                    self.slow_timer = pygame.time.get_ticks()

                elif powerup.type == "life":
                    self.lives += 1

                self.powerups.remove(powerup)

            elif powerup.rect.top > HEIGHT:
                self.powerups.remove(powerup)

        current_time = pygame.time.get_ticks()
        if (
            self.combo > 0
            and current_time - self.last_brick_hit_time > COMBO_RESET_TIME
        ):
            self.combo = 0
        # Expand reset
        if (
            self.expand_timer
            and current_time - self.expand_timer > EXPAND_DURATION
        ):
            self.paddle.rect.width = 120
            self.expand_timer = 0

        # Slow reset
        if (
            self.slow_timer
            and current_time - self.slow_timer > SLOW_DURATION
        ):
            # Restore normal speed while keeping direction
            self.ball.vx = -5 if self.ball.vx < 0 else 5
            self.ball.vy = -5 if self.ball.vy < 0 else 5

            self.slow_timer = 0
            
        # Update particles
        for particle in self.particles[:]:
            particle.update()

            if particle.life <= 0:
                self.particles.remove(particle)
        

    def draw(self):
        self.screen.fill(BLACK)

        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        for brick in self.bricks:
            brick.draw(self.screen)
            
        #draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # HUD
        font = pygame.font.SysFont(None, 36)

        score_text = font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        lives_text = font.render(
            f"Lives: {self.lives}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (20, 10))
        self.screen.blit(lives_text, (WIDTH - 120, 10))

        if self.combo > 1:
            combo_text = font.render(
                f"COMBO x{self.combo}",
                True,
                (255, 215, 0)
            )
            self.screen.blit(combo_text, (WIDTH // 2 - 80, 10))
            
        if self.expand_timer:
            expand_text = font.render(
                f"EXPAND: {(EXPAND_DURATION - (pygame.time.get_ticks() - self.expand_timer)) // 1000}s",
                True,
                (0, 255, 0)
            )
            self.screen.blit(expand_text, (20, 50))

        if self.slow_timer:
            slow_text = font.render(
                f"SLOW: {(SLOW_DURATION - (pygame.time.get_ticks() - self.slow_timer)) // 1000}s",
                True,
                (0, 0, 255)
            )
            self.screen.blit(slow_text, (20, 80))

        # End states
        if self.state == "game_over":
            game_over_text = font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            self.screen.blit(
                game_over_text,
                (WIDTH // 2 - 100, HEIGHT // 2)
            )

        elif self.state == "won":
            win_text = font.render(
                "YOU WIN!",
                True,
                (0, 255, 0)
            )

            self.screen.blit(
                win_text,
                (WIDTH // 2 - 80, HEIGHT // 2)
            )

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw()

            self.clock.tick(FPS)
