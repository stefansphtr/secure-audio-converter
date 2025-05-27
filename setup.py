"""
Setup and test script for the Secure Audio Converter.
"""

import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_tkinter():
    """Check if tkinter is available."""
    try:
        import tkinter
        print("✅ Tkinter is available")
        return True
    except ImportError:
        print("❌ Tkinter not found. Please install python3-tk")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        print(f"✅ FFmpeg found at: {ffmpeg_path}")
        return True
    else:
        print("❌ FFmpeg not found. Please install FFmpeg:")
        print("   Windows: choco install ffmpeg  OR  winget install FFmpeg.FFmpeg")
        print("   Download: https://ffmpeg.org/download.html")
        return False

def install_requirements():
    """Install required packages."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def test_import():
    """Test if all modules can be imported."""
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src" / "script"))
        
        from converter_core import SecureAudioConverter
        from config import setup_logging
        print("✅ Core modules imported successfully")
        
        try:
            from gui import ConverterGUI
            print("✅ GUI module imported successfully")
        except ImportError as e:
            print(f"⚠️  GUI module import failed: {e}")
            
        return True
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🔧 Setting up Secure Audio Converter...")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Tkinter", check_tkinter),
        ("FFmpeg", check_ffmpeg),
        ("Requirements", install_requirements),
        ("Module Import", test_import),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        results.append(check_func())
    
    print("\n" + "=" * 50)
    print("📊 Setup Summary:")
    
    for (name, _), result in zip(checks, results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
    
    if all(results):
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 Usage:")
        print("   GUI mode: python src/script/converter_mp3.py")
        print("   CLI mode: python src/script/converter_mp3.py input.mp4")
    else:
        print("\n⚠️  Setup incomplete. Please fix the failed checks above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
