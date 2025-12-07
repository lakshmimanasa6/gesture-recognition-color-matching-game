"""
Gesture Recognition Color Connecting Game
A real-time game that uses hand gestures to connect colored balls
"""

import cv2
import mediapipe as mp
import numpy as np
from gesture_detector import GestureDetector
from game_manager import GameManager
from utils import draw_text, draw_circle, distance_between_points

class GestureGame:
    def __init__(self):
        """Initialize the gesture recognition game"""
        self.cap = cv2.VideoCapture(0)
        self.gesture_detector = GestureDetector()
        self.game_manager = GameManager()
        
        # Game settings
        self.window_name = "Gesture Color Connection Game"
        self.is_running = True
        self.show_fps = True
        self.show_help = True
        
        # FPS calculation
        self.fps = 0
        self.frame_count = 0
        self.prev_time = 0
        
    def process_frame(self, frame):
        """Process a single frame of video"""
        # Detect hand gestures
        hand_landmarks, handedness = self.gesture_detector.detect_hands(frame)
        gesture_points = self.gesture_detector.get_gesture_points(hand_landmarks)
        
        # Update game based on detected points
        if gesture_points:
            for point, hand_id in gesture_points:
                self.game_manager.update_cursor(point, hand_id)
        
        # Draw game elements
        self._draw_game(frame, hand_landmarks)
        
        return frame
    
    def _draw_game(self, frame, hand_landmarks):
        """Draw all game elements on the frame"""
        # Draw matched pairs with lines
        for pair in self.game_manager.matched_pairs:
            ball1 = None
            ball2 = None
            for ball in self.game_manager.balls:
                if ball['id'] == pair['ball1_id']:
                    ball1 = ball
                if ball['id'] == pair['ball2_id']:
                    ball2 = ball
            
            if ball1 and ball2:
                # Draw line between matched balls
                cv2.line(frame, tuple(ball1['pos'].astype(int)), 
                        tuple(ball2['pos'].astype(int)), 
                        pair['color'], 3)
        
        # Draw all balls
        for ball in self.game_manager.balls:
            if not ball['matched']:
                # Draw unmatched ball
                color = ball['color']
                radius = ball['radius']
                
                # Highlight selected ball
                if ball['selected']:
                    cv2.circle(frame, tuple(ball['pos'].astype(int)), 
                             radius + 5, (255, 255, 255), 3)
                
                # Draw ball
                cv2.circle(frame, tuple(ball['pos'].astype(int)), 
                          radius, color, -1)
                
                # Draw ball border
                cv2.circle(frame, tuple(ball['pos'].astype(int)), 
                          radius, (255, 255, 255), 2)
        
        # Draw current line being drawn from first selected ball to cursor
        if self.game_manager.current_line:
            start_pos, end_pos = self.game_manager.current_line
            cv2.line(frame, tuple(map(int, start_pos)), tuple(map(int, end_pos)), 
                    (0, 255, 255), 2)  # Yellow line while drawing
            
            # Draw circle at cursor position
            cv2.circle(frame, tuple(map(int, end_pos)), 8, (0, 255, 255), 2)
        
        # Draw hand landmarks
        if hand_landmarks:
            for hand in hand_landmarks:
                for i, landmark in enumerate(hand):
                    x, y = int(landmark[0]), int(landmark[1])
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                    
                    # Draw connections between landmarks for hand visualization
                    if i < len(hand) - 1:
                        x_next, y_next = int(hand[i + 1][0]), int(hand[i + 1][1])
                        cv2.line(frame, (x, y), (x_next, y_next), (0, 200, 0), 1)
        
        # Draw UI
        self._draw_ui(frame)
    
    def _draw_ui(self, frame):
        """Draw user interface elements"""
        # Score
        score_text = f"Score: {self.game_manager.score}"
        draw_text(frame, score_text, (10, 30), color=(0, 255, 0), font_size=1)
        
        # Level
        level_text = f"Level: {self.game_manager.level}"
        draw_text(frame, level_text, (10, 60), color=(0, 255, 0), font_size=1)
        
        # Remaining pairs
        total_pairs = len(self.game_manager.balls) // 2
        matched_pairs = len(self.game_manager.matched_pairs)
        remaining_text = f"Pairs: {matched_pairs}/{total_pairs}"
        draw_text(frame, remaining_text, (10, 90), 
                 color=(255, 200, 0), font_size=1)
        
        # Combo
        if self.game_manager.combo > 0:
            combo_text = f"Combo: {self.game_manager.combo}x"
            draw_text(frame, combo_text, (10, 120), 
                     color=(0, 165, 255), font_size=1)
        
        # FPS
        if self.show_fps:
            fps_text = f"FPS: {self.fps:.1f}"
            draw_text(frame, fps_text, 
                     (frame.shape[1] - 150, 30), 
                     color=(0, 255, 0), font_size=0.7)
        
        # Help text
        if self.show_help:
            help_text = "Match same colors | H: Help | Q: Quit | R: Reset"
            draw_text(frame, help_text, 
                     (frame.shape[1] - 450, frame.shape[0] - 20), 
                     color=(200, 200, 200), font_size=0.5)
    
    def update_fps(self, current_time):
        """Update FPS calculation"""
        self.frame_count += 1
        if current_time - self.prev_time >= 1:
            self.fps = self.frame_count / (current_time - self.prev_time)
            self.frame_count = 0
            self.prev_time = current_time
    
    def handle_input(self):
        """Handle keyboard input"""
        key = cv2.waitKey(5) & 0xFF
        
        if key == ord('q') or key == 27:  # Q or ESC
            self.is_running = False
        elif key == ord('h'):  # H for help
            self.show_help = not self.show_help
        elif key == ord('r'):  # R for reset
            self.game_manager.reset_game()
        elif key == ord('f'):  # F for FPS
            self.show_fps = not self.show_fps
    
    def run(self):
        """Main game loop"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        
        import time
        
        while self.is_running:
            success, frame = self.cap.read()
            
            if not success:
                print("Failed to read frame from camera")
                break
            
            # Flip frame for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame
            frame = self.process_frame(frame)
            
            # Update game logic
            current_time = time.time()
            self.game_manager.update(frame.shape)
            self.update_fps(current_time)
            
            # Display frame
            cv2.imshow(self.window_name, frame)
            
            # Handle input
            self.handle_input()
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    """Entry point for the game"""
    game = GestureGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Game closed")

if __name__ == "__main__":
    main()
