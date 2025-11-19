# Text-to-Talking Avatar Video Generator

A full-stack application for generating talking avatar videos from text input. This project uses:
- **Django backend** (Python) for video generation with TTS (Text-to-Speech) and avatar synthesis
- **React frontend** (Node.js/npm) for the user interface
- **Local ML models** only - no external SaaS APIs required

## 🚀 Quick Start

**New to the project?** See [QUICKSTART.md](QUICKSTART.md) for step-by-step setup instructions!

## Architecture

```
TEXTSPEAKER/
├── videogen_backend/          # Django backend (Python ML)
│   ├── manage.py
│   ├── requirements.txt
│   ├── videogen_backend/      # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   └── api/                   # API app
│       ├── views.py           # Video generation endpoint
│       ├── serializers.py     # Input validation
│       └── urls.py
│
└── video-avatar-frontend/     # React frontend
    ├── package.json
    ├── public/
    └── src/
        ├── App.js             # Main UI component
        └── index.js
```

## Features

### Interactive Web Interface
- Text input form in React UI
- Django REST API endpoint `/api/generatevideo/`
- Video playback and download in browser
- CORS-enabled for local development
- Media file serving for generated videos

### Batch Processing from CSV
- **NEW**: Automatically generate multiple videos from CSV file
- Process dozens or hundreds of text entries at once
- Customizable filenames and output directory
- Progress tracking and error reporting
- See [CSV_VIDEO_GUIDE.md](CSV_VIDEO_GUIDE.md) for detailed instructions

### Video Generation
- Text-to-Speech (TTS) conversion (placeholder for real TTS integration)
- Avatar video generation (placeholder for Wav2Lip/SadTalker integration)
- MoviePy-based video creation
- Support for custom avatar images

## Setup Instructions

### Prerequisites

- Python 3.8+ (for Django backend)
- Node.js 14+ and npm (for React frontend)
- pip (Python package manager)

### Backend Setup (Django)

1. Navigate to the backend directory:
   ```bash
   cd videogen_backend
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. (Optional) Create a superuser for Django admin:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the Django development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

   The backend API will be available at `http://127.0.0.1:8000/`

### Frontend Setup (React)

1. Navigate to the frontend directory:
   ```bash
   cd video-avatar-frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will open automatically at `http://localhost:3000/`

## Usage

### Method 1: Batch Processing from CSV (Recommended for Multiple Videos)

Generate multiple videos at once from a CSV file:

```bash
# Quick start with sample data
python generate_videos.py sample_texts.csv

# Custom output directory
python generate_videos.py your_texts.csv --output-dir my_videos

# Use custom avatar
python generate_videos.py your_texts.csv --avatar path/to/avatar.png
```

**CSV Format:**
```csv
text,filename,avatar
"Your text here","video_name",
"More text","another_video",
```

See [CSV_VIDEO_GUIDE.md](CSV_VIDEO_GUIDE.md) for complete documentation on batch processing.

### Method 2: Interactive Web Interface (For Single Videos)

1. Ensure both backend (Django on port 8000) and frontend (React on port 3000) are running
2. Open your browser to `http://localhost:3000`
3. Enter text in the textarea
4. Click "Generate Video"
5. Wait for processing (the video will appear when ready)
6. Play or download the generated video

## ML Model Integration

The application includes placeholder functions for ML models. To use real models:

### Text-to-Speech (TTS)

In `videogen_backend/api/views.py`, uncomment the TTS initialization:

```python
from TTS.api import TTS
TTS_MODEL_NAME = "tts_models/en/ljspeech/tacotron2-DDC"
tts_model = TTS(TTS_MODEL_NAME)
```

And in the `text_to_speech()` function:
```python
tts_model.tts_to_file(text=text, file_path=str(out_wav_path))
```

Install the TTS library:
```bash
pip install TTS
```

### Avatar Video Generation

Replace the placeholder in `generate_talking_avatar()` function with your chosen model:

**For Wav2Lip:**
```python
from wav2lip_inference import make_talking_video
make_talking_video(
    face_image=str(avatar_img),
    audio=str(audio_path),
    outfile=str(out_video_path),
)
```

**For SadTalker or other models:**
Follow the specific model's inference API and integrate accordingly.

### Avatar Image

Place your avatar image at:
```
videogen_backend/avatar/avatar.png
```

The directory will be created automatically when the backend starts.

## API Endpoints

### POST /api/generatevideo/

Generate a talking avatar video from text.

**Request:**
```json
{
  "text": "Hello, world!"
}
```

**Response (Success):**
```json
{
  "video_url": "/media/video/<uuid>.mp4"
}
```

**Response (Error):**
```json
{
  "detail": "Error message"
}
```

## Development Notes

- CORS is enabled for all origins in development (see `settings.py`)
- Media files are stored in `videogen_backend/media/`
- Audio files: `media/audio/`
- Video files: `media/video/`
- Database uses SQLite by default
- Both servers run in development mode with hot-reload

## Production Deployment

Before deploying to production:

1. Update Django settings:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Restrict `CORS_ALLOW_ALL_ORIGINS` and use `CORS_ALLOWED_ORIGINS`
   - Use a production database (PostgreSQL, MySQL)
   - Set a strong `SECRET_KEY`

2. Build React for production:
   ```bash
   cd video-avatar-frontend
   npm run build
   ```

3. Serve React build with Django or a web server (nginx, Apache)

4. Use a production WSGI server (gunicorn, uWSGI)

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
