# camera_test.py
import cv2
import sys

def test_camera():
    print("Testing camera access...")
    
    # Try different camera indices
    for i in range(5):
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            print(f"✅ Camera {i} is accessible!")
            
            # Try to read a frame
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} can read frames!")
                cv2.imshow(f'Camera {i} Test - Press any key to close', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print(f"❌ Camera {i} cannot read frames")
            
            cap.release()
        else:
            print(f"❌ Camera {i} is not accessible")
    
    print("\nCamera test completed.")

if __name__ == "__main__":
    test_camera()