"""
Gesture Detection Module
Detects hand gestures and extracts key points using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from utils import distance_between_points

class GestureDetector:
    def __init__(self):
        """Initialize MediaPipe hand detection"""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Gesture thresholds
        self.pointer_threshold = 0.05  # Distance threshold for pointer detection
        self.palm_threshold = 100  # Pixel threshold for palm open/closed
        
    def detect_hands(self, frame):
        """
        Detect hands and landmarks in the frame
        
        Args:
            frame: Input video frame (BGR)
            
        Returns:
            hand_landmarks: List of hand landmark coordinates
            handedness: List of hand labels ('Left' or 'Right')
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        hand_landmarks = []
        handedness = []
        
        if results.multi_hand_landmarks:
            h, w, _ = frame.shape
            
            for hand_lm, hand_info in zip(
                results.multi_hand_landmarks, 
                results.multi_handedness
            ):
                # Extract landmark coordinates
                landmarks = []
                for lm in hand_lm.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    landmarks.append((x, y))
                
                hand_landmarks.append(landmarks)
                handedness.append(hand_info.classification[0].label)
        
        return hand_landmarks, handedness
    
    def get_gesture_points(self, hand_landmarks):
        """
        Extract gesture points (fingertips, palm center, etc.)
        
        Args:
            hand_landmarks: List of hand landmark coordinates
            
        Returns:
            List of tuples (point, hand_id)
        """
        gesture_points = []
        
        if not hand_landmarks:
            return gesture_points
        
        # MediaPipe hand landmarks indices
        THUMB_TIP = 4
        INDEX_FINGER_TIP = 8
        MIDDLE_FINGER_TIP = 12
        RING_FINGER_TIP = 16
        PINKY_TIP = 20
        PALM_CENTER = 9
        
        for hand_id, landmarks in enumerate(hand_landmarks):
            # Get key points (fingertips)
            fingertips = [
                landmarks[THUMB_TIP],
                landmarks[INDEX_FINGER_TIP],
                landmarks[MIDDLE_FINGER_TIP],
                landmarks[RING_FINGER_TIP],
                landmarks[PINKY_TIP]
            ]
            
            # Use index finger tip as primary pointer
            pointer = landmarks[INDEX_FINGER_TIP]
            gesture_points.append((pointer, hand_id))
            
        return gesture_points
    
    def detect_gesture(self, hand_landmarks):
        """
        Detect specific gestures (pointing, open hand, fist, etc.)
        
        Args:
            hand_landmarks: List of hand landmark coordinates
            
        Returns:
            Dictionary with gesture information
        """
        if not hand_landmarks:
            return None
        
        # Landmark indices
        THUMB_IP = 2
        THUMB_TIP = 4
        INDEX_MCP = 5
        INDEX_PIP = 6
        INDEX_DIP = 7
        INDEX_FINGER_TIP = 8
        MIDDLE_PIP = 10
        MIDDLE_FINGER_TIP = 12
        RING_PIP = 14
        RING_FINGER_TIP = 16
        PINKY_PIP = 18
        PINKY_TIP = 20
        WRIST = 0
        
        gestures = {
            'pointing': False,
            'open_hand': False,
            'fist': False,
            'two_finger_point': False,
            'peace': False
        }
        
        for landmarks in hand_landmarks:
            # Calculate finger distances
            index_extended = distance_between_points(
                landmarks[INDEX_FINGER_TIP],
                landmarks[INDEX_PIP]
            ) > distance_between_points(
                landmarks[INDEX_PIP],
                landmarks[INDEX_MCP]
            )
            
            middle_extended = distance_between_points(
                landmarks[MIDDLE_FINGER_TIP],
                landmarks[MIDDLE_PIP]
            ) > distance_between_points(
                landmarks[MIDDLE_PIP],
                landmarks[5]  # MCP
            )
            
            # Pointing gesture (index extended, others folded)
            if index_extended and not middle_extended:
                gestures['pointing'] = True
            
            # Peace gesture (index and middle extended)
            if index_extended and middle_extended:
                gestures['peace'] = True
            
            # Open hand (all fingers extended)
            all_extended = True
            for tip_idx in [THUMB_TIP, INDEX_FINGER_TIP, MIDDLE_FINGER_TIP, 
                           RING_FINGER_TIP, PINKY_TIP]:
                if distance_between_points(landmarks[tip_idx], landmarks[WRIST]) < 50:
                    all_extended = False
            
            if all_extended:
                gestures['open_hand'] = True
        
        return gestures
    
    def release(self):
        """Release resources"""
        self.hands.close()
