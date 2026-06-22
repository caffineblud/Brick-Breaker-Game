# 🧱 Brick Breaker Game

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-22c55e?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.1-FF8C00?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)

> A classic brick-breaker rebuilt from scratch in Python and pygame — neon dark-theme aesthetic, 2-HP brick system, dynamic speed scaling, angle-based paddle physics, and full sound feedback.

---

## 📸 Preview

<p align="center">
  <img src="screenshots/V1.0.png" alt="Brick Breaker Gameplay" width="800"/>
</p>

---

## 🆕 What's New in V1.1

| # | Feature | Details |
|---|---|---|
| 🔊 | **Sound Effects** | Four `.wav` sounds — paddle hit, brick destroy, life lost, win |
| 🎵 | **pygame.mixer integration** | All audio loaded via `pygame.mixer.Sound`, played on game events |
| 📁 | **`sounds/` folder** | Dedicated audio directory (`paddle.wav`, `brick.wav`, `lose.wav`, `win.wav`) |
| 🗂️ | **`assets/` directory** | Placeholder for future power-ups, particles, and boss sprites |

---

## ✨ Full Feature Set

| Feature | Description |
|---|---|
| 🟥 **2-HP Brick System** | Top 3 rows take 2 hits — darken on first hit, show dot HP indicators |
| 💥 **1-HP Bricks** | Bottom 3 rows shatter in a single hit |
| ⚡ **Dynamic Speed Scaling** | Ball speeds up every 5 destroyed bricks (`SPEED_UP_EVERY`, `SPEED_INCREMENT`) |
| 🎮 **Angle Physics** | Paddle hit offset influences ball bounce angle — not just flat reflection |
| 🏆 **Scoring System** | +10 for destroyed bricks, +5 for hitting a 2-HP brick without destroying it |
| ❤️ **3 Lives** | Ball falling below screen costs one life — game over at zero |
| 🎨 **Neon Dark UI** | Dark grid background (`DARK_BG`), neon-colored bricks with shine strips |
| 📊 **Live HUD** | Score, lives (❤ symbols), and current ball speed shown during play |
| 🪟 **State Machine** | Clean `playing → lost_life → game_over / won` state transitions with overlays |
| 🔊 **Sound Feedback** | Sounds on paddle hit, brick destroy, life lost, and win |

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
│   ├── ball.py          # ⚽ Position, velocity, wall bounce, speed scaling
│   ├── paddle.py        # 🏓 Movement, screen clamping, re-center on life loss
│   └── brick.py         # 🧱 HP logic, darkening, dot indicators, grid factory
│
├── sounds/
│   ├── paddle.wav        # 🔊 Plays on paddle hit
│   ├── brick.wav         # 💥 Plays on brick destroyed
│   ├── lose.wav          # ❌ Plays on life lost / game over
│   └── win.wav           # 🎉 Plays on stage clear
│
├── screenshots/
│   └── V1.0.png
│
└── assets/               # 🔮 Future — power-ups, particles, boss sprites
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core game logic |
| **Game Engine** | [pygame](https://www.pygame.org/) | Rendering, event loop, input, audio |
| **Audio** | `pygame.mixer.Sound` | `.wav` playback for all game events |
| **Config** | `settings.py` | All constants in one place — no magic numbers |

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
| 1 | 🔴 Red | 2 | Darkens on first hit, dot indicator |
| 2 | 🩷 Pink | 2 | Darkens on first hit, dot indicator |
| 3 | 🟠 Orange | 2 | Darkens on first hit, dot indicator |
| 4 | 🟡 Yellow | 1 | Shatters in one hit |
| 5 | 🟢 Neon Green | 1 | Shatters in one hit |
| 6 | 🔵 Neon Blue | 1 | Shatters in one hit |

---

## 🏆 Scoring

| Event | Points |
|---|---|
| Brick destroyed (any HP) | +10 |
| 2-HP brick hit but not destroyed | +5 |

---

## ⚙️ Configuration — `settings.py`

All game tuning lives in a single file. No magic numbers anywhere else.

```python
SCREEN_W, SCREEN_H  = 800, 600
FPS                 = 60
BALL_SPEED          = 5
SPEED_UP_EVERY      = 5       # speed up every N bricks destroyed
SPEED_INCREMENT     = 0.3     # velocity added each time
STARTING_LIVES      = 3
BRICK_ROWS          = 6
BRICK_COLS          = 10
PADDLE_W            = 110
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

### Dynamic Speed Scaling
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

`requirements.txt` contains:
```
pygame
numpy
```

---

## 🔮 Planned for V1.2+

- [ ] ⚡ Power-ups (wide paddle, multi-ball, slow-mo, laser)
- [ ] 🏆 High score persistence (`scores.json`)
- [ ] 🗺️ Multiple levels with increasing difficulty
- [ ] 🎨 Particle effects on brick destroy
- [ ] 👾 Boss brick / special stages

---

## 👨‍💻 Author

**Yash Kumar Singh**

[![GitHub](https://img.shields.io/badge/GitHub-caffineblud-181717?style=flat-square&logo=github)](https://github.com/caffineblud)

⭐ If you like this project, consider giving it a star.