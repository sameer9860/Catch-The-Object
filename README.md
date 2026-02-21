# � Catch the Falling Objects

> A fun, fast-paced arcade game built with **Python** and **Pygame** — catch falling apples, grab power-ups, and dodge bombs to survive as long as you can!

![Game Over Screen](gameover.png)

---

## ✨ Features

| Feature                       | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| 🏆 **High Score Tracking**    | Your best score is automatically saved to `highscore.txt` |
| 📈 **Progressive Difficulty** | Game speeds up every 20 points — how far can you go?      |
| 🌄 **5 Dynamic Backgrounds**  | New environments unlock as you advance through levels     |
| 🎵 **Sound Effects & Music**  | Catch sounds, explosions, and a looping background track  |
| 💥 **Particle Effects**       | Satisfying burst animations on every catch and hit        |
| 🔀 **Screen Shake**           | Dramatic camera shake when a bomb hits you                |
| 🔢 **Combo Multiplier**       | Chain catches to multiply your score                      |

---

## 🕹️ How to Play

### 🎮 Controls

| Key             | Action                    |
| --------------- | ------------------------- |
| `← Left Arrow`  | Move basket left          |
| `→ Right Arrow` | Move basket right         |
| `Space`         | Start game (from menu)    |
| `R`             | Restart (after Game Over) |
| `Q` / `Esc`     | Quit game                 |

### 🎯 Objective

- **Catch** falling objects with your basket to earn points.
- **Avoid bombs** — each one costs you a life.
- You start with **3 lives**. Lose them all and the game ends.
- Keep catching without missing to build a **combo multiplier**!

---

## 💎 Objects & Power-Ups

| Object              | Type     | Effect                                    |
| ------------------- | -------- | ----------------------------------------- |
| 🍎 **Apple**        | Good     | +1 point                                  |
| ✨ **Golden Apple** | Power-Up | +3 points & activates **Double Points**   |
| ❤️ **Heart**        | Power-Up | Grants **+1 extra life** (max 7)          |
| ⭐ **Magic Star**   | Power-Up | Activates **Wide Basket** for ~10 seconds |
| 💣 **Bomb**         | Bad      | -1 life + screen shake                    |

> **Pro tip:** Chain catches without missing to build your combo multiplier — every 3 consecutive catches adds another ×1 to your score!

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.x
- Pygame library

### Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sameer9860/Catch-The-Object.git
   cd Catch-The-Object
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**

   ```bash
   python catch-the-object.py
   ```

---

## � Project Structure

```
Catch-The-Object/
├── catch-the-object.py   # Main game source
├── requirements.txt      # Python dependencies
├── highscore.txt         # Persisted high score
├── apple.png             # Apple sprite
├── bomb.png              # Bomb sprite
├── basket.png            # Basket sprite
├── gameover.png          # Game over image
├── bg1.png – bg5.png     # Level backgrounds
├── catch.wav             # Catch sound effect
├── explosion.wav         # Explosion sound effect
└── background.mp3        # Background music
```

---

## �📜 License

This project is open-source and free to use. Feel free to play, modify, and share — enjoy catching! 🎉
