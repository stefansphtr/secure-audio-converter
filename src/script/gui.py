"""
GUI Application for the Secure Audio Converter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import logging
from pathlib import Path
from typing import List, Optional

from converter_core import SecureAudioConverter
from config import *

logger = logging.getLogger(__name__)

class ConverterGUI:
    """Main GUI application for the audio converter."""
    
    def __init__(self, root):
        self.root = root
        self.converter = None
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.setup_layout()
        
        # Thread communication
        self.progress_queue = queue.Queue()
        self.root.after(100, self.check_progress_queue)
        
        # Initialize converter
        self.initialize_converter()
    
    def setup_window(self):
        """Configure the main window."""
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=THEME_COLOR)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
    
    def setup_variables(self):
        """Initialize tkinter variables."""
        self.input_files = []
        self.output_format = tk.StringVar(value=DEFAULT_FORMAT)
        self.output_dir = tk.StringVar()
        self.bitrate = tk.StringVar(value=DEFAULT_BITRATE)
        self.quality = tk.StringVar(value=DEFAULT_QUALITY)
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
    
    def setup_widgets(self):
        """Create and configure all widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # File selection frame
        self.file_frame = ttk.LabelFrame(self.main_frame, text="Input Files", padding="10")
        
        self.file_listbox = tk.Listbox(self.file_frame, height=6, width=70)
        self.file_scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical")
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)
        self.file_scrollbar.config(command=self.file_listbox.yview)
        
        self.add_files_btn = ttk.Button(self.file_frame, text="Add Files", 
                                       command=self.add_files)
        self.remove_files_btn = ttk.Button(self.file_frame, text="Remove Selected", 
                                          command=self.remove_files)
        self.clear_files_btn = ttk.Button(self.file_frame, text="Clear All", 
                                         command=self.clear_files)
        
        # Settings frame
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Conversion Settings", padding="10")
        
        # Output format
        ttk.Label(self.settings_frame, text="Output Format:").grid(row=0, column=0, sticky="w", padx=5)
        format_frame = ttk.Frame(self.settings_frame)
        ttk.Radiobutton(format_frame, text="MP3", variable=self.output_format, 
                       value="mp3").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="WAV", variable=self.output_format, 
                       value="wav").pack(side="left", padx=5)
        
        # Bitrate
        ttk.Label(self.settings_frame, text="Bitrate:").grid(row=1, column=0, sticky="w", padx=5)
        self.bitrate_combo = ttk.Combobox(self.settings_frame, textvariable=self.bitrate, 
                                         values=BITRATE_OPTIONS, state="readonly", width=10)
        
        # Quality
        ttk.Label(self.settings_frame, text="Quality:").grid(row=2, column=0, sticky="w", padx=5)
        self.quality_combo = ttk.Combobox(self.settings_frame, textvariable=self.quality, 
                                         values=list(QUALITY_PRESETS.keys()), state="readonly", width=10)
        
        # Output directory
        ttk.Label(self.settings_frame, text="Output Directory:").grid(row=3, column=0, sticky="w", padx=5)
        self.output_dir_entry = ttk.Entry(self.settings_frame, textvariable=self.output_dir, width=40)
        self.browse_output_btn = ttk.Button(self.settings_frame, text="Browse", 
                                           command=self.browse_output_dir)
        
        # Progress frame
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.status_label = ttk.Label(self.progress_frame, textvariable=self.status_var)
        
        # Control frame
        self.control_frame = ttk.Frame(self.main_frame)
        
        self.convert_btn = ttk.Button(self.control_frame, text="Start Conversion", 
                                     command=self.start_conversion, style="Accent.TButton")
        self.stop_btn = ttk.Button(self.control_frame, text="Stop", 
                                  command=self.stop_conversion, state="disabled")
        
        # Info frame
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Information", padding="10")
        self.info_text = tk.Text(self.info_frame, height=8, width=70, wrap="word")
        self.info_scrollbar = ttk.Scrollbar(self.info_frame, orient="vertical")
        self.info_text.config(yscrollcommand=self.info_scrollbar.set)
        self.info_scrollbar.config(command=self.info_text.yview)
        
    def setup_layout(self):
        """Arrange widgets in the window."""
        self.main_frame.pack(fill="both", expand=True)
        
        # File selection
        self.file_frame.pack(fill="both", expand=True, pady=5)
        
        file_list_frame = ttk.Frame(self.file_frame)
        file_list_frame.pack(fill="both", expand=True)
        
        self.file_listbox.pack(side="left", fill="both", expand=True)
        self.file_scrollbar.pack(side="right", fill="y")
        
        file_btn_frame = ttk.Frame(self.file_frame)
        file_btn_frame.pack(fill="x", pady=5)
        
        self.add_files_btn.pack(side="left", padx=5)
        self.remove_files_btn.pack(side="left", padx=5)
        self.clear_files_btn.pack(side="left", padx=5)
        
        # Settings
        self.settings_frame.pack(fill="x", pady=5)
        
        format_frame = ttk.Frame(self.settings_frame)
        format_frame.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Radiobutton(format_frame, text="MP3", variable=self.output_format, 
                       value="mp3").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="WAV", variable=self.output_format, 
                       value="wav").pack(side="left", padx=5)
        
        self.bitrate_combo.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.quality_combo.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        output_dir_frame = ttk.Frame(self.settings_frame)
        output_dir_frame.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self.output_dir_entry.grid(row=0, column=0, padx=(0, 5))
        self.browse_output_btn.grid(row=0, column=1)
        
        # Progress
        self.progress_frame.pack(fill="x", pady=5)
        self.progress_bar.pack(fill="x", pady=2)
        self.status_label.pack(anchor="w")
        
        # Controls
        self.control_frame.pack(fill="x", pady=5)
        self.convert_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)
        
        # Info
        self.info_frame.pack(fill="both", expand=True, pady=5)
        
        info_content_frame = ttk.Frame(self.info_frame)
        info_content_frame.pack(fill="both", expand=True)
        
        self.info_text.pack(side="left", fill="both", expand=True)
        self.info_scrollbar.pack(side="right", fill="y")
    
    def initialize_converter(self):
        """Initialize the converter and check FFmpeg."""
        try:
            self.converter = SecureAudioConverter()
            self.log_info("Audio converter initialized successfully")
            self.log_info(f"FFmpeg found at: {self.converter.ffmpeg_path}")
        except Exception as e:
            self.log_error(f"Failed to initialize converter: {e}")
            messagebox.showerror("Error", f"Failed to initialize converter:\n{e}")
    
    def add_files(self):
        """Add files to the conversion list."""
        files = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[
                ("Video files", "*.mp4 *.m4v *.mov *.avi *.mkv"),
                ("MP4 files", "*.mp4"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
        
        self.log_info(f"Added {len(files)} files to conversion list")
    
    def remove_files(self):
        """Remove selected files from the list."""
        selected = self.file_listbox.curselection()
        for index in reversed(selected):
            self.file_listbox.delete(index)
            del self.input_files[index]
        
        self.log_info(f"Removed {len(selected)} files from list")
    
    def clear_files(self):
        """Clear all files from the list."""
        self.file_listbox.delete(0, tk.END)
        self.input_files.clear()
        self.log_info("Cleared all files from list")
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir.set(directory)
    
    def start_conversion(self):
        """Start the conversion process."""
        if not self.input_files:
            messagebox.showwarning("Warning", "Please add files to convert")
            return
        
        if not self.converter:
            messagebox.showerror("Error", "Converter not initialized")
            return
        
        # Disable UI during conversion
        self.convert_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        # Start conversion in thread
        self.conversion_thread = threading.Thread(target=self.run_conversion, daemon=True)
        self.conversion_thread.start()
    
    def run_conversion(self):
        """Run the conversion process in a separate thread."""
        try:
            output_format = f".{self.output_format.get()}"
            output_dir = self.output_dir.get() if self.output_dir.get() else None
            bitrate = self.bitrate.get()
            quality = self.quality.get()
            
            def progress_callback(message, progress):
                self.progress_queue.put(("progress", message, progress))
            
            if len(self.input_files) == 1:
                # Single file conversion
                success = self.converter.convert_file(
                    self.input_files[0],
                    output_format,
                    output_dir,
                    bitrate,
                    quality,
                    progress_callback
                )
                
                if success:
                    self.progress_queue.put(("complete", "Conversion completed successfully!", 100))
                else:
                    self.progress_queue.put(("error", "Conversion failed", 0))
            else:
                # Batch conversion
                results = self.converter.convert_batch(
                    self.input_files,
                    output_format,
                    output_dir,
                    bitrate,
                    quality,
                    progress_callback
                )
                
                successful = sum(results)
                total = len(results)
                
                if successful == total:
                    self.progress_queue.put(("complete", f"All {total} files converted successfully!", 100))
                else:
                    self.progress_queue.put(("warning", f"{successful}/{total} files converted", 100))
        
        except Exception as e:
            self.progress_queue.put(("error", f"Conversion error: {e}", 0))
        finally:
            self.progress_queue.put(("finished", "", 0))
    
    def stop_conversion(self):
        """Stop the conversion process."""
        # Note: This is a simplified implementation
        # In a real application, you'd need to properly terminate the ffmpeg process
        self.log_info("Stop requested - conversion will finish current file")
        self.stop_btn.config(state="disabled")
    
    def check_progress_queue(self):
        """Check for progress updates from the conversion thread."""
        try:
            while True:
                event_type, message, progress = self.progress_queue.get_nowait()
                
                if event_type == "progress":
                    self.status_var.set(message)
                    self.progress_var.set(progress)
                elif event_type == "complete":
                    self.status_var.set(message)
                    self.progress_var.set(progress)
                    self.log_info(message)
                elif event_type == "error":
                    self.status_var.set(message)
                    self.progress_var.set(progress)
                    self.log_error(message)
                elif event_type == "warning":
                    self.status_var.set(message)
                    self.progress_var.set(progress)
                    self.log_warning(message)
                elif event_type == "finished":
                    # Re-enable UI
                    self.convert_btn.config(state="normal")
                    self.stop_btn.config(state="disabled")
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_progress_queue)
    
    def log_info(self, message):
        """Add info message to the log."""
        self._add_log_message("INFO", message)
    
    def log_warning(self, message):
        """Add warning message to the log."""
        self._add_log_message("WARNING", message)
    
    def log_error(self, message):
        """Add error message to the log."""
        self._add_log_message("ERROR", message)
    
    def _add_log_message(self, level, message):
        """Add a message to the info text widget."""
        self.info_text.insert(tk.END, f"[{level}] {message}\n")
        self.info_text.see(tk.END)
        self.root.update_idletasks()


def main():
    """Main function to run the GUI application."""
    # Setup logging
    setup_logging()
    
    # Create and run the GUI
    root = tk.Tk()
    app = ConverterGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Error", f"Application error: {e}")


if __name__ == "__main__":
    main()
