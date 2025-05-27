# Deployment Guide

## Local Deployment

### Running the Streamlit App Locally

1. Navigate to the project directory:
   ```bash
   cd "d:\21. Teleperformance\Tools"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Open your browser and navigate to the displayed URL (usually `http://localhost:8501`)

## Cloud Deployment (Streamlit Cloud)

### Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free at https://share.streamlit.io/)

### Step-by-Step Deployment

1. **Prepare Your Repository**
   - Push all your code to a GitHub repository
   - Ensure `requirements.txt` is in the root directory
   - Ensure `streamlit_app.py` is in the root directory

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy!"

3. **Configuration**
   - The app will automatically install dependencies from `requirements.txt`
   - FFmpeg is pre-installed on Streamlit Cloud

### Important Notes for Cloud Deployment

1. **File Size Limits**: Streamlit Cloud has upload limits. The app is configured with a 500MB limit, but you may need to adjust based on your hosting platform.

2. **FFmpeg**: Our app uses FFmpeg for audio conversion. Streamlit Cloud includes FFmpeg by default.

3. **Temporary Files**: The app creates temporary files during conversion. These are automatically cleaned up after processing.

4. **Security**: The app includes comprehensive security measures:
   - File type validation
   - Size limits
   - Path sanitization
   - SHA256 integrity checks

## Alternative Deployment Options

### 1. Heroku
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

### 2. Railway
```bash
# Create railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"
  }
}
```

### 3. Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Sharing with Colleagues

Once deployed, you can share the URL with your colleagues. They will be able to:

1. Upload MP4 files through the web interface
2. Select output format (MP3 or WAV)
3. Choose quality settings
4. Download converted files individually or as a ZIP package
5. Process multiple files in batch

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Ensure FFmpeg is installed on your system or deployment platform
2. **File upload fails**: Check file size limits and ensure the file is a valid MP4
3. **Conversion fails**: Verify the input file is not corrupted and is a valid video file
4. **Memory issues**: Large files may cause memory issues on free hosting platforms

### Support

For issues or questions, check the logs in the Streamlit interface or contact Stefan.

---
Made with 🔥 by Stefan
