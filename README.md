# Secure Audio Converter

A secure, user-friendly application to convert video files to audio format AND convert between different audio formats with comprehensive security measures and both GUI and CLI interfaces.

## 🌟 Features

- **🔒 Security First**: Input validation, file size limits, and path sanitization
- **🎵 Dual Conversion Types**: 
  - **Video-to-Audio**: MP4, M4V, MOV, AVI, MKV → MP3, WAV
  - **Audio-to-Audio**: MP3, WAV, M4A, AAC, FLAC → MP3, WAV ✨ NEW
- **🖥️ Multiple Interfaces**: GUI (tkinter), CLI, and web (Streamlit) interfaces
- **⚡ Fast Conversion**: Uses FFmpeg for efficient processing
- **📦 Batch Processing**: Convert multiple files at once
- **🎵 Quality Control**: Three quality levels (high, medium, low)
- **📝 Comprehensive Logging**: Detailed logs for debugging and audit

## 📁 Project Structure

```text
Tools/
├── requirements.txt          # Python dependencies
├── packages.txt             # System packages (FFmpeg)
├── setup.py                 # Setup and verification script
├── streamlit_app.py         # Web interface
├── README.md                # This file
└── src/
    └── script/
        ├── __init__.py
        ├── converter_mp3.py  # Main entry point
        ├── converter_core.py # Core conversion logic
        ├── config.py         # Configuration settings
        ├── gui.py           # Desktop GUI interface
        └── simple_gui.py    # Simplified GUI
```

## 🚀 Quick Start

### 1. Setup

Run the setup script to verify dependencies:

```bash
python setup.py
```

### 2. Usage Options

**Web Interface (Streamlit):**
```bash
streamlit run streamlit_app.py
```

**Desktop GUI Mode:**
```bash
python src/script/converter_mp3.py
```

**Command Line Mode:**
```bash
# Convert video to audio
python src/script/converter_mp3.py video.mp4

# Convert audio format
python src/script/converter_mp3.py audio.flac --format mp3

# Convert to WAV with high bitrate
python src/script/converter_mp3.py audio.mp3 --format wav

# Batch convert with custom output directory
python src/script/converter_mp3.py *.mp3 *.flac --output-dir ./converted --quality high
```

## 📋 Prerequisites

- **Python 3.7+** (with tkinter for GUI)
- **FFmpeg** (system installation required)

### Installing FFmpeg

**Windows:**

```bash
# Using Chocolatey
choco install ffmpeg

# Using winget
winget install FFmpeg.FFmpeg

# Or download from: https://ffmpeg.org/download.html
```

## 🔧 Configuration

The application uses secure defaults:

- **Max file size**: 500MB
- **Allowed input formats**: 
  - **Video**: MP4, M4V, MOV, AVI, MKV
  - **Audio**: MP3, WAV, M4A, AAC, FLAC ✨ NEW
- **Output formats**: MP3, WAV
- **Default quality**: High (192k bitrate)
- **Timeout**: 5 minutes per file

Modify [`src/script/config.py`](src/script/config.py) to adjust these settings.

## 🎵 Supported Conversions

### Video to Audio (Original Feature)
- **MP4** → MP3/WAV
- **M4V** → MP3/WAV  
- **MOV** → MP3/WAV
- **AVI** → MP3/WAV
- **MKV** → MP3/WAV

### Audio to Audio ✨ NEW
- **MP3** ↔ WAV (bidirectional)
- **M4A** → MP3/WAV
- **AAC** → MP3/WAV
- **FLAC** → MP3/WAV
- **WAV** → MP3

### Use Cases for Audio-to-Audio Conversion
- **Format Standardization**: Convert mixed audio library to consistent format
- **Quality Adjustment**: Re-encode with different quality settings
- **Compression**: Convert uncompressed WAV to smaller MP3
- **Professional Prep**: Convert MP3 to WAV for editing software
- **Device Compatibility**: Convert unsupported formats to universal MP3

## 🖼️ Interface Features

### Web Interface (Streamlit)
- **Drag & Drop Upload**: Easy file selection for video and audio
- **Real-time Progress**: Live conversion status updates
- **Batch Download**: ZIP download for multiple converted files
- **Responsive Design**: Works on desktop and mobile
- **No Installation**: Use directly in web browser

### Desktop GUI
- **File Queue Management**: Add, remove, and organize conversion queue
- **Progress Tracking**: Real-time conversion progress
- **Settings Panel**: Adjust quality, bitrate, and output format
- **Log Viewer**: Monitor conversion status and errors

## 🔒 Security Features

1. **Input Validation**: File extension and size checks for both video and audio
2. **Path Sanitization**: Prevents directory traversal attacks
3. **File Integrity**: SHA256 hash verification
4. **Process Security**: Timeout protection and error handling
5. **Safe Output**: Prevents overwriting without confirmation
6. **Format Verification**: Validates actual file content, not just extension

## 📊 Command Line Options

```text
python src/script/converter_mp3.py [options] [files...]

Options:
  --gui                 Launch GUI interface (default if no files)
  --format {mp3,wav}    Output format (default: mp3)
  --output-dir DIR      Output directory
  --bitrate RATE        Audio bitrate (default: 192k)
  --quality {high,medium,low}  Conversion quality (default: high)
  --verbose             Enable verbose logging

Examples:
  # Convert video to audio
  python converter_mp3.py video.mp4
  
  # Convert FLAC to high-quality MP3
  python converter_mp3.py music.flac --format mp3 --bitrate 320k
  
  # Convert MP3 to WAV for editing
  python converter_mp3.py audio.mp3 --format wav
  
  # Batch convert mixed formats
  python converter_mp3.py *.mp3 *.flac *.m4a --output-dir ./converted
```

## 🐛 Troubleshooting

**FFmpeg not found:**
- Install FFmpeg and ensure it's in your system PATH
- Run `ffmpeg -version` to verify installation

**Unsupported format error:**
- Check if your file format is in the supported list
- Verify file isn't corrupted
- For audio files: ensure the file contains valid audio data

**Conversion fails:**
- Check file format is supported (Video: MP4/M4V/MOV/AVI/MKV, Audio: MP3/WAV/M4A/AAC/FLAC)
- Verify file isn't corrupted
- Check available disk space
- Review logs for detailed error messages

**Quality concerns:**
- Remember: converting compressed audio (MP3) to uncompressed (WAV) won't improve quality
- For best results, start with highest quality source available
- Use WAV output only when you need uncompressed audio for editing

## 📝 Logging

Logs are saved to `converter.log` and include:

- File validation results (video and audio)
- Conversion progress and completion status
- Error messages and debugging info
- Security-related events
- Format conversion details

## 🤝 Contributing

1. Follow the modular structure
2. Add tests for new features
3. Update documentation for new audio format support
4. Ensure security measures are maintained
5. Test both video-to-audio and audio-to-audio conversions

## 📄 License

This project is intended for internal use at Teleperformance. All rights reserved.

## 🆘 Support

For issues or questions:

1. Check the logs in `converter.log`
2. Verify FFmpeg installation
3. Run `python setup.py` to check configuration
4. Ensure your file format is supported
5. Review this README for troubleshooting tips

---

**Made with 🔥 by Stefan | AI Enthusiast**