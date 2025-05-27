#!/usr/bin/env python3
"""
Secure MP4 to MP3/WAV Converter - Main Entry Point
Converts MP4 video files to MP3 or WAV audio format with security measures.
Supports both GUI and command-line interfaces.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from converter_core import SecureAudioConverter
from config import setup_logging, APP_NAME, APP_VERSION

logger = logging.getLogger(__name__)


def run_cli(args):
    """Run the command-line interface."""
    try:
        converter = SecureAudioConverter()
        
        if len(args.input_files) == 1:
            success = converter.convert_file(
                args.input_files[0],
                f'.{args.format}',
                args.output_dir,
                args.bitrate,
                args.quality
            )
            sys.exit(0 if success else 1)
        else:
            results = converter.convert_batch(
                args.input_files,
                f'.{args.format}',
                args.output_dir,
                args.bitrate,
                args.quality
            )
            sys.exit(0 if all(results) else 1)
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


def run_gui():
    """Run the graphical user interface."""
    try:
        import tkinter as tk
        from gui import ConverterGUI
        
        root = tk.Tk()
        app = ConverterGUI(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            logger.info("Application terminated by user")
        except Exception as e:
            logger.error(f"GUI error: {e}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Please install tkinter or use the command-line interface.")
        sys.exit(1)


def main():
    """Main function with interface selection."""
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{APP_VERSION} - Secure MP4 to MP3/WAV converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
GUI Mode (default):
  python converter_mp3.py --gui
  python converter_mp3.py (no arguments)

CLI Examples:
  python converter_mp3.py input.mp4
  python converter_mp3.py input.mp4 --format wav --bitrate 320k
  python converter_mp3.py *.mp4 --output-dir ./converted --quality high
        """
    )
    
    parser.add_argument('input_files', nargs='*', help='Input MP4 file(s) (CLI mode)')
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface (default if no files specified)')
    parser.add_argument('--format', '-f', choices=['mp3', 'wav'], default='mp3',
                       help='Output format (default: mp3) [CLI only]')
    parser.add_argument('--output-dir', '-o', help='Output directory [CLI only]')
    parser.add_argument('--bitrate', '-b', default='192k',
                       help='Audio bitrate (default: 192k) [CLI only]')
    parser.add_argument('--quality', '-q', choices=['high', 'medium', 'low'], 
                       default='high', help='Conversion quality (default: high) [CLI only]')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Determine interface mode
    if args.gui or not args.input_files:
        # GUI mode
        logger.info("Launching GUI interface")
        run_gui()
    else:
        # CLI mode
        logger.info("Running in CLI mode")
        run_cli(args)


if __name__ == "__main__":
    main()