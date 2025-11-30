# 🎮 Nokia Snake Game - Demo & Preview

## 🎬 Game Preview

### Dual Window Interface

The game runs with two synchronized windows:

1. **Game Window (Left)** - Classic Nokia Snake gameplay
   - Green monochrome Nokia-style graphics
   - Grid-based snake movement
   - Score display in top-left
   - Particle effects when eating fruit
   - Snake with animated eyes

2. **Gesture Window (Right)** - Live webcam feed
   - Real-time hand tracking with landmarks
   - Face detection box
   - Current direction indicator
   - Boost status display
   - Visual feedback for gestures

## 🖼️ Visual Elements

### Game Screen Features
```
┌─────────────────────────┐
│ Score: 50        [Game] │
│                         │
│    ████                 │
│    ████  ●              │
│    ████                 │
│    ████                 │
│                         │
│         🍎              │
│                         │
│                         │
└─────────────────────────┘
```

### Gesture Window Features
```
┌─────────────────────────┐
│ Direction: RIGHT [Cam]  │
│ BOOST!                  │
│                         │
│   ┌─────────┐           │
│   │ Face    │           │
│   │Detected │           │
│   └─────────┘           │
│                         │
│      👋 Hand            │
│     Landmarks           │
└─────────────────────────┘
```

## 🎯 Gameplay Demonstration

### Starting the Game
1. Run `python main.py`
2. Two windows appear
3. Snake starts in center moving right
4. Show hand to webcam

### Basic Movement
```
Swipe RIGHT → Snake moves right →→→
Swipe UP    → Snake moves up    ↑↑↑
Swipe LEFT  → Snake moves left  ←←←
Swipe DOWN  → Snake moves down  ↓↓↓
```

### Eating Fruit
```
Before:          After:
████ → 🍎       ████████ 
                Score: +10
                ✨ Particles!
```

### Speed Boost
```
Normal Speed:    Boost Speed:
████ →          ████ →→→
(8 FPS)         (15 FPS)
                Pinch detected!
```

### Game Over
```
┌─────────────────────────┐
│                         │
│      GAME OVER          │
│      Score: 120         │
│                         │
│  Show UP gesture to     │
│      restart            │
│                         │
└─────────────────────────┘
```

## 🎨 Color Scheme (Nokia Style)

- **Background**: Dark Green `(48, 98, 48)`
- **Snake Body**: Nokia Green `(155, 188, 15)`
- **Snake Head**: Light Green `(204, 255, 51)`
- **Fruit**: Red `(255, 0, 0)`
- **Grid Lines**: Black `(0, 0, 0)`
- **Particles**: Yellow `(255, 255, 0)`

## 🎭 Gesture Recognition Demo

### Hand Tracking
```
     Index
       ●
      /|\
     / | \
Thumb●-●-●-● Pinky
    |  |  |
    ●  ●  ●
    Wrist
```

### Gesture Detection Flow
```
1. Camera captures frame
2. MediaPipe detects hand landmarks
3. Calculate hand movement
4. Determine gesture direction
5. Send to game controller
6. Snake responds immediately
```

## 📊 Performance Metrics

- **Game FPS**: 60 (display)
- **Snake Speed**: 8-15 (game logic)
- **Gesture Detection**: Real-time (~30 FPS)
- **Latency**: <50ms gesture to action
- **Hand Tracking**: 21 landmarks per hand

## 🎪 Special Effects

### Particle System
When snake eats fruit:
- 10 particles spawn
- Yellow color with fade
- Random velocity vectors
- 20-frame lifetime
- Smooth animation

### Snake Eyes
- Eyes follow movement direction
- 3-pixel circles
- Black color on light green head
- Position changes with direction

## 🎬 Typical Game Session

```
1. Start Game
   ↓
2. Position hand in camera
   ↓
3. Swipe to control snake
   ↓
4. Eat fruits, grow snake
   ↓
5. Use pinch for boost
   ↓
6. Avoid walls & self
   ↓
7. Game Over → Show UP to restart
```

## 🔧 Technical Preview

### Architecture
```
Main Thread              Gesture Thread
    |                         |
    ├─ Game Loop             ├─ Camera Capture
    ├─ Update Logic          ├─ Hand Detection
    ├─ Collision Check       ├─ Gesture Analysis
    ├─ Render Graphics       ├─ Face Detection
    └─ Display Frame         └─ Visual Feedback
         ↑                        ↓
         └────── Gesture Data ────┘
```

### Data Flow
```
Webcam → OpenCV → MediaPipe → Gesture Controller
                                      ↓
                              Gesture + Boost
                                      ↓
                              Game Controller
                                      ↓
                              Snake Game Logic
                                      ↓
                              Pygame Display
```

## 🎯 Key Features in Action

✅ **Real-time gesture recognition** - Instant response  
✅ **Smooth animations** - 60 FPS display  
✅ **Visual feedback** - See your hand tracking  
✅ **Particle effects** - Satisfying fruit collection  
✅ **Speed boost** - Pinch for faster gameplay  
✅ **Face detection** - Know you're in frame  
✅ **Score tracking** - Competitive gameplay  
✅ **Easy restart** - UP gesture to play again  

## 🎮 Try It Yourself!

```bash
git clone https://github.com/sricharanreddynyayam-crypto/nokia-snake-gesture-control.git
cd nokia-snake-gesture-control
python setup.py
python main.py
```

**Experience the nostalgia of Nokia Snake with the magic of AI! 🐍✨**