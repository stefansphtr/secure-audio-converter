"""
Core converter module for secure audio conversion.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List
import subprocess
import hashlib
import shutil

logger = logging.getLogger(__name__)

class SecureAudioConverter:
    """Secure audio converter with input validation and safety checks."""
    
    # Allowed file extensions for security
    ALLOWED_INPUT_EXTENSIONS = {'.mp4', '.m4v', '.mov', '.avi', '.mkv', '.mp3', '.wav', '.m4a', '.aac', '.flac'}
    ALLOWED_OUTPUT_EXTENSIONS = {'.mp3', '.wav'}
    
    # Maximum file size (500MB)
    MAX_FILE_SIZE = 500 * 1024 * 1024
    
    def __init__(self):
        """Initialize the converter and check for ffmpeg availability."""
        self.ffmpeg_path = self._find_ffmpeg()
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg and ensure it's in PATH.")
        
    def _find_ffmpeg(self) -> Optional[str]:
        """Find ffmpeg executable in system PATH."""
        # Try standard system PATH first
        ffmpeg_path = shutil.which('ffmpeg')
        
        if ffmpeg_path:
            return ffmpeg_path
        
        # Try common installation paths (useful for some environments)
        common_paths = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/opt/conda/bin/ffmpeg',
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
            'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _validate_file_path(self, file_path: str) -> Path:
        """Validate and sanitize file path."""
        try:
            path = Path(file_path).resolve()
            
            # Check if file exists
            if not path.exists():
                raise FileNotFoundError(f"Input file does not exist: {file_path}")
            
            # Check if it's actually a file
            if not path.is_file():
                raise ValueError(f"Path is not a file: {file_path}")
            
            # Check file size
            if path.stat().st_size > self.MAX_FILE_SIZE:
                raise ValueError(f"File too large. Maximum size: {self.MAX_FILE_SIZE / (1024*1024):.1f}MB")
            
            # Check file extension
            if path.suffix.lower() not in self.ALLOWED_INPUT_EXTENSIONS:
                raise ValueError(f"Invalid input file type. Allowed: {', '.join(self.ALLOWED_INPUT_EXTENSIONS)}")
            
            return path
            
        except Exception as e:
            logger.error(f"File validation failed: {e}")
            raise
    
    def _validate_output_format(self, output_format: str) -> str:
        """Validate output format."""
        format_lower = output_format.lower()
        if not format_lower.startswith('.'):
            format_lower = '.' + format_lower
        
        if format_lower not in self.ALLOWED_OUTPUT_EXTENSIONS:
            raise ValueError(f"Invalid output format. Allowed: {', '.join(self.ALLOWED_OUTPUT_EXTENSIONS)}")
        
        return format_lower
    
    def _sanitize_output_path(self, input_path: Path, output_dir: Optional[str], output_format: str) -> Path:
        """Create safe output path."""
        if output_dir:
            output_directory = Path(output_dir).resolve()
            # Ensure output directory exists
            output_directory.mkdir(parents=True, exist_ok=True)
        else:
            output_directory = input_path.parent
        
        # Create output filename
        output_filename = input_path.stem + output_format
        output_path = output_directory / output_filename
        
        # Prevent overwriting existing files without confirmation
        if output_path.exists():
            logger.warning(f"Output file already exists: {output_path}")
            counter = 1
            while output_path.exists():
                output_filename = f"{input_path.stem}_{counter}{output_format}"
                output_path = output_directory / output_filename
                counter += 1
            logger.info(f"Using alternative filename: {output_filename}")
        
        return output_path
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of the file for integrity check."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def convert_file(self, input_file: str, output_format: str = '.mp3', 
                    output_dir: Optional[str] = None, bitrate: str = '192k',
                    quality: str = 'high', progress_callback=None) -> bool:
        """
        Convert MP4 file to MP3 or WAV format securely.
        
        Args:
            input_file: Path to input MP4 file
            output_format: Output format (.mp3 or .wav)
            output_dir: Output directory (optional)
            bitrate: Audio bitrate (default: 192k)
            quality: Conversion quality (high, medium, low)
            progress_callback: Optional callback for progress updates
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Validate inputs
            input_path = self._validate_file_path(input_file)
            output_format = self._validate_output_format(output_format)
            output_path = self._sanitize_output_path(input_path, output_dir, output_format)
            
            logger.info(f"Starting conversion: {input_path} -> {output_path}")
            logger.info(f"Input file hash: {self._get_file_hash(input_path)}")
            
            if progress_callback:
                progress_callback("Starting conversion...", 10)
            
            # Build ffmpeg command with security considerations
            cmd = [
                self.ffmpeg_path,
                '-i', str(input_path),
                '-vn',  # No video
                '-y',   # Overwrite output files
            ]
            
            # Add format-specific options
            if output_format == '.mp3':
                cmd.extend([
                    '-acodec', 'libmp3lame',
                    '-ab', bitrate,
                ])
                
                # Quality settings for MP3
                if quality == 'high':
                    cmd.extend(['-q:a', '0'])
                elif quality == 'medium':
                    cmd.extend(['-q:a', '2'])
                else:  # low
                    cmd.extend(['-q:a', '4'])
                    
            elif output_format == '.wav':
                cmd.extend([
                    '-acodec', 'pcm_s16le',
                    '-ar', '44100',  # Sample rate
                ])
            
            cmd.append(str(output_path))
            
            if progress_callback:
                progress_callback("Converting...", 50)
            
            # Execute conversion with timeout
            logger.info(f"Executing: {' '.join(cmd[:3])} ... {cmd[-1]}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                check=False
            )
            
            if progress_callback:
                progress_callback("Finalizing...", 90)
            
            if result.returncode == 0:
                # Verify output file was created
                if output_path.exists() and output_path.stat().st_size > 0:
                    logger.info(f"Conversion successful: {output_path}")
                    logger.info(f"Output file size: {output_path.stat().st_size / (1024*1024):.2f}MB")
                    if progress_callback:
                        progress_callback("Conversion completed successfully!", 100)
                    return True
                else:
                    logger.error("Conversion failed: Output file not created or empty")
                    if progress_callback:
                        progress_callback("Conversion failed: Output file not created", 0)
                    return False
            else:
                logger.error(f"FFmpeg error (code {result.returncode}): {result.stderr}")
                if progress_callback:
                    progress_callback(f"FFmpeg error: {result.stderr[:50]}...", 0)
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Conversion timed out")
            if progress_callback:
                progress_callback("Conversion timed out", 0)
            return False
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            if progress_callback:
                progress_callback(f"Error: {str(e)}", 0)
            return False
    
    def convert_batch(self, input_files: List[str], output_format: str = '.mp3',
                     output_dir: Optional[str] = None, bitrate: str = '192k',
                     quality: str = 'high', progress_callback=None) -> List[bool]:
        """
        Convert multiple files in batch.
        
        Args:
            input_files: List of input file paths
            output_format: Output format (.mp3 or .wav)
            output_dir: Output directory (optional)
            bitrate: Audio bitrate
            quality: Conversion quality
            progress_callback: Optional callback for progress updates
            
        Returns:
            List[bool]: Success status for each file
        """
        results = []
        total_files = len(input_files)
        
        for i, input_file in enumerate(input_files):
            logger.info(f"Processing file {i + 1}/{total_files}: {input_file}")
            
            if progress_callback:
                progress_callback(f"Processing file {i + 1}/{total_files}: {Path(input_file).name}", 
                                (i / total_files) * 100)
            
            success = self.convert_file(input_file, output_format, output_dir, bitrate, quality)
            results.append(success)
            
        successful = sum(results)
        logger.info(f"Batch conversion complete: {successful}/{total_files} files converted successfully")
        
        if progress_callback:
            progress_callback(f"Batch complete: {successful}/{total_files} files converted", 100)
        
        return results
