# Quick Reference: CSV to Video Generation

## Fastest Way to Get Started

```bash
# 1. Install dependencies
cd videogen_backend
pip install -r requirements.txt

# 2. Go back to project root
cd ..

# 3. Generate videos from sample CSV
python generate_videos.py sample_texts.csv
```

Your videos will be in the `output/` directory!

## CSV Format

Create a file like `my_texts.csv`:

```csv
text,filename,avatar
"Hello world! This is my first video.","intro",
"Thanks for watching!","outro",
```

Then run:
```bash
python generate_videos.py my_texts.csv
```

## Common Commands

```bash
# Validate CSV without generating
python generate_videos.py my_texts.csv --validate-only

# Specify output directory
python generate_videos.py my_texts.csv --output-dir my_videos

# Use custom avatar
python generate_videos.py my_texts.csv --avatar my_avatar.png

# Get help
python generate_videos.py --help
```

## What You Get

- MP4 videos with your avatar and audio
- Customizable filenames
- Progress tracking
- Error reporting

## Next Steps

1. **Replace TTS**: Edit `videogen_backend/api/batch_generator.py` to use real Text-to-Speech
2. **Add Lip-Sync**: Integrate Wav2Lip or SadTalker for animated talking
3. **Customize Avatar**: Replace `videogen_backend/avatar/avatar.png`

For complete documentation, see [CSV_VIDEO_GUIDE.md](CSV_VIDEO_GUIDE.md)
