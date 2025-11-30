"""
Setup script to automatically install all required dependencies
"""
import subprocess
import sys

def install_requirements():
    """Install all packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ All packages installed successfully!")
        print("\nYou can now run the game with: python main.py")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error installing packages: {e}")
        print("Please try installing manually: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()