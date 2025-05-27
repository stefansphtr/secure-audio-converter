"""
Streamlit Web Application for Secure Audio Converter
Converts MP4 video files to MP3 or WAV audio format with security measures.
"""

import streamlit as st
import tempfile
import os
import zipfile
from pathlib import Path
import logging
from io import BytesIO
import time

# Configure page
st.set_page_config(
    page_title="Secure Audio Converter",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add script directory to path
import sys
script_dir = Path(__file__).parent / "src" / "script"
sys.path.insert(0, str(script_dir))

from converter_core import SecureAudioConverter
from config import setup_logging, APP_NAME, APP_VERSION, QUALITY_PRESETS, BITRATE_OPTIONS

# Setup logging for Streamlit
@st.cache_resource
def setup_streamlit_logging():
    """Setup logging for Streamlit environment."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)

logger = setup_streamlit_logging()

# Initialize converter
@st.cache_resource
def get_converter():
    """Get or create the audio converter instance."""
    try:
        return SecureAudioConverter()
    except Exception as e:
        error_msg = str(e)
        if "FFmpeg not found" in error_msg:
            st.error("⚠️ **FFmpeg not available on this server**")
            st.info("""
            **This is likely a deployment issue. Please:**
            
            1. **For Streamlit Cloud:** Ensure `packages.txt` contains `ffmpeg`
            2. **For other platforms:** Install FFmpeg system-wide
            3. **Local development:** Install FFmpeg from https://ffmpeg.org/
            
            **If you're the administrator:**
            - The `packages.txt` file should install FFmpeg automatically
            - Try redeploying the application
            - Check deployment logs for installation errors
            """)
        else:
            st.error(f"Failed to initialize converter: {e}")
        
        return None

def create_download_link(file_path, filename):
    """Create a download link for the converted file."""
    with open(file_path, "rb") as f:
        data = f.read()
    
    st.download_button(
        label=f"📥 Download {filename}",
        data=data,
        file_name=filename,
        mime="audio/mpeg" if filename.endswith('.mp3') else "audio/wav"
    )

def create_zip_download(file_paths, filenames):
    """Create a ZIP file download for multiple files."""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path, filename in zip(file_paths, filenames):
            if os.path.exists(file_path):
                zip_file.write(file_path, filename)
    
    zip_buffer.seek(0)
    
    st.download_button(
        label="📦 Download All Files (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="converted_audio_files.zip",
        mime="application/zip"
    )

def main():
    """Main Streamlit application."""
      # Header
    st.title("🎵 Secure Audio Converter")
    st.markdown(
        "<div style='text-align: left; margin-top: -10px; margin-bottom: 20px;'>"
        "<p style='color: #ff6b6b; font-size: 18px; margin: 0;'>Made with 🔥 by Stefan</p>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(f"**{APP_NAME} v{APP_VERSION}**")
    st.markdown("Convert MP4 video files to MP3 or WAV audio format securely")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Conversion Settings")
    
    # Output format
    output_format = st.sidebar.selectbox(
        "Output Format",
        ["mp3", "wav"],
        help="Choose the output audio format"
    )
    
    # Quality settings (only for MP3)
    if output_format == "mp3":
        quality = st.sidebar.selectbox(
            "Quality",
            list(QUALITY_PRESETS.keys()),
            index=0,  # Default to 'high'
            help="Audio quality level"
        )
        
        bitrate = st.sidebar.selectbox(
            "Bitrate",
            BITRATE_OPTIONS,
            index=1,  # Default to '192k'
            help="Audio bitrate (higher = better quality, larger file)"
        )
    else:
        quality = "high"
        bitrate = "192k"
    
    # Show quality description
    if output_format == "mp3" and quality in QUALITY_PRESETS:
        st.sidebar.info(f"Quality: {QUALITY_PRESETS[quality]['description']}")
    
    # Security information
    st.sidebar.header("🔒 Security Info")
    st.sidebar.info(f"""
    **File Limits:**
    - Max size: 500MB per file
    - Max batch: 50 files
    - Allowed formats: MP4, M4V, MOV, AVI, MKV
    
    **Security Features:**
    - Input validation
    - Path sanitization
    - File integrity checks
    - Process timeout protection
    """)
      # Initialize converter
    converter = get_converter()
    
    if not converter:
        st.error("⚠️ **Audio Converter Not Available**")
        st.markdown("""
        ### 🔧 **For Administrators:**
        
        This application requires **FFmpeg** to be installed on the server.
        
        **Streamlit Cloud Setup:**
        1. Ensure `packages.txt` file exists in repository root
        2. File should contain: `ffmpeg`
        3. Redeploy the application
        
        **Local Setup:**
        ```bash
        # Windows (Chocolatey)
        choco install ffmpeg
        
        # Windows (winget)  
        winget install FFmpeg.FFmpeg
        
        # Linux (Ubuntu/Debian)
        sudo apt update && sudo apt install ffmpeg
        
        # macOS (Homebrew)
        brew install ffmpeg
        ```
        
        ### 📞 **For Users:**
        Please contact your system administrator to resolve this issue.
        """)
        st.stop()
    
    # Show FFmpeg status in sidebar
    with st.sidebar:
        st.success(f"✅ FFmpeg Ready")
        if hasattr(converter, 'ffmpeg_path'):
            st.text(f"Path: {converter.ffmpeg_path}")
    
    # Show FFmpeg status (remove old line)
    # st.sidebar.success(f"✅ FFmpeg found: {converter.ffmpeg_path}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 File Upload")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose video files to convert",
            type=['mp4', 'm4v', 'mov', 'avi', 'mkv'],
            accept_multiple_files=True,
            help="Upload MP4, M4V, MOV, AVI, or MKV files (max 500MB each)"
        )
        
        if uploaded_files:
            st.success(f"📂 {len(uploaded_files)} file(s) uploaded")
            
            # Show uploaded files
            with st.expander("📋 Uploaded Files", expanded=True):
                for i, file in enumerate(uploaded_files, 1):
                    file_size = file.size / (1024 * 1024)  # Convert to MB
                    st.write(f"{i}. **{file.name}** ({file_size:.1f} MB)")
            
            # Convert button
            if st.button("🎯 Start Conversion", type="primary", use_container_width=True):
                convert_files(uploaded_files, converter, output_format, quality, bitrate)
    
    with col2:
        st.header("ℹ️ Instructions")
        st.markdown("""
        **How to use:**
        1. 📁 Upload your video files (left panel)
        2. ⚙️ Configure settings (sidebar)
        3. 🎯 Click "Start Conversion"
        4. 📥 Download converted files
        
        **Supported formats:**
        - **Input:** MP4, M4V, MOV, AVI, MKV
        - **Output:** MP3, WAV
        
        **Tips:**
        - 🎵 MP3 is smaller, WAV is higher quality
        - 🚀 Higher bitrate = better quality
        - 📦 Multiple files = ZIP download
        """)

def convert_files(uploaded_files, converter, output_format, quality, bitrate):
    """Convert uploaded files and provide download links."""
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        converted_files = []
        conversion_results = []
        
        total_files = len(uploaded_files)
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # Update progress
                progress = (i / total_files)
                progress_bar.progress(progress)
                status_text.text(f"Processing {uploaded_file.name}... ({i+1}/{total_files})")
                
                # Save uploaded file to temp directory
                input_path = temp_path / uploaded_file.name
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Convert file
                success = converter.convert_file(
                    str(input_path),
                    f".{output_format}",
                    str(temp_path),
                    bitrate,
                    quality
                )
                
                if success:
                    # Find the output file
                    output_filename = input_path.stem + f".{output_format}"
                    output_path = temp_path / output_filename
                    
                    if output_path.exists():
                        # Read the converted file
                        with open(output_path, "rb") as f:
                            converted_data = f.read()
                        
                        converted_files.append({
                            'filename': output_filename,
                            'data': converted_data,
                            'size': len(converted_data)
                        })
                        conversion_results.append(True)
                    else:
                        conversion_results.append(False)
                        st.error(f"❌ Output file not found for {uploaded_file.name}")
                else:
                    conversion_results.append(False)
                    st.error(f"❌ Conversion failed for {uploaded_file.name}")
                    
            except Exception as e:
                conversion_results.append(False)
                st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        # Final progress update
        progress_bar.progress(1.0)
        
        # Show results
        successful = sum(conversion_results)
        status_text.text(f"✅ Conversion complete: {successful}/{total_files} files converted")
        
        if converted_files:
            st.success(f"🎉 Successfully converted {len(converted_files)} file(s)!")
            
            # Show download section
            st.header("📥 Download Converted Files")
            
            if len(converted_files) == 1:
                # Single file download
                file_info = converted_files[0]
                file_size = file_info['size'] / (1024 * 1024)  # Convert to MB
                
                st.write(f"**{file_info['filename']}** ({file_size:.1f} MB)")
                
                st.download_button(
                    label=f"📥 Download {file_info['filename']}",
                    data=file_info['data'],
                    file_name=file_info['filename'],
                    mime="audio/mpeg" if file_info['filename'].endswith('.mp3') else "audio/wav",
                    use_container_width=True
                )
            else:
                # Multiple files - show individual downloads and ZIP option
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Individual Downloads")
                    for file_info in converted_files:
                        file_size = file_info['size'] / (1024 * 1024)
                        st.write(f"**{file_info['filename']}** ({file_size:.1f} MB)")
                        
                        st.download_button(
                            label=f"📥 {file_info['filename']}",
                            data=file_info['data'],
                            file_name=file_info['filename'],
                            mime="audio/mpeg" if file_info['filename'].endswith('.mp3') else "audio/wav",
                            key=f"download_{file_info['filename']}"
                        )
                
                with col2:
                    st.subheader("Bulk Download")
                    
                    # Create ZIP file
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file_info in converted_files:
                            zip_file.writestr(file_info['filename'], file_info['data'])
                    
                    zip_buffer.seek(0)
                    total_size = sum(f['size'] for f in converted_files) / (1024 * 1024)
                    
                    st.write(f"**All files** ({total_size:.1f} MB total)")
                    st.download_button(
                        label="📦 Download All (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name="converted_audio_files.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
        else:
            st.error("❌ No files were converted successfully. Please check the logs and try again.")

    # Footer with Stefan's signature
    st.markdown("---")
    st.markdown(
        "<div style='text-align: right; color: #aac86c; padding: 20px;'>"
        "<p>Made with 🔥 by Stefanus | AI Enthusiast</p>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
