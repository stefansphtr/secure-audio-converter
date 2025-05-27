"""
Configuration settings for the audio converter.
"""

import logging
import os

# Logging configuration
def setup_logging(log_level=logging.INFO, log_file='converter.log'):
    """Setup logging configuration."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

# Application settings
APP_NAME = "Secure Audio Converter"
APP_VERSION = "1.0.0"

# Default conversion settings
DEFAULT_BITRATE = "192k"
DEFAULT_QUALITY = "high"
DEFAULT_FORMAT = "mp3"

# Quality presets
QUALITY_PRESETS = {
    "high": {"mp3": "0", "description": "Best quality"},
    "medium": {"mp3": "2", "description": "Good quality"},
    "low": {"mp3": "4", "description": "Smaller files"}
}

# Bitrate options
BITRATE_OPTIONS = ["128k", "192k", "256k", "320k"]

# File size limits
MAX_FILE_SIZE_MB = 500
MAX_BATCH_FILES = 50

# UI settings
WINDOW_SIZE = "800x600"
THEME_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
SUCCESS_COLOR = "#27AE60"
ERROR_COLOR = "#E74C3C"
