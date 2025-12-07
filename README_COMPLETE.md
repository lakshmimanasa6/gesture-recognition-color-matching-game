# 🎮 Gesture Recognition Color Matching Game

A real-time interactive game that uses **hand gesture recognition to match colored ball pairs**. Built with MediaPipe for hand detection and OpenCV for live video processing.

## ✨ Features

- **Real-time Hand Detection**: Uses MediaPipe to track hand positions and gestures
- **Color Pair Matching**: Connect two balls of the same color together
- **Line Drawing**: Visual feedback shows connection lines as you gesture
- **Progressive Difficulty**: Each level adds more ball pairs
- **Combo System**: Build multipliers for consecutive correct matches
- **Score Tracking**: Earn points with combo bonuses
- **Multi-hand Support**: Detect up to 2 hands (uses primary hand for control)
- **Performance Monitoring**: Real-time FPS counter

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /Users/manasa/gesture_game
python3.11 -m pip install -r requirements.txt
```

### 2. Run the Game
```bash
python3.11 game.py
```

That's it! The game starts immediately.

## 🎯 How to Play

### Objective
**Find two balls of the same color and connect them together using hand gestures!**

### Gameplay Steps

1. **Look at the colored balls on screen**
   - Each color appears exactly **twice**
   - You need to match the pairs

2. **Move your hand near a ball**
   - It highlights with a **white border** (selected)
   - The ball is now your "first selection"

3. **Move your hand to another ball of the SAME color**
   - A **yellow line** draws from the first ball to your hand
   - This is visual feedback showing your connection attempt

4. **When you reach the matching color**
   - System detects the match ✓
   - A **solid colored line** appears between them
   - **+200 points** awarded (×combo multiplier)
   - Both balls stay connected

5. **Repeat until all pairs matched**
   - Match all the pairs to complete the level
   - Advance to next level with more balls

## 🎮 Controls

| Key/Action | Function |
|------------|----------|
| **Hand Movement** | Move hand to select and connect balls |
| **H** | Toggle help/instructions on screen |
| **F** | Toggle FPS (frames per second) display |
| **R** | Reset game to Level 1 |
| **Q** or **ESC** | Quit game |

## 📊 Scoring

| Event | Points |
|-------|--------|
| 1st correct match (1x combo) | 200 |
| 2nd correct match (2x combo) | 400 |
| 3rd correct match (3x combo) | 600 |
| Nth correct match (Nx combo) | 200 × N |
| Wrong color match | Combo resets to 0 |
| Level complete bonus | 500 × current level |

**Example**: If you have a 5x combo and match correctly:
- Points earned = 200 × 5 = **1000 points!**

## 📈 Game Difficulty

| Level | Pairs | Ball Count | Difficulty |
|-------|-------|-----------|------------|
| 1 | 3 | 6 | Easy (Learning) |
| 2 | 4 | 8 | Easy |
| 3 | 5 | 10 | Medium |
| 4 | 6 | 12 | Hard |
| 5 | 7 | 14 | Very Hard |
| n | 2+n | 4+2n | Increases with level |

## 📁 Project Structure

```
gesture_game/
├── game.py                    # Main game loop and rendering
├── gesture_detector.py        # Hand detection with MediaPipe
├── game_manager.py            # Game logic and state management
├── utils.py                   # Helper functions for drawing/math
├── requirements.txt           # Python dependencies
├── run_game.sh               # Launcher script
│
├── COLOR_MATCHING_GUIDE.md   # Detailed gameplay guide ⭐ START HERE
├── GAME_MECHANICS.txt        # Visual game mechanics explanation
├── CHANGES_SUMMARY.md        # What changed from v1.0
├── QUICK_REF.txt            # Quick reference card
├── QUICKSTART.md            # Quick start guide
└── README.md                # This file
```

## 💡 Tips for Better Gameplay

### Hand Detection Tips
✓ **Good lighting** - Natural light works best
✓ **Keep hand visible** - Hand should be fully in camera frame
✓ **Maintain distance** - 30-60cm from camera (about arm's length)
✓ **Smooth movements** - Move slowly, avoid jerky motions
✓ **Use index finger** - Clearest for gesture detection

### Gameplay Strategy
✓ **Plan ahead** - Look at ball positions before starting
✓ **Build combos** - Consecutive matches = higher score multiplier
✓ **Keep focus** - It's easy to lose track during fast gameplay
✓ **Match quickly** - Complete levels faster to reach higher levels
✓ **Maintain rhythm** - Develop a steady hand movement pattern

## ⚙️ Customization

### Easy Mode (for beginners)
Edit `game_manager.py`:
```python
self.ball_radius = 35           # Larger balls (easier to hit)
self.selection_distance = 80    # Larger selection area
self.max_balls = 4 + self.level # Start with fewer balls
```

### Hard Mode (for experts)
Edit `game_manager.py`:
```python
self.ball_radius = 15           # Tiny balls (harder)
self.selection_distance = 30    # Tiny selection area
self.max_balls = 8 + self.level * 2  # Many more balls
```

### Change Colors
Edit `game_manager.py` in `generate_balls()` method:
```python
colors = [
    (255, 0, 0),    # Blue (BGR format)
    (0, 255, 0),    # Green
    (0, 0, 255),    # Red
    # Add your colors here...
]
```

### Adjust Hand Detection Sensitivity
Edit `gesture_detector.py`:
```python
self.hands = self.mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,  # Lower = more detections
    min_tracking_confidence=0.5    # Lower = smoother tracking
)
```

## 🐛 Troubleshooting

### Problem: Hand not detected
**Solution**: Improve lighting, ensure hand is fully visible, increase detection sensitivity

### Problem: Balls too small to click
**Solution**: Increase `ball_radius` in game_manager.py (try 35-40)

### Problem: Selection range too small
**Solution**: Increase `selection_distance` in game_manager.py (try 70-80)

### Problem: Game runs slow (low FPS)
**Solution**: 
- Close other applications
- Reduce ball count: `self.max_balls = 4 + self.level`
- Lower detection: `min_detection_confidence = 0.5`

### Problem: Camera not opening
**Solution**: Check camera permissions, try different camera index (0, 1, or 2)

### Problem: Import errors with mediapipe
**Solution**: Ensure you're using Python 3.11:
```bash
python3.11 -m pip install mediapipe
```

## 📋 System Requirements

- **Python**: 3.9+ (3.11 recommended for MediaPipe)
- **Webcam**: USB or built-in
- **RAM**: 4GB minimum
- **CPU**: Dual-core processor
- **OS**: macOS, Windows, or Linux

## 🎯 Game Statistics Tracked

The game displays real-time:
- **Score**: Total points accumulated
- **Level**: Current difficulty level
- **Pairs**: Matched pairs / Total pairs (X/Y)
- **Combo**: Current multiplier (shows only when > 0)
- **FPS**: Frames per second (performance indicator)

## 🏆 Strategies for High Scores

1. **Maximize Combo Multiplier**
   - Each correct match increases combo
   - Higher combo = exponentially more points
   - Don't rush - accuracy > speed

2. **Complete Levels Quickly**
   - Each level completion gives 500 × level bonus
   - Fast gameplay = more levels = more bonuses

3. **Maintain Consistency**
   - Avoid mismatches (resets combo)
   - Build rhythm and muscle memory
   - Play multiple sessions to improve

4. **Learn Ball Positions**
   - After a few levels, recognize color patterns
   - Plan your matching sequence mentally
   - Execute efficiently

## 📝 Game Version History

### v2.0 - Color Matching (Current)
- ✓ Color pair matching (instead of sequential numbers)
- ✓ Line drawing visualization
- ✓ Real-time gesture feedback
- ✓ Improved combo system
- ✓ Better visual feedback with white borders

### v1.0 - Sequential Connections
- Sequential numbered ball connections
- No visual line feedback during gesture
- Basic combo system

## 🔗 Technical Details

### Hand Detection (MediaPipe)
- Detects 21 hand landmarks per hand
- Uses index finger tip for cursor control
- Supports up to 2 hands simultaneously
- ~30 FPS on modern hardware

### Game Loop
1. Capture frame from webcam
2. Detect hand landmarks
3. Calculate cursor position
4. Update game state
5. Check for color matches
6. Render frame with drawings
7. Display FPS and UI

### Performance
- **Target FPS**: 30 FPS
- **Typical FPS**: 20-30 FPS (depends on hardware)
- **Latency**: 50-150ms (hand to cursor response)

## 🤝 Contributing

Want to add features? Ideas:
- [ ] Sound effects and music
- [ ] Particle effects
- [ ] Different game modes (time attack, endless)
- [ ] Leaderboard system
- [ ] Gesture-based special moves
- [ ] Multiplayer support
- [ ] Mobile version

## 📞 Support

If you encounter issues:

1. **Check the guides**:
   - `COLOR_MATCHING_GUIDE.md` - Detailed instructions
   - `GAME_MECHANICS.txt` - Visual explanations
   - `QUICK_REF.txt` - Quick answers

2. **Troubleshooting**:
   - Ensure Python 3.11
   - Verify dependencies: `python3.11 -m pip list`
   - Check camera permissions
   - Improve lighting conditions

3. **Debug**:
   ```bash
   python3.11 -m py_compile game.py  # Check for syntax errors
   python3.11 -c "import cv2, mediapipe"  # Check imports
   ```

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `COLOR_MATCHING_GUIDE.md` | 📚 Complete gameplay guide |
| `GAME_MECHANICS.txt` | 🎮 Visual mechanics explanation |
| `CHANGES_SUMMARY.md` | 📝 What changed from v1 |
| `QUICK_REF.txt` | ⚡ Quick reference card |
| `QUICKSTART.md` | 🚀 Setup & quick start |

## 🎨 Color Palette

Default colors (BGR format):
- **Blue**: (255, 0, 0)
- **Green**: (0, 255, 0)
- **Red**: (0, 0, 255)
- **Cyan**: (255, 255, 0)
- **Magenta**: (255, 0, 255)
- **Yellow**: (0, 255, 255)

## 📊 Game Architecture

```
User Hand Movement
        ↓
   Hand Detection (MediaPipe)
        ↓
   Extract Landmarks
        ↓
   Calculate Cursor Position
        ↓
   Game Manager Update
        ↓
   Check Ball Proximity
        ↓
   Color Match Detection
        ↓
   Update Score & Combo
        ↓
   Render Frame
        ↓
   Display to Screen
```

## 🔐 License

Free to use and modify for educational purposes.

## 🎉 Ready to Play?

```bash
cd /Users/manasa/gesture_game
python3.11 game.py
```

**Good luck and have fun! Match those colors! 🌈✨**

---

**Last Updated**: December 7, 2025
**Version**: 2.0 - Color Matching
**Python**: 3.11+
**Status**: Ready to Play ✓
