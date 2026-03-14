# check_opencv.py
import cv2
import pkg_resources

print("OpenCV Version:", cv2.__version__)
print("OpenCV Build Information:")
print(cv2.getBuildInformation())

# Check available modules
print("\nChecking face module...")
if hasattr(cv2, 'face'):
    print("✅ cv2.face module is available")
    print("Available in cv2.face:", [x for x in dir(cv2.face) if not x.startswith('_')])
else:
    print("❌ cv2.face module is NOT available")

# Check if we can create recognizer
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("✅ LBPHFaceRecognizer_create works!")
except Exception as e:
    print(f"❌ LBPHFaceRecognizer_create failed: {e}")
    # Try alternative
    try:
        recognizer = cv2.face.createLBPHFaceRecognizer()
        print("✅ createLBPHFaceRecognizer works!")
    except Exception as e:
        print(f"❌ createLBPHFaceRecognizer also failed: {e}")