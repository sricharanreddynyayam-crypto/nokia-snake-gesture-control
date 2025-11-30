"""
Hand Gesture Controller using MediaPipe
Detects hand gestures for controlling the snake game
"""
import cv2
import mediapipe as mp
import numpy as np

class GestureController:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_detection
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture detection parameters
        self.prev_hand_position = None
        self.gesture_threshold = 0.05
        self.current_direction = None
        
        # Camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")
    
    def detect_pinch(self, hand_landmarks):
        """Detect pinch gesture (thumb and index finger close together)"""
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        
        distance = np.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        
        return distance < 0.05
    
    def detect_gestures(self, hand_landmarks):
        """Detect swipe gestures based on hand movement"""
        # Get palm center (wrist position)
        wrist = hand_landmarks.landmark[0]
        current_pos = np.array([wrist.x, wrist.y])
        
        gesture = None
        
        if self.prev_hand_position is not None:
            # Calculate movement
            movement = current_pos - self.prev_hand_position
            
            # Detect significant movements
            if abs(movement[0]) > self.gesture_threshold or abs(movement[1]) > self.gesture_threshold:
                if abs(movement[0]) > abs(movement[1]):
                    # Horizontal movement
                    gesture = 'RIGHT' if movement[0] > 0 else 'LEFT'
                else:
                    # Vertical movement
                    gesture = 'DOWN' if movement[1] > 0 else 'UP'
        
        self.prev_hand_position = current_pos
        return gesture
    
    def process_frame(self):
        """Process camera frame and detect gestures"""
        ret, frame = self.cap.read()
        if not ret:
            return None, None, None
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect hands
        hand_results = self.hands.process(rgb_frame)
        
        # Detect face
        face_results = self.face_detection.process(rgb_frame)
        
        gesture = None
        boost = False
        
        # Draw face detection
        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                       int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(frame, bbox, (0, 255, 0), 2)
                cv2.putText(frame, 'Face Detected', (bbox[0], bbox[1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Process hand gestures
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                
                # Detect gestures
                gesture = self.detect_gestures(hand_landmarks)
                boost = self.detect_pinch(hand_landmarks)
                
                if gesture:
                    self.current_direction = gesture
        
        # Display current direction
        if self.current_direction:
            cv2.putText(frame, f'Direction: {self.current_direction}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if boost:
            cv2.putText(frame, 'BOOST!', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return frame, gesture, boost
    
    def release(self):
        """Release camera resources"""
        self.cap.release()
        cv2.destroyAllWindows()