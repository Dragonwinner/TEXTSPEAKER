# Text-to-Talking Avatar Video Generator

A full-stack application for generating talking avatar videos from text input. This project uses:
- **Django backend** (Python) for video generation with TTS (Text-to-Speech) and avatar synthesis
- **React frontend** (Node.js/npm) for the user interface
- **Local ML models** only - no external SaaS APIs required

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

- Text input form in React UI
- Django REST API endpoint `/api/generatevideo/`
- Text-to-Speech (TTS) conversion using Coqui TTS
- Avatar video generation (placeholder for Wav2Lip/SadTalker integration)
- Video playback and download in browser
- CORS-enabled for local development
- Media file serving for generated videos

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
