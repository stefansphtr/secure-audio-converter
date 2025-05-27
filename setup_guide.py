"""
Installation and Setup Guide for Secure Audio Converter
"""

import subprocess
import sys
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def check_python():
    """Check Python installation."""
    version = sys.version_info
    if version >= (3, 7):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.7+")
        return False

def check_tkinter():
    """Check tkinter availability."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ Tkinter - OK")
        return True
    except ImportError:
        print("❌ Tkinter - Not available")
        print("   Install: pip install tk")
        return False
    except Exception as e:
        print(f"⚠️  Tkinter - Available but issue: {e}")
        return True

def check_ffmpeg():
    """Check FFmpeg installation."""
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ FFmpeg - {version_line}")
                return True
            else:
                print("❌ FFmpeg - Found but not working")
                return False
        except Exception as e:
            print(f"❌ FFmpeg - Error checking: {e}")
            return False
    else:
        print("❌ FFmpeg - Not found in PATH")
        return False

def install_ffmpeg_instructions():
    """Show FFmpeg installation instructions."""
    print("\n🔧 FFmpeg Installation Instructions:")
    print("   Choose ONE of the following methods:")
    print("\n   Method 1 - Chocolatey (Recommended):")
    print("   1. Install Chocolatey: https://chocolatey.org/install")
    print("   2. Run: choco install ffmpeg")
    print("\n   Method 2 - winget:")
    print("   Run: winget install FFmpeg.FFmpeg")
    print("\n   Method 3 - Manual Download:")
    print("   1. Go to: https://ffmpeg.org/download.html")
    print("   2. Download Windows build")
    print("   3. Extract to C:\\ffmpeg")
    print("   4. Add C:\\ffmpeg\\bin to system PATH")
    print("\n   Method 4 - Portable (No admin required):")
    print("   1. Download from: https://www.gyan.dev/ffmpeg/builds/")
    print("   2. Extract anywhere")
    print("   3. Add the bin folder to PATH")

def test_converter():
    """Test the converter initialization."""
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src" / "script"))
        from converter_core import SecureAudioConverter
        converter = SecureAudioConverter()
        print("✅ Converter - Initialized successfully")
        return True
    except RuntimeError as e:
        if "FFmpeg not found" in str(e):
            print("❌ Converter - FFmpeg required")
            return False
        else:
            print(f"❌ Converter - Error: {e}")
            return False
    except Exception as e:
        print(f"❌ Converter - Import error: {e}")
        return False

def create_test_structure():
    """Create test directories."""
    try:
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        (test_dir / "input").mkdir(exist_ok=True)
        (test_dir / "output").mkdir(exist_ok=True)
        print("✅ Test directories created")
        return True
    except Exception as e:
        print(f"❌ Failed to create test directories: {e}")
        return False

def main():
    """Main setup function."""
    print_header("SECURE AUDIO CONVERTER - SETUP GUIDE")
    
    print("This guide will help you set up the Secure Audio Converter.")
    print("Please follow each step carefully.")
    
    # Step 1: Check Python
    print_step(1, "Checking Python Installation")
    python_ok = check_python()
    
    # Step 2: Check Tkinter
    print_step(2, "Checking Tkinter (GUI Support)")
    tkinter_ok = check_tkinter()
    
    # Step 3: Check FFmpeg
    print_step(3, "Checking FFmpeg (Audio Processing)")
    ffmpeg_ok = check_ffmpeg()
    
    if not ffmpeg_ok:
        install_ffmpeg_instructions()
    
    # Step 4: Test converter
    print_step(4, "Testing Converter Initialization")
    converter_ok = test_converter()
    
    # Step 5: Create test structure
    print_step(5, "Setting up Test Environment")
    test_ok = create_test_structure()
    
    # Summary
    print_header("SETUP SUMMARY")
    
    components = [
        ("Python 3.7+", python_ok),
        ("Tkinter (GUI)", tkinter_ok),
        ("FFmpeg (Audio)", ffmpeg_ok),
        ("Converter Core", converter_ok),
        ("Test Environment", test_ok)
    ]
    
    for name, status in components:
        icon = "✅" if status else "❌"
        print(f"   {icon} {name}")
    
    # Final recommendations
    all_ok = all(status for _, status in components)
    
    if all_ok:
        print("\n🎉 Setup Complete!")
        print("\n🚀 You can now use the converter:")
        print("   GUI Mode: python src/script/converter_mp3.py")
        print("   CLI Mode: python src/script/converter_mp3.py input.mp4")
        print("   Simple GUI: python src/script/simple_gui.py")
    else:
        print("\n⚠️  Setup Incomplete")
        print("\nRequired actions:")
        
        if not ffmpeg_ok:
            print("   • Install FFmpeg (see instructions above)")
        if not tkinter_ok:
            print("   • Install Tkinter: pip install tk")
        if not python_ok:
            print("   • Upgrade Python to 3.7 or higher")
        
        print("\nAfter fixing issues, run this setup again:")
        print("   python setup_guide.py")
    
    print("\n📚 For more help, see README.md")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
