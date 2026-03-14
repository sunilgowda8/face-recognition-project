# reinstall_opencv.py
import subprocess
import sys
import os

def reinstall_opencv():
    print("Reinstalling OpenCV with GUI support...")
    
    # Uninstall all OpenCV versions
    packages = ["opencv-python", "opencv-contrib-python", "opencv-python-headless"]
    for package in packages:
        result = subprocess.run([
            sys.executable, "-m", "pip", "uninstall", "-y", package
        ], capture_output=True, text=True)
        print(f"Uninstalled {package}")
    
    # Install opencv-contrib-python (includes GUI support)
    print("Installing opencv-contrib-python...")
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "opencv-contrib-python"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ OpenCV installed successfully!")
        print("Please restart your application.")
    else:
        print("❌ Failed to install OpenCV:")
        print(result.stderr)
        
    input("Press Enter to exit...")

if __name__ == "__main__":
    reinstall_opencv()