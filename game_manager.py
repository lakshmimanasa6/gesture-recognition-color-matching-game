"""
Game Manager Module
Manages game state, scoring, and ball color matching
"""

import random
import numpy as np
from utils import distance_between_points

class GameManager:
    def __init__(self):
        """Initialize the game manager"""
        self.score = 0
        self.level = 1
        self.combo = 0
        self.max_combo = 0
        
        # Game state
        self.balls = []
        self.matched_pairs = []  # Pairs that have been successfully matched
        self.current_line = None  # Current line being drawn from gesture
        self.first_selected_ball = None  # First ball selected for matching
        self.cursor_pos = [0, 0]
        self.active_hand_id = None
        
        # Game settings
        self.ball_radius = 25
        self.selection_distance = 50  # How close to select a ball
        self.max_balls = 6 + self.level * 2  # Always even number for pairs
        
        # Initialize game
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.score = 0
        self.level = 1
        self.combo = 0
        self.matched_pairs = []
        self.first_selected_ball = None
        self.current_line = None
        self.generate_balls()
    
    def generate_balls(self, num_pairs=None):
        """Generate colored ball pairs on the screen"""
        if num_pairs is None:
            num_pairs = self.max_balls // 2
        
        self.balls = []
        self.matched_pairs = []
        self.first_selected_ball = None
        
        # Color palette - each color appears twice (pairs)
        colors = [
            (255, 0, 0),    # Blue
            (0, 255, 0),    # Green
            (0, 0, 255),    # Red
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
            (128, 0, 255),  # Purple
            (255, 128, 0),  # Orange
            (0, 128, 255),  # Sky Blue
            (255, 0, 128),  # Pink
        ]
        
        # Create pairs of each color
        color_list = []
        for i in range(num_pairs):
            color_list.append(colors[i % len(colors)])
            color_list.append(colors[i % len(colors)])  # Add color twice for pairs
        
        # Shuffle colors
        random.shuffle(color_list)
        
        # Generate ball positions
        for i, color in enumerate(color_list):
            # Random position avoiding overlaps
            while True:
                x = random.randint(self.ball_radius + 50, 1280 - self.ball_radius - 50)
                y = random.randint(self.ball_radius + 100, 720 - self.ball_radius - 50)
                
                # Check if position is too close to other balls
                too_close = False
                for ball in self.balls:
                    dist = distance_between_points((x, y), tuple(ball['pos']))
                    if dist < self.ball_radius * 3.5:
                        too_close = True
                        break
                
                if not too_close:
                    break
            
            ball = {
                'id': i,
                'pos': np.array([x, y]),
                'radius': self.ball_radius,
                'color': color,
                'matched': False,
                'selected': False
            }
            self.balls.append(ball)
    
    def update_cursor(self, position, hand_id):
        """Update cursor position from hand gesture"""
        self.cursor_pos = list(position)
        self.active_hand_id = hand_id
        
        # Update the line being drawn
        if self.first_selected_ball is not None:
            self.current_line = (tuple(self.first_selected_ball['pos']), tuple(self.cursor_pos))
        
        # Check if cursor is near any ball to select it
        self.check_ball_selection()
    
    def check_ball_selection(self):
        """Check if cursor is near a ball and select/match it"""
        for ball in self.balls:
            if ball['matched']:  # Skip already matched balls
                continue
            
            dist = distance_between_points(
                tuple(self.cursor_pos),
                tuple(ball['pos'])
            )
            
            if dist < self.selection_distance:
                # First ball selection
                if self.first_selected_ball is None:
                    self.first_selected_ball = ball
                    ball['selected'] = True
                # Second ball selection - attempt match
                elif self.first_selected_ball['id'] != ball['id']:
                    self.attempt_match(ball)
    
    def attempt_match(self, second_ball):
        """Attempt to match two balls"""
        first_ball = self.first_selected_ball
        
        # Check if colors match
        if first_ball['color'] == second_ball['color']:
            # Successful match!
            self.match_pair(first_ball, second_ball)
        else:
            # Wrong color, reset selection
            self.reset_selection()
    
    def match_pair(self, ball1, ball2):
        """Mark a matched pair and update score"""
        ball1['matched'] = True
        ball2['matched'] = True
        
        # Add to matched pairs list
        self.matched_pairs.append({
            'ball1_id': ball1['id'],
            'ball2_id': ball2['id'],
            'color': ball1['color']
        })
        
        # Update score
        self.combo += 1
        base_points = 200
        self.score += base_points * self.combo
        
        # Reset current line
        self.current_line = None
        self.first_selected_ball = None
        
        # Check if level complete
        if len(self.matched_pairs) == len(self.balls) // 2:
            self.level_complete()
    
    def reset_selection(self):
        """Reset the current selection"""
        if self.first_selected_ball:
            self.first_selected_ball['selected'] = False
        
        self.first_selected_ball = None
        self.current_line = None
        self.combo = 0  # Reset combo on wrong match
    
    def level_complete(self):
        """Handle level completion"""
        self.max_combo = max(self.max_combo, self.combo)
        self.level += 1
        self.max_balls = 6 + self.level * 2  # Ensure even number
        self.score += 500 * self.level  # Bonus for level completion
        
        # Generate new balls
        self.generate_balls(self.max_balls // 2)
        self.combo = 0
    
    def update(self, frame_shape):
        """Update game state"""
        # Game updates happen in real-time via gesture tracking
        pass
