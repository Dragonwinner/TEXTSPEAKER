# Quick Start Guide

This guide will help you get the Text-to-Avatar Video Generator running on your local machine.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher and npm
- Git

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dragonwinner/TEXTSPEAKER.git
cd TEXTSPEAKER
```

### 2. Set Up the Django Backend

```bash
# Navigate to backend directory
cd videogen_backend

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the Django server
python manage.py runserver 0.0.0.0:8000
```

The backend API will now be running at `http://127.0.0.1:8000/`

### 3. Set Up the React Frontend (in a new terminal)

```bash
# From the project root, navigate to frontend directory
cd video-avatar-frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will automatically open in your browser at `http://localhost:3000/`

### 4. Test the Application

1. Open your browser to `http://localhost:3000/`
2. Enter text in the textarea (e.g., "Hello, world!")
3. Click "Generate Video"
4. You should see an error message indicating TTS/video generation is not yet implemented - this is expected!

## Next Steps: Adding ML Models

To make the application fully functional, you need to integrate real ML models:

### Add Text-to-Speech (TTS)

1. Install the TTS library:
   ```bash
   pip install TTS
   ```

2. Edit `videogen_backend/api/views.py`:
   - Uncomment the TTS import and initialization lines at the top
   - Uncomment the TTS call in the `text_to_speech()` function

### Add Avatar Video Generation

1. Install your chosen model (e.g., Wav2Lip, SadTalker)
   ```bash
   # Example for Wav2Lip
   pip install opencv-python librosa
   # ... additional dependencies as needed
   ```

2. Add your avatar image:
   ```bash
   # Place your avatar image at:
   # videogen_backend/avatar/avatar.png
   ```

3. Edit `videogen_backend/api/views.py`:
   - Replace the placeholder in `generate_talking_avatar()` with your model's inference code

## Troubleshooting

### Port Already in Use

If port 8000 or 3000 is already in use:

**Django:**
```bash
python manage.py runserver 0.0.0.0:8001
```

**React:**
Update the fetch URL in `video-avatar-frontend/src/App.js` to match your Django port.

### CORS Issues

If you see CORS errors in the browser console, ensure:
- Django server is running on `http://127.0.0.1:8000`
- React is making requests to the correct URL
- `CORS_ALLOW_ALL_ORIGINS = True` is set in Django settings

### Dependencies Issues

For Python dependency issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

For Node dependency issues:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Architecture Overview

```
User Browser (localhost:3000)
         ↓
    React Frontend
         ↓ (POST /api/generatevideo/)
    Django Backend (localhost:8000)
         ↓
    1. Text → TTS → audio.wav
    2. avatar.png + audio.wav → Wav2Lip/SadTalker → video.mp4
         ↓
    Response: { video_url: "/media/video/<id>.mp4" }
         ↓
    Video displayed in browser
```

All processing happens locally - no external API calls!

## Development Tips

- Both servers support hot-reload - your changes will automatically refresh
- Media files are stored in `videogen_backend/media/`
- Check `videogen_backend/media/audio/` and `videogen_backend/media/video/` for generated files
- Use Django admin at `http://127.0.0.1:8000/admin/` (create superuser with `python manage.py createsuperuser`)

## Further Reading

- See [README.md](README.md) for complete documentation
- See [ORIGINAL_SPEC.md](ORIGINAL_SPEC.md) for the original project specification
