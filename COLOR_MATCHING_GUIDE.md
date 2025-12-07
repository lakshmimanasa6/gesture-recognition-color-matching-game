# Color Matching Gesture Game - Updated Guide

## What's New - Color Matching Mechanics!

Your gesture game now features **COLOR MATCHING** instead of sequential connections. This is much more intuitive and fun!

### Game Objective
**Match pairs of the same color by connecting them with a gesture line!**

## How to Play

### Step-by-Step Instructions

1. **Start the Game**
   ```bash
   cd /Users/manasa/gesture_game
   python3.11 game.py
   ```

2. **Understand the Board**
   - You'll see colored circles (balls) on the screen
   - Each color appears **exactly twice** (forming pairs)
   - Your job: Connect matching colors together

3. **Make a Match**
   - **Move your hand** to hover over a colored ball
   - When you get **close enough**, the ball gets **selected** (white highlight)
   - **Move your hand to another ball of the SAME COLOR**
   - When you hover over the matching color, they automatically **connect!**
   - A colored **line appears** connecting the two matched balls

4. **Complete the Level**
   - Match all the ball pairs to complete the level
   - Progress to the next level with more balls
   - Score points for each successful match

## Scoring System

| Action | Points |
|--------|--------|
| First correct match | 200 points |
| Second match (2x combo) | 400 points |
| Third match (3x combo) | 600 points |
| Wrong color match | Combo resets to 0 |
| Level complete bonus | 500 × level |

**Example**: If you're on a 3x combo and match correctly, you get 200 × 3 = **600 points**!

## Combo System

- **Combo increases** with each successful same-color match
- **Combo resets** if you try to match two balls of different colors
- **Higher combo = higher points per match**

## Game Controls

| Key | Action |
|-----|--------|
| **Hand Movement** | Move to select and connect balls |
| **H** | Toggle help text |
| **F** | Toggle FPS counter |
| **R** | Reset game to Level 1 |
| **Q** or **ESC** | Quit game |

## Game Difficulty Progression

| Level | Pairs | Difficulty |
|-------|-------|------------|
| 1 | 3 pairs (6 balls) | Easy - learn the mechanics |
| 2 | 4 pairs (8 balls) | Getting harder |
| 3 | 5 pairs (10 balls) | Medium challenge |
| 4+ | Increases by 1 pair per level | Very challenging |

## Tips for Success

### Hand Gesture Tips
✓ **Keep your hand clearly visible** in the camera
✓ **Move slowly** - jerky movements reduce detection accuracy
✓ **Use your index finger** - it's most reliably detected
✓ **Good lighting** is essential for hand detection
✓ **Keep hand 30-60cm** away from camera (about arm's length)

### Gameplay Tips
✓ **Plan your approach** - look at ball positions before starting
✓ **Maintain your combo** - each correct match gets you more points
✓ **Match similar colored pairs quickly** - they're easier to spot
✓ **Use steady hand movements** - don't jitter or move too fast

### Strategy
✓ Start with balls that are far apart - easier to track
✓ Match the most obvious color pairs first
✓ Once you get the hang of it, try to keep your combo going
✓ Try to complete levels quickly to move up

## Visual Guide

### On Screen You'll See:

```
┌─────────────────────────────────────────────┐
│ Score: 1200      FPS: 25.3                  │
│ Level: 2                                     │
│ Pairs: 2/4                                   │
│ Combo: 2x                                    │
│                                              │
│      ⚪ (Blue)                              │
│           \                                  │
│            ──── (line when matched)         │
│                                              │
│      ⚪ (Blue)                              │
│                                              │
│   ⭕ (Green - selected, white border)       │
│                                              │
│   ⚪ (Red)                                  │
│                                              │
│   ⚪ (Yellow)                                │
│                                              │
│ Match same colors | H: Help | Q: Quit | R   │
└─────────────────────────────────────────────┘
```

## Understanding the Visual Feedback

**Colored Circles**: Unmatched balls waiting to be paired
**White Border**: Currently selected/hovering ball
**Yellow Cursor Line**: Line being drawn from first ball to your hand
**Solid Color Line**: Matched pair connection

## Troubleshooting

### Problem: "Hand not being detected"
**Solution**: 
- Ensure good lighting (bright room or natural light)
- Keep hand fully visible in camera frame
- Reduce distance confidence in gesture_detector.py

### Problem: "Balls too small to click"
**Solution**: 
In `game_manager.py`, increase ball size:
```python
self.ball_radius = 35  # Default is 25
```

### Problem: "Too hard to make connections"
**Solution**:
In `game_manager.py`, increase selection distance:
```python
self.selection_distance = 70  # Default is 50
```

### Problem: "Game runs slow"
**Solution**:
- Close other applications
- Reduce number of initial balls in `game_manager.py`:
```python
self.max_balls = 4 + self.level * 1  # Instead of 6 + self.level * 2
```

## Advanced Customization

### Easy Mode (for learning)
Edit `game_manager.py`:
```python
self.ball_radius = 35           # Larger balls
self.selection_distance = 80    # Easier to select
self.max_balls = 4 + self.level # Fewer balls
```

### Hard Mode (for experts)
Edit `game_manager.py`:
```python
self.ball_radius = 15           # Tiny balls
self.selection_distance = 30    # Harder to select
self.max_balls = 8 + self.level * 3  # Many more balls
```

### Change Colors
Edit `game_manager.py` in `generate_balls()` method:
```python
colors = [
    (255, 0, 0),    # Change these RGB values
    (0, 255, 0),    # Each color appears twice
    # Add more colors...
]
```

## Performance Tips

**For Better FPS:**
- Use Python 3.11 (has better MediaPipe support)
- Close other applications
- Ensure adequate lighting (better detection = better performance)
- Update your graphics drivers

**Recommended System Requirements:**
- Modern CPU (M1/M2 Mac, or Intel i5+)
- Minimum 4GB RAM
- USB 2.0+ webcam

## Game Statistics

The game tracks:
- **Score**: Total points earned
- **Level**: Current difficulty level
- **Combo**: Current multiplication factor
- **Matched Pairs**: Progress on current level
- **FPS**: Frames per second (performance metric)

## Getting Better

**Beginner Phase (Levels 1-3)**
- Learn hand detection sensitivity
- Practice smooth hand movements
- Focus on understanding game mechanics

**Intermediate Phase (Levels 4-6)**
- Start maintaining combos
- Look for patterns in color layout
- Increase speed of movements

**Advanced Phase (Levels 7+)**
- Maximize combos for high scores
- Plan ahead for optimal matching order
- Challenge yourself with harder difficulty

## FAQ

**Q: Why isn't my hand being detected?**
A: Ensure you have good lighting and your hand is fully in frame. The detection works best with well-lit environments.

**Q: Can I use both hands?**
A: Currently, the game detects both hands but uses one primary hand for cursor control. You could extend it to use both hands simultaneously.

**Q: What if I accidentally click the wrong color?**
A: Your combo resets to 0, but you can immediately start building it back up with the next correct match.

**Q: How do I get a better score?**
A: Maintain high combos by consistently matching correct colors. Each higher combo multiplier increases your points significantly.

**Q: Can I play on Windows/Linux?**
A: Yes! The code is platform-independent. Install Python 3.11+ and the required packages.

## Version History

**v2.0 - Color Matching Update**
- Changed from sequential numbered connections to color matching pairs
- Added line drawing visualization
- Improved gesture feedback
- New combo system based on correct matches
- Better visual feedback for selected balls

---

**Ready to play? Run: `python3.11 /Users/manasa/gesture_game/game.py`**

Have fun matching colors! 🎮✨
