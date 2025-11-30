"""
Nokia Snake Game with Gesture Control
Main entry point for the game
"""
import cv2
import threading
from snake_game import SnakeGame
from gesture_controller import GestureController

class GameController:
    def __init__(self):
        self.game = SnakeGame()
        self.gesture_controller = GestureController()
        self.running = True
        self.current_gesture = None
        self.boost_active = False
        
    def gesture_thread(self):
        """Thread for processing gestures"""
        while self.running:
            frame, gesture, boost = self.gesture_controller.process_frame()
            
            if frame is not None:
                # Display gesture window
                cv2.imshow('Gesture Control', frame)
                
                # Update gesture state
                if gesture:
                    self.current_gesture = gesture
                self.boost_active = boost
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
    
    def run(self):
        """Main game loop"""
        # Start gesture detection thread
        gesture_thread = threading.Thread(target=self.gesture_thread)
        gesture_thread.daemon = True
        gesture_thread.start()
        
        print("=" * 50)
        print("Nokia Snake - Gesture Control")
        print("=" * 50)
        print("\nControls:")
        print("  Swipe UP/DOWN/LEFT/RIGHT - Move snake")
        print("  Pinch (thumb + index) - Speed boost")
        print("  ESC - Quit game")
        print("  Q in gesture window - Quit")
        print("\nGame Rules:")
        print("  • Eat fruit to grow and score points")
        print("  • Don't hit walls or yourself")
        print("  • Show UP gesture when game over to restart")
        print("\nStarting game...")
        print("=" * 50)
        
        # Main game loop
        try:
            while self.running:
                if not self.game.run_frame(self.current_gesture, self.boost_active):
                    self.running = False
                
                # Reset gesture after processing
                self.current_gesture = None
        
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        
        finally:
            # Cleanup
            print("\nCleaning up...")
            self.running = False
            self.game.quit()
            self.gesture_controller.release()
            print("Game closed. Thanks for playing!")

def main():
    """Entry point"""
    try:
        controller = GameController()
        controller.run()
    except RuntimeError as e:
        print(f"Error: {e}")
        print("\nPlease ensure:")
        print("  1. Webcam is connected")
        print("  2. Camera permissions are granted")
        print("  3. No other application is using the camera")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()