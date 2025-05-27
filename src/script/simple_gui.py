"""
Simple GUI Test for the Audio Converter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import logging
from pathlib import Path

from converter_core import SecureAudioConverter
from config import setup_logging, APP_NAME, APP_VERSION

logger = logging.getLogger(__name__)

class SimpleConverterGUI:
    """Simple GUI for testing the audio converter."""
    
    def __init__(self, root):
        self.root = root
        self.converter = None
        self.input_files = []
        
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.initialize_converter()
    
    def setup_window(self):
        """Configure the main window."""
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("600x400")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (300)
        y = (self.root.winfo_screenheight() // 2) - (200)
        self.root.geometry(f"+{x}+{y}")
    
    def setup_variables(self):
        """Initialize tkinter variables."""
        self.output_format = tk.StringVar(value="mp3")
        self.output_dir = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
    
    def setup_widgets(self):
        """Create and configure widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"{APP_NAME}", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Select Files", padding="10")
        file_frame.pack(fill="both", expand=True, pady=5)
        
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.pack(fill="both", expand=True, pady=5)
        
        file_btn_frame = ttk.Frame(file_frame)
        file_btn_frame.pack(fill="x")
        
        ttk.Button(file_btn_frame, text="Add Files", command=self.add_files).pack(side="left", padx=5)
        ttk.Button(file_btn_frame, text="Clear", command=self.clear_files).pack(side="left", padx=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill="x", pady=5)
        
        # Format selection
        format_frame = ttk.Frame(settings_frame)
        format_frame.pack(fill="x", pady=2)
        
        ttk.Label(format_frame, text="Format:").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="MP3", variable=self.output_format, value="mp3").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="WAV", variable=self.output_format, value="wav").pack(side="left", padx=5)
        
        # Output directory
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill="x", pady=2)
        
        ttk.Label(output_frame, text="Output Dir:").pack(side="left", padx=5)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=30).pack(side="left", padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).pack(side="left", padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=10)
        
        self.convert_btn = ttk.Button(control_frame, text="Convert Files", command=self.start_conversion)
        self.convert_btn.pack(side="left", padx=5)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", pady=5)
        
        ttk.Label(status_frame, text="Status:").pack(side="left")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left", padx=10)
    
    def initialize_converter(self):
        """Initialize the converter."""
        try:
            self.converter = SecureAudioConverter()
            self.status_var.set("Ready - FFmpeg found")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to initialize converter:\n{e}")
    
    def add_files(self):
        """Add files to the conversion list."""
        files = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[
                ("Video files", "*.mp4 *.m4v *.mov *.avi *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
        
        self.status_var.set(f"Added {len(files)} files")
    
    def clear_files(self):
        """Clear all files."""
        self.file_listbox.delete(0, tk.END)
        self.input_files.clear()
        self.status_var.set("Files cleared")
    
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
        
        # Disable button during conversion
        self.convert_btn.config(state="disabled")
        
        # Start conversion in thread
        threading.Thread(target=self.run_conversion, daemon=True).start()
    
    def run_conversion(self):
        """Run the conversion process."""
        try:
            output_format = f".{self.output_format.get()}"
            output_dir = self.output_dir.get() if self.output_dir.get() else None
            
            successful = 0
            total = len(self.input_files)
            
            for i, input_file in enumerate(self.input_files):
                self.root.after(0, lambda: self.status_var.set(f"Converting {i+1}/{total}..."))
                
                success = self.converter.convert_file(
                    input_file,
                    output_format,
                    output_dir,
                    "192k",
                    "high"
                )
                
                if success:
                    successful += 1
            
            # Update UI in main thread
            self.root.after(0, lambda: self.status_var.set(f"Complete: {successful}/{total} files converted"))
            self.root.after(0, lambda: self.convert_btn.config(state="normal"))
            
            if successful == total:
                self.root.after(0, lambda: messagebox.showinfo("Success", f"All {total} files converted successfully!"))
            else:
                self.root.after(0, lambda: messagebox.showwarning("Partial Success", f"{successful}/{total} files converted"))
        
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {e}"))
            self.root.after(0, lambda: self.convert_btn.config(state="normal"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Conversion failed: {e}"))

def main():
    """Main function to run the simple GUI."""
    setup_logging()
    
    root = tk.Tk()
    app = SimpleConverterGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Error", f"Application error: {e}")

if __name__ == "__main__":
    main()
