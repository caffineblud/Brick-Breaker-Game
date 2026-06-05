# 🧱 brick-breaker

A classic brick-breaker game built with Python and pygame — featuring a two-hit HP system, dynamic speed scaling, and a neon dark-theme aesthetic.

**Author:** *Yash Kumar Singh*

---

## Install & run

```bash
pip install pygame
cd brick_breaker
python main.py
```

---

## Project structure

```
brick_breaker/
├── main.py          ← entry point (3 lines)
├── settings.py      ← all constants & config
└── game/
    ├── __init__.py
    ├── paddle.py    ← Paddle class
    ├── ball.py      ← Ball class + speed control
    ├── brick.py     ← Brick class with HP system
    └── game.py      ← game loop, HUD, overlays, collision
```

---

## Controls

| Key | Action |
|-----|--------|
| `← / A` | Move paddle left |
| `→ / D` | Move paddle right |
| `SPACE` | Launch ball / continue after life loss |
| `R` | Restart after win or game over |
| `ESC` | Quit |

---

## Gameplay

- **60 × 10 brick grid** — 6 rows, 10 columns
- **2-HP bricks** (top 3 rows) darken on first hit and show dot indicators
- **1-HP bricks** (bottom 3 rows) shatter in one hit
- Ball **speeds up** every 5 destroyed bricks (`SPEED_UP_EVERY`, `SPEED_INCREMENT` in `settings.py`)
- Paddle angle influences ball bounce direction based on hit offset

### Scoring

| Event | Points |
|-------|--------|
| Brick destroyed | +10 |
| 2-HP brick hit (not destroyed) | +5 |

### Lives

Start with **3 lives**. Ball falling below screen costs one life. Lose all three → game over.

---

## Row configuration

| Row | Color | HP |
|-----|-------|----|
| 1 | Red | 2 |
| 2 | Pink | 2 |
| 3 | Orange | 2 |
| 4 | Yellow | 1 |
| 5 | Neon green | 1 |
| 6 | Neon blue | 1 |

---

## Configuration

All tunable values live in `settings.py`:

```python
SCREEN_W, SCREEN_H  = 800, 600
FPS                 = 60
BALL_SPEED          = 5
SPEED_UP_EVERY      = 5       # speed up every N bricks destroyed
SPEED_INCREMENT     = 0.3     # velocity added each time
STARTING_LIVES      = 3
BRICK_ROWS          = 6
BRICK_COLS          = 10
```

---

## File overview

| File | Responsibility |
|------|---------------|
| `main.py` | Bootstraps the game — just 3 lines |
| `settings.py` | Single source of truth for all constants |
| `ball.py` | Position, velocity, wall/ceiling bounce, speed scaling |
| `brick.py` | HP logic, darkening on hit, dot indicators, grid factory |
| `paddle.py` | Movement, clamping, re-centering on life loss |
| `game.py` | State machine, event loop, HUD, overlay screens, collision |

---

## Future improvements

### 🔋 Power-ups
Drop collectible power-ups when certain bricks break — ideas:
- **Wide paddle** — temporarily expands `PADDLE_W`
- **Multi-ball** — spawns 2 extra balls simultaneously
- **Slow-mo** — reduces `current_speed` for a few seconds
- **Laser** — paddle fires projectiles that destroy bricks directly

Implementation hint: add a `PowerUp` class with a type enum, spawn on brick destroy with some probability, and check collision with the paddle in `game.py`.

### 🏆 High score / leaderboard
- Persist the top score to a local file (e.g. `scores.json`) between sessions
- Show a leaderboard overlay on the win/game-over screen
- Optionally accept a player name at game start

### 🎵 Sound effects & music
pygame has a built-in mixer — add sounds for:
- Ball hitting a brick (`pygame.mixer.Sound`)
- Ball hitting the paddle
- Life lost / game over
- Background loop music (`pygame.mixer.music.load`)

All audio paths can be constants in `settings.py`.

### 🗺️ Multiple levels / stage progression
- After clearing all bricks, load the next level instead of showing the win screen
- Each level can increase `BRICK_ROWS`, add more 2-HP bricks, or introduce 3-HP bricks
- `ROW_CONFIG` in `settings.py` can be extended to a list-of-levels structure
- Track current level in `Game` state and display it in the HUD

---

## Requirements

- Python 3.x
- pygame (`pip install pygame`)

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push to GitHub
6. Open a Pull Request

---

## ⭐ Support

If you enjoyed this project, consider starring the repository.

It helps others discover the project and motivates future improvements.

---
