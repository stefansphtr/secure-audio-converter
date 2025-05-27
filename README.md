# Secure Audio Converter

A secure, user-friendly application to convert MP4 video files to MP3 or WAV audio format with comprehensive security measures and both GUI and CLI interfaces.

## 🌟 Features

- **🔒 Security First**: Input validation, file size limits, and path sanitization
- **🖥️ Dual Interface**: Both GUI (tkinter) and command-line interfaces
- **⚡ Fast Conversion**: Uses FFmpeg for efficient processing
- **📦 Batch Processing**: Convert multiple files at once
- **🎵 Quality Control**: Three quality levels (high, medium, low)
- **📝 Comprehensive Logging**: Detailed logs for debugging and audit
- **🎯 Format Support**: MP3 and WAV output formats

## 📁 Project Structure

```text
Tools/
├── requirements.txt          # Python dependencies
├── setup.py                 # Setup and verification script
├── README.md                # This file
└── src/
    └── script/
        ├── __init__.py
        ├── converter_mp3.py  # Main entry point
        ├── converter_core.py # Core conversion logic
        ├── config.py         # Configuration settings
        └── gui.py           # GUI interface
```

## 🚀 Quick Start

### 1. Setup

Run the setup script to verify dependencies:

```bash
python setup.py
```

### 2. Usage

**GUI Mode (Recommended):**

```bash
python src/script/converter_mp3.py
```

**Command Line Mode:**

```bash
# Convert single file
python src/script/converter_mp3.py video.mp4

# Convert to WAV with high bitrate
python src/script/converter_mp3.py video.mp4 --format wav --bitrate 320k

# Batch convert with custom output directory
python src/script/converter_mp3.py *.mp4 --output-dir ./converted --quality high
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
- **Allowed formats**: MP4, M4V, MOV, AVI, MKV
- **Output formats**: MP3, WAV
- **Default quality**: High (192k bitrate)
- **Timeout**: 5 minutes per file

Modify `src/script/config.py` to adjust these settings.

## 🖼️ GUI Features

- **Drag & Drop**: Easy file selection
- **Progress Tracking**: Real-time conversion progress
- **Batch Processing**: Queue multiple files
- **Settings Panel**: Adjust quality, bitrate, and output format
- **Log Viewer**: Monitor conversion status and errors

## 🔒 Security Features

1. **Input Validation**: File extension and size checks
2. **Path Sanitization**: Prevents directory traversal attacks
3. **File Integrity**: SHA256 hash verification
4. **Process Security**: Timeout protection and error handling
5. **Safe Output**: Prevents overwriting without confirmation

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
```

## 🐛 Troubleshooting

**FFmpeg not found:**

- Install FFmpeg and ensure it's in your system PATH
- Run `ffmpeg -version` to verify installation

**GUI not working:**

- Ensure tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt-get install python3-tk`

**Conversion fails:**

- Check file format is supported
- Verify file isn't corrupted
- Check available disk space
- Review logs for detailed error messages

## 📝 Logging

Logs are saved to `converter.log` and include:

- File validation results
- Conversion progress
- Error messages and debugging info
- Security-related events

## 🤝 Contributing

1. Follow the modular structure
2. Add tests for new features
3. Update documentation
4. Ensure security measures are maintained

## 📄 License

This project is intended for internal use at Teleperformance. All rights reserved.

## 🆘 Support

For issues or questions:

1. Check the logs in `converter.log`
2. Verify FFmpeg installation
3. Run `python setup.py` to check configuration
4. Review this README for troubleshooting tips
