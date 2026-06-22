# 🧱 Brick Breaker Game

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-22c55e?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.2-FF8C00?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)

> A classic brick-breaker rebuilt in Python and pygame — neon dark-theme aesthetic, 2-HP brick system, dynamic speed scaling, angle-based paddle physics, full sound feedback, and a particle engine for visual polish.

---

## 📸 Preview

<p align="center">
  <img src="screenshots/V1.0.png" alt="Brick Breaker Gameplay" width="800"/>
</p>

---

## 🆕 What's New in V1.2

> V1.2 is the **visual polish update** — every major game interaction now has particle feedback, and the codebase was fully refactored for maintainability.

| # | Feature | Details |
|---|---|---|
| ✨ | **Ball Trail Particles** | Motion trail behind the ball as it moves |
| ✨ | **Paddle Spark Particles** | Small sparks burst on every paddle collision |
| 💥 | **Brick Explosion Particles** | Burst effect when bricks are hit or destroyed |
| 🔧 | **Standardized Constants** | All variable names unified across the codebase |
| 🛠️ | **Fixed Import Errors** | Resolved `WIDTH`, `BRICK_W`, `SCREEN_W`, `PADDLE_W` conflicts |
| 🔁 | **Rebuilt Collision System** | `check_brick_collision()` restored and stabilized |

---

## 📋 Version History

| Version | Highlights |
|---|---|
| **V1.0** | Base game — 2-HP bricks, speed scaling, angle physics, neon UI, HUD, state machine |
| **V1.1** | 🔊 Sound system — `pygame.mixer` integration, 4 `.wav` files (paddle, brick, lose, win) |
| **V1.2** | ✨ Particle engine — ball trail, paddle sparks, brick explosions + full constants refactor |

---

## ✨ Full Feature Set

| Feature | Description |
|---|---|
| ✨ **Particle Engine** | Ball trail, paddle sparks, and brick explosion effects |
| 🟥 **2-HP Brick System** | Top 3 rows take 2 hits — darken on first hit, show dot HP indicators |
| 💥 **1-HP Bricks** | Bottom 3 rows shatter in a single hit |
| ⚡ **Dynamic Speed Scaling** | Ball speeds up every 5 destroyed bricks |
| 🎮 **Angle Physics** | Paddle hit offset influences ball bounce angle |
| 🏆 **Scoring System** | +10 for destroyed bricks, +5 for hitting a 2-HP brick |
| ❤️ **3 Lives** | Ball falling below screen costs one life |
| 🎨 **Neon Dark UI** | Dark grid background, neon-colored bricks with shine strips |
| 📊 **Live HUD** | Score, lives (❤ symbols), and current ball speed |
| 🔊 **Sound Feedback** | Sounds on paddle hit, brick destroy, life lost, and win |
| 🪟 **State Machine** | Clean `playing → lost_life → game_over / won` transitions with overlays |

---

## 🗂️ Project Structure

```
brick-breaker-game/
│
├── main.py              # 🚀 Entry point — 2 lines, just runs Game()
├── settings.py          # ⚙️  Single source of truth for all constants & config
├── requirements.txt     # 📦 Python dependencies
├── .gitignore
├── README.md
├── LICENSE
│
├── game/
│   ├── __init__.py
│   ├── game.py          # 🧠 Game loop, state machine, HUD, overlays, collision
│   ├── ball.py          # ⚽ Position, velocity, wall bounce, speed scaling, trail particles
│   ├── paddle.py        # 🏓 Movement, clamping, re-center on life loss, spark particles
│   └── brick.py         # 🧱 HP logic, darkening, dot indicators, explosion particles
│
├── sounds/
│   ├── paddle.wav        # 🔊 Paddle hit
│   ├── brick.wav         # 💥 Brick destroyed
│   ├── lose.wav          # ❌ Life lost / game over
│   └── win.wav           # 🎉 Stage clear
│
├── screenshots/
│   └── V1.0.png
│
└── assets/               # 🔮 Future — power-ups, boss sprites
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core game logic |
| **Game Engine** | [pygame](https://www.pygame.org/) | Rendering, event loop, input, audio |
| **Particles** | Custom particle system | Trail, spark, and explosion effects |
| **Audio** | `pygame.mixer.Sound` | `.wav` playback for all game events |
| **Config** | `settings.py` | All constants unified — no magic numbers |

---

## 🔧 V1.2 Refactor — Constants Renamed

All variable names were standardized in `settings.py` and updated across every file:

| Old Name | New Name |
|---|---|
| `SCREEN_W` | `WIDTH` |
| `SCREEN_H` | `HEIGHT` |
| `PADDLE_W` | `PADDLE_WIDTH` |
| `PADDLE_H` | `PADDLE_HEIGHT` |
| `BALL_R` | `BALL_RADIUS` |
| `BRICK_W` | `BRICK_WIDTH` |
| `BRICK_H` | `BRICK_HEIGHT` |

This resolved all import conflicts and makes the codebase consistent for future features.

---

## 🎮 Controls

| Key | Action |
|---|---|
| `← / A` | Move paddle left |
| `→ / D` | Move paddle right |
| `SPACE` | Launch ball / continue after life loss |
| `R` | Restart after win or game over |
| `ESC` | Quit |

---

## 🧱 Brick Grid

**6 rows × 10 columns = 60 bricks**

| Row | Color | HP | Behavior |
|---|---|---|---|
| 1 | 🔴 Red | 2 | Darkens on first hit, dot indicator, explosion particles |
| 2 | 🩷 Pink | 2 | Darkens on first hit, dot indicator, explosion particles |
| 3 | 🟠 Orange | 2 | Darkens on first hit, dot indicator, explosion particles |
| 4 | 🟡 Yellow | 1 | Shatters in one hit, explosion particles |
| 5 | 🟢 Neon Green | 1 | Shatters in one hit, explosion particles |
| 6 | 🔵 Neon Blue | 1 | Shatters in one hit, explosion particles |

---

## 🏆 Scoring

| Event | Points |
|---|---|
| Brick destroyed | +10 |
| 2-HP brick hit but not destroyed | +5 |

---

## ⚙️ Configuration — `settings.py`

```python
WIDTH, HEIGHT       = 800, 600
FPS                 = 60
BALL_SPEED          = 5
SPEED_UP_EVERY      = 5       # speed up every N bricks destroyed
SPEED_INCREMENT     = 0.3     # velocity added each time
STARTING_LIVES      = 3
BRICK_ROWS          = 6
BRICK_COLS          = 10
PADDLE_WIDTH        = 110
PADDLE_SPEED        = 7
```

---

## 🧠 Technical Highlights

### Angle-Based Paddle Physics
```python
# ball.py — bounce_paddle()
offset  = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
self.vx = offset * self.current_speed * 1.2
```
Hitting the paddle edge sends the ball at a steeper angle. Center hits bounce more vertically.

### Direction-Preserved Speed Scaling
```python
# ball.py — increase_speed()
mag = math.hypot(self.vx, self.vy)
self.vx = (self.vx / mag) * self.current_speed
self.vy = (self.vy / mag) * self.current_speed
```
Direction is preserved while velocity magnitude is scaled — no direction drift on speed-up.

### Overlap-Based Collision Response
```python
# game.py — check_brick_collision()
if overlap_x < overlap_y:
    ball.vx *= -1   # side hit → reverse horizontal
else:
    ball.vy *= -1   # top/bottom hit → reverse vertical
```
Compares overlap axes to determine the correct bounce direction, avoiding corner tunneling.

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/caffineblud/Brick-Breaker-Game.git
cd Brick-Breaker-Game
pip install -r requirements.txt
python main.py
```

---

## 🔮 Planned for V1.3+

- [ ] ⚡ Power-ups (wide paddle, multi-ball, slow-mo, laser)
- [ ] 🏆 High score persistence (`scores.json`)
- [ ] 🗺️ Multiple levels with increasing difficulty
- [ ] 👾 Boss brick / special stages

---

## 👨‍💻 Author

**Yash Kumar Singh**

[![GitHub](https://img.shields.io/badge/GitHub-caffineblud-181717?style=flat-square&logo=github)](https://github.com/caffineblud)

⭐ If you like this project, consider giving it a star.