"""
Utility Functions
Helper functions for drawing and calculations
"""

import cv2
import math

def distance_between_points(point1, point2):
    """
    Calculate Euclidean distance between two points
    
    Args:
        point1: Tuple (x, y)
        point2: Tuple (x, y)
        
    Returns:
        float: Distance between points
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def draw_text(frame, text, position, color=(255, 255, 255), 
             font=cv2.FONT_HERSHEY_SIMPLEX, font_size=1, thickness=2):
    """
    Draw text on frame
    
    Args:
        frame: Input frame
        text: Text to draw
        position: Tuple (x, y) for text position
        color: BGR color tuple
        font: Font type
        font_size: Font size
        thickness: Text thickness
    """
    cv2.putText(frame, text, position, font, font_size, color, thickness)

def draw_circle(frame, center, radius, color=(0, 255, 0), thickness=-1):
    """
    Draw circle on frame
    
    Args:
        frame: Input frame
        center: Tuple (x, y) for center
        radius: Circle radius
        color: BGR color tuple
        thickness: -1 for filled, positive for outline
    """
    cv2.circle(frame, tuple(map(int, center)), radius, color, thickness)

def draw_line(frame, point1, point2, color=(0, 255, 0), thickness=2):
    """
    Draw line on frame
    
    Args:
        frame: Input frame
        point1: Start point tuple (x, y)
        point2: End point tuple (x, y)
        color: BGR color tuple
        thickness: Line thickness
    """
    cv2.line(frame, tuple(map(int, point1)), tuple(map(int, point2)), color, thickness)

def draw_rectangle(frame, top_left, bottom_right, color=(0, 255, 0), thickness=2):
    """
    Draw rectangle on frame
    
    Args:
        frame: Input frame
        top_left: Top-left corner tuple (x, y)
        bottom_right: Bottom-right corner tuple (x, y)
        color: BGR color tuple
        thickness: -1 for filled, positive for outline
    """
    cv2.rectangle(frame, tuple(map(int, top_left)), 
                 tuple(map(int, bottom_right)), color, thickness)

def point_in_circle(point, center, radius):
    """
    Check if a point is inside a circle
    
    Args:
        point: Tuple (x, y)
        center: Tuple (x, y) for circle center
        radius: Circle radius
        
    Returns:
        bool: True if point is in circle
    """
    dist = distance_between_points(point, center)
    return dist <= radius

def line_intersection(p1, p2, p3, p4):
    """
    Check if two lines intersect
    
    Args:
        p1, p2: Points defining first line
        p3, p4: Points defining second line
        
    Returns:
        bool: True if lines intersect
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    if abs(denom) < 1e-10:
        return False
    
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    
    return 0 <= ua <= 1 and 0 <= ub <= 1

def smoothen_coordinates(current, previous, alpha=0.6):
    """
    Apply exponential smoothing to coordinates
    
    Args:
        current: Current coordinates
        previous: Previous coordinates
        alpha: Smoothing factor (0-1)
        
    Returns:
        tuple: Smoothed coordinates
    """
    if previous is None:
        return current
    
    smoothed_x = int(alpha * current[0] + (1 - alpha) * previous[0])
    smoothed_y = int(alpha * current[1] + (1 - alpha) * previous[1])
    
    return (smoothed_x, smoothed_y)

def get_fps(frame_count, elapsed_time):
    """
    Calculate FPS
    
    Args:
        frame_count: Number of frames processed
        elapsed_time: Elapsed time in seconds
        
    Returns:
        float: FPS value
    """
    if elapsed_time == 0:
        return 0
    return frame_count / elapsed_time

def clamp(value, min_val, max_val):
    """
    Clamp value between min and max
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))
