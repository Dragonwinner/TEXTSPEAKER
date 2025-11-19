# CSV to Video Generation Guide

This guide explains how to automatically generate videos from text entries in a CSV file.

## Overview

The system reads text entries from a CSV file and generates videos where an avatar "speaks" each text entry. Videos are saved to an output folder with customizable filenames.

## Features

- **Batch Processing**: Generate multiple videos from a single CSV file
- **Custom Filenames**: Specify custom names for output videos
- **Placeholder TTS**: Uses simple audio generation (can be replaced with real TTS)
- **Placeholder Avatar**: Uses static image with audio (can be replaced with Wav2Lip/SadTalker)
- **Progress Tracking**: See real-time progress as videos are generated
- **Error Handling**: Gracefully handles errors and reports failed entries

## CSV Format

Your CSV file should have a header row with at least a `text` column:

```csv
text,filename,avatar
"Your text here","custom_name",
"More text","another_video",
```

### Columns:

1. **text** (required): The text to be spoken by the avatar
2. **filename** (optional): Custom filename for the output video (without .mp4 extension)
   - If not provided, videos are named `video_1.mp4`, `video_2.mp4`, etc.
3. **avatar** (optional): Path to a specific avatar image for this entry
   - If not provided, uses the default avatar at `videogen_backend/avatar/avatar.png`

### Example CSV:

See `sample_texts.csv` in the project root for a working example.

## Usage Methods

### Method 1: Standalone Script (Recommended for Quick Use)

The easiest way to generate videos:

```bash
python generate_videos.py sample_texts.csv
```

This will:
- Read entries from `sample_texts.csv`
- Generate videos in the `output/` directory
- Show progress for each video

#### Options:

```bash
# Specify output directory
python generate_videos.py sample_texts.csv --output-dir my_videos

# Use a custom avatar image
python generate_videos.py sample_texts.csv --avatar path/to/avatar.png

# Validate CSV without generating videos
python generate_videos.py sample_texts.csv --validate-only
```

#### Full Command Help:

```bash
python generate_videos.py --help
```

### Method 2: Django Management Command

If you're working within the Django project:

```bash
cd videogen_backend
python manage.py generate_videos_from_csv ../sample_texts.csv
```

#### Options:

```bash
# Specify output directory
python manage.py generate_videos_from_csv ../sample_texts.csv --output-dir ../my_videos

# Use a custom avatar
python manage.py generate_videos_from_csv ../sample_texts.csv --avatar ../custom_avatar.png

# Validate only
python manage.py generate_videos_from_csv ../sample_texts.csv --validate-only
```

## Output Structure

After running the script, you'll find:

```
output/
├── welcome_video.mp4     # Generated videos
├── tech_demo.mp4
├── use_cases.mp4
└── temp_audio/           # Intermediate audio files
    ├── welcome_video_abc123.wav
    ├── tech_demo_def456.wav
    └── ...
```

## Workflow

For each text entry in the CSV:

1. **Text to Speech**: Converts text to audio WAV file
   - Currently uses a placeholder beep audio
   - Duration is based on text length (approx. 5 words per second)
   
2. **Avatar Video Generation**: Creates video from avatar image + audio
   - Uses MoviePy to combine static avatar image with audio
   - Currently shows static image (can be replaced with lip-sync models)
   
3. **Output**: Saves MP4 video with specified filename

## Customization

### Using Real TTS (Text-to-Speech)

To replace the placeholder audio with real speech:

1. Install a TTS library (e.g., Coqui TTS, pyttsx3, gTTS):
   ```bash
   pip install TTS
   ```

2. Edit `videogen_backend/api/batch_generator.py`

3. Replace the `text_to_speech_placeholder()` function:
   ```python
   def text_to_speech_placeholder(text: str, out_wav_path: Path):
       from TTS.api import TTS
       tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
       tts.tts_to_file(text=text, file_path=str(out_wav_path))
   ```

### Using Real Avatar Animation (Lip-Sync)

To add lip-sync animation:

1. Install Wav2Lip or SadTalker following their instructions

2. Edit `videogen_backend/api/batch_generator.py`

3. Replace the `generate_placeholder_video()` function with your model's inference code

### Custom Avatar Image

Place your avatar image at:
```
videogen_backend/avatar/avatar.png
```

Or specify it per-video in the CSV or via command-line:
```bash
python generate_videos.py texts.csv --avatar my_avatar.png
```

## Troubleshooting

### CSV Validation Failed

Make sure your CSV:
- Has a header row with a `text` column
- Uses proper CSV formatting (quoted strings for text with commas)
- Is UTF-8 encoded

### Video Generation Failed

Check that:
- MoviePy and its dependencies are installed: `pip install moviepy`
- FFmpeg is installed on your system (MoviePy requires it)
- The avatar image exists and is readable
- You have write permissions in the output directory

### Audio/Video Quality Issues

The current implementation uses:
- Simple beep audio (placeholder for TTS)
- Static image video (placeholder for lip-sync)

For production use, replace with real TTS and avatar animation models.

## Performance

- Processing time depends on:
  - Number of entries in CSV
  - Text length (affects audio duration)
  - TTS model speed (if using real TTS)
  - Avatar model speed (if using real lip-sync)

- The placeholder implementation is fast (~1-2 seconds per video)
- Real TTS + lip-sync models will be slower (10-30 seconds per video depending on hardware)

## Examples

### Basic Usage:

```bash
# Generate from sample CSV
python generate_videos.py sample_texts.csv

# Output:
# - output/welcome_video.mp4
# - output/tech_demo.mp4
# - output/use_cases.mp4
# - output/how_to_use.mp4
# - output/thank_you.mp4
```

### Custom Configuration:

```bash
# Generate with custom settings
python generate_videos.py my_data.csv \
  --output-dir production_videos \
  --avatar corporate_avatar.png
```

### Validation Before Generation:

```bash
# Check CSV format first
python generate_videos.py large_dataset.csv --validate-only

# If valid, generate videos
python generate_videos.py large_dataset.csv --output-dir batch_output
```

## Next Steps

1. Try the sample CSV: `python generate_videos.py sample_texts.csv`
2. Create your own CSV with your text content
3. Customize the avatar image
4. Integrate real TTS and lip-sync models for production use

## Support

For issues or questions:
- Check that all dependencies are installed
- Verify CSV format matches the specification
- Review error messages for specific issues
- Ensure sufficient disk space for video output
