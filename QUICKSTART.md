# Quick Start Guide - Gesture Recognition Color Connecting Game

## Installation & Setup

### 1. Prerequisites
- macOS with M1/M2/M3 chip (ARM64) or Intel Mac
- Webcam
- Python 3.11 (required for MediaPipe support on macOS)

### 2. Install Dependencies

Navigate to the project directory and install packages:

```bash
cd /Users/manasa/gesture_game
python3.11 -m pip install -r requirements.txt
```

Or install packages individually:
```bash
python3.11 -m pip install opencv-python mediapipe numpy
```

### 3. Run the Game

**Option A: Direct Python**
```bash
cd /Users/manasa/gesture_game
python3.11 game.py
```

**Option B: Using the launcher script**
```bash
cd /Users/manasa/gesture_game
chmod +x run_game.sh
./run_game.sh
```

## Game Controls

| Key | Action |
|-----|--------|
| **Hand/Fingertip Movement** | Move cursor to select and connect balls |
| **H** | Toggle help text on/off |
| **F** | Toggle FPS display |
| **R** | Reset game to level 1 |
| **Q** or **ESC** | Quit game |

## How to Play

1. **Objective**: Connect all colored balls in numerical order (0 → 1 → 2 → ... → n)

2. **Connection Mechanics**:
   - Move your index finger (or hand) near a ball to connect it
   - The ball must be connected in the correct numerical sequence
   - You cannot skip numbers - always connect the next ball in order

3. **Scoring**:
   - **Correct Connection**: 100 points × current combo multiplier
   - **Level Complete**: 1000 points × current level
   - Example: If you're on a 3x combo, each correct connection = 300 points

4. **Combo System**:
   - Correctly connecting consecutive balls increases your combo multiplier
   - Breaking the sequence resets the combo to 0
   - Higher combos = higher score per connection

5. **Difficulty Progression**:
   - **Level 1**: 5 balls
   - **Level 2**: 7 balls
   - **Level 3**: 9 balls
   - And so on... (+2 balls per level)

6. **Level Completion**:
   - After connecting all balls in sequence, you advance to the next level
   - Game resets with more balls
   - Difficulty increases with each level

## Gameplay Tips

### For Better Hand Detection
- **Lighting**: Ensure good lighting on your hand
- **Distance**: Keep your hand 30-60cm from the camera
- **Visibility**: Keep hand clearly in frame
- **Speed**: Move hand smoothly, not too fast

### To Improve Your Score
1. **Plan ahead**: Look at the ball positions before starting
2. **Steady movements**: Slow, deliberate movements work better than fast jerky ones
3. **Maintain combos**: Try to keep your combo multiplier high
4. **Watch the sequence**: Always connect 0 → 1 → 2 → n in order

## Troubleshooting

### Camera Issues
**Problem**: Camera not opening or "Failed to read frame"
```bash
# Check if camera is in use by other applications
lsof | grep camera

# Try changing camera index in game.py:
# Change: self.cap = cv2.VideoCapture(0)
# To:     self.cap = cv2.VideoCapture(1) or cv2.VideoCapture(2)
```

### Poor Hand Detection
**Problem**: Hand landmarks not detected
- Improve lighting (natural light is best)
- Position hand clearly in view
- Adjust detection confidence in `gesture_detector.py`:
  ```python
  min_detection_confidence=0.5  # Lower = more detections
  min_tracking_confidence=0.3    # Lower = smoother tracking
  ```

### Performance Issues
**Problem**: Game runs slowly (low FPS)
- Close other applications
- Reduce ball count temporarily:
  - Edit `game_manager.py` line in `__init__`:
  - Change: `self.max_balls = 5 + self.level * 2`
  - To: `self.max_balls = 3 + self.level * 1`

### Import Errors
**Problem**: "Import mediapipe could not be resolved"
- Make sure you're using Python 3.11:
  ```bash
  python3.11 -m pip list | grep -i mediapipe
  ```
- Reinstall if needed:
  ```bash
  python3.11 -m pip install --force-reinstall mediapipe
  ```

## Project Structure

```
gesture_game/
├── game.py                 # Main game loop and rendering
├── gesture_detector.py     # Hand detection with MediaPipe
├── game_manager.py         # Game state and scoring
├── utils.py               # Helper functions
├── requirements.txt       # Python dependencies
├── run_game.sh           # Launcher script
├── README.md             # Full documentation
└── QUICKSTART.md         # This file
```

## Advanced Customization

### Change Game Difficulty

Edit `game_manager.py`:
```python
# Increase difficulty more aggressively
self.max_balls = 8 + self.level * 3  # More balls per level

# Make connections harder to achieve
self.connection_distance = 40  # Smaller = harder to connect

# Adjust scoring
self.score += 50 * self.combo  # Less points per connection
```

### Adjust Hand Detection

Edit `gesture_detector.py`:
```python
self.hands = self.mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,  # 0-1, lower = more detections
    min_tracking_confidence=0.3    # 0-1, lower = smoother tracking
)
```

### Change Ball Colors

Edit `game_manager.py` in `generate_balls()` method:
```python
colors = [
    (255, 0, 0),    # Blue (BGR format!)
    (0, 255, 0),    # Green
    (0, 0, 255),    # Red
    # Add more colors as needed
]
```

### Modify UI Elements

Edit `game.py` in `_draw_ui()` method to change:
- Score position and size
- Level display
- Combo counter
- Help text location

## Performance Expectations

On a modern Mac (M1/M2/M3):
- **FPS**: 20-30 FPS (depends on hand detection)
- **Latency**: 50-100ms hand-to-cursor response
- **CPU Usage**: 15-25% during gameplay

On Intel Mac:
- **FPS**: 15-25 FPS
- **Latency**: 100-150ms
- **CPU Usage**: 25-40%

## FAQ

**Q: Can I use both hands to play?**
A: The game supports detecting both hands, but the cursor is controlled by one primary hand. You could extend it to support dual-hand gameplay.

**Q: What if my hand is partially out of frame?**
A: Hand detection works best when the entire hand is visible. Keep your hand fully in the camera view.

**Q: Can I play on Windows/Linux?**
A: Yes! The code is platform-independent. Just ensure you have Python 3.9+ and can install the required packages.

**Q: How do I record my gameplay?**
A: You can use screen recording tools like QuickTime (Cmd+Shift+5) on macOS.

## Next Steps

1. **Run the game**: `python3.11 game.py`
2. **Practice a few levels** to get comfortable with hand movements
3. **Customize difficulty** if needed
4. **Share your high score!**

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review the Troubleshooting section above
3. Check that you're using Python 3.11
4. Verify all dependencies are installed: `python3.11 -m pip list`

---

**Happy Gaming! 🎮✨**
