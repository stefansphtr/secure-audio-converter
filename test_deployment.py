#!/usr/bin/env python3
"""
Test script to verify FFmpeg installation and functionality.
This script can be used to debug deployment issues.
"""

import subprocess
import shutil
import sys
import os
from pathlib import Path

def test_ffmpeg_installation():
    """Test FFmpeg installation and availability."""
    print("🔍 Testing FFmpeg Installation")
    print("=" * 50)
    
    # Test 1: Check if ffmpeg is in PATH
    print("\n1. Checking system PATH...")
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        print(f"✅ FFmpeg found in PATH: {ffmpeg_path}")
    else:
        print("❌ FFmpeg not found in system PATH")
    
    # Test 2: Check common installation paths
    print("\n2. Checking common installation paths...")
    common_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/opt/conda/bin/ffmpeg',
        '/app/.apt/usr/bin/ffmpeg',  # Streamlit Cloud path
        'C:\\ffmpeg\\bin\\ffmpeg.exe',
        'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'
    ]
    
    found_paths = []
    for path in common_paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"✅ Found: {path}")
    
    if not found_paths:
        print("❌ No FFmpeg found in common paths")
    
    # Test 3: Try to run ffmpeg
    print("\n3. Testing FFmpeg execution...")
    ffmpeg_executable = ffmpeg_path or (found_paths[0] if found_paths else 'ffmpeg')
    
    try:
        result = subprocess.run(
            [ffmpeg_executable, '-version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg working: {version_line}")
            return True
        else:
            print(f"❌ FFmpeg execution failed (code {result.returncode})")
            print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg executable not found")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg execution timed out")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test error: {e}")
        return False

def test_converter_initialization():
    """Test the converter initialization."""
    print("\n🔧 Testing Converter Initialization")
    print("=" * 50)
    
    try:
        # Add the script directory to Python path
        script_dir = Path(__file__).parent / "src" / "script"
        sys.path.insert(0, str(script_dir))
        
        from converter_core import SecureAudioConverter
        
        converter = SecureAudioConverter()
        print(f"✅ Converter initialized successfully")
        print(f"✅ FFmpeg path: {converter.ffmpeg_path}")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except RuntimeError as e:
        print(f"❌ Runtime error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_environment():
    """Check the deployment environment."""
    print("\n🌍 Environment Information")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check for Streamlit Cloud indicators
    streamlit_indicators = [
        'STREAMLIT_SERVER_PORT' in os.environ,
        'STREAMLIT_SHARING_MODE' in os.environ,
        '/app' in os.getcwd(),
        '.streamlit' in os.path.expanduser('~')
    ]
    
    if any(streamlit_indicators):
        print("🌊 Detected: Streamlit Cloud environment")
    else:
        print("🖥️  Detected: Local environment")
    
    # Check if packages.txt exists
    packages_txt = Path('packages.txt')
    if packages_txt.exists():
        print(f"✅ packages.txt found")
        with open(packages_txt) as f:
            content = f.read().strip()
            print(f"   Content: {content}")
    else:
        print("❌ packages.txt not found (required for Streamlit Cloud)")

def main():
    """Main test function."""
    print("🧪 Secure Audio Converter - Deployment Test")
    print("🔥 Made by Stefan")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Environment Check", check_environment),
        ("FFmpeg Installation", test_ffmpeg_installation),
        ("Converter Initialization", test_converter_initialization),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The converter should work correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        
        # Deployment-specific advice
        print("\n💡 Troubleshooting Tips:")
        print("• For Streamlit Cloud: Ensure 'packages.txt' contains 'ffmpeg'")
        print("• For local deployment: Install FFmpeg system-wide")
        print("• Check deployment logs for package installation errors")
        print("• Try redeploying the application after adding packages.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
