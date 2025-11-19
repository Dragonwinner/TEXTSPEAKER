"""
Batch video generation module for processing multiple text entries.
"""
import uuid
from pathlib import Path
from typing import Dict, Optional
import wave
import struct
import math


def generate_silent_audio(duration_seconds: float, output_path: Path):
    """
    Generate a silent audio WAV file for placeholder purposes.
    
    Args:
        duration_seconds: Duration of audio in seconds
        output_path: Path to save the audio file
    """
    sample_rate = 22050  # Standard sample rate for speech
    num_samples = int(duration_seconds * sample_rate)
    
    with wave.open(str(output_path), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Write silent audio (zeros)
        for _ in range(num_samples):
            wav_file.writeframes(struct.pack('h', 0))


def generate_simple_beep_audio(text: str, output_path: Path):
    """
    Generate a simple beep audio as a placeholder for TTS.
    Duration is based on text length.
    
    Args:
        text: The text content (used to determine duration)
        output_path: Path to save the audio file
    """
    # Estimate duration: ~5 words per second (average speaking rate)
    word_count = len(text.split())
    duration = max(1.0, word_count / 5.0)  # At least 1 second
    
    sample_rate = 22050
    num_samples = int(duration * sample_rate)
    frequency = 440.0  # A4 note
    
    with wave.open(str(output_path), 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Generate a soft beep tone
        for i in range(num_samples):
            # Simple sine wave with decay
            amplitude = 8000 * (1 - i / num_samples)  # Gradual decay
            value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
            wav_file.writeframes(struct.pack('h', value))


def text_to_speech_placeholder(text: str, out_wav_path: Path):
    """
    Placeholder for TTS functionality.
    Generates a simple audio file based on text length.
    
    Args:
        text: The text to convert to speech
        out_wav_path: Path to save the audio file
    """
    print(f"  [TTS Placeholder] Generating audio for: {text[:50]}...")
    
    # Generate simple audio placeholder
    generate_simple_beep_audio(text, out_wav_path)
    
    print(f"  [TTS Placeholder] Audio saved to: {out_wav_path}")


def generate_placeholder_video(avatar_img: Path, audio_path: Path, out_video_path: Path):
    """
    Placeholder for avatar video generation.
    Creates a simple video file using moviepy or fallback method.
    
    Args:
        avatar_img: Path to avatar image
        audio_path: Path to audio file
        out_video_path: Path to save the video
    """
    print(f"  [Video Placeholder] Generating video with audio: {audio_path.name}")
    
    try:
        # Try using moviepy if available
        from moviepy import ImageClip, AudioFileClip
        
        # Load audio to get duration
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        
        # Check if avatar image exists
        if avatar_img.exists():
            # Create video from image
            video = ImageClip(str(avatar_img)).with_duration(duration)
        else:
            # Create a blank video if no avatar
            print(f"  [Video Placeholder] Warning: Avatar image not found at {avatar_img}")
            print(f"  [Video Placeholder] Creating blank video")
            import numpy as np
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            video = ImageClip(blank_frame).with_duration(duration)
        
        # Set audio
        video = video.with_audio(audio)
        
        # Write video file
        video.write_videofile(
            str(out_video_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            logger=None  # Suppress moviepy output
        )
        
        # Close clips
        audio.close()
        video.close()
        
        print(f"  [Video Placeholder] Video saved to: {out_video_path}")
        
    except ImportError:
        print("  [Video Placeholder] moviepy not installed, creating minimal video file")
        # Create a minimal MP4 file as placeholder
        # This is a very basic approach - in production, proper video generation is needed
        with open(out_video_path, 'wb') as f:
            # Write minimal MP4 header (this won't be a valid video, just a placeholder)
            f.write(b'\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6f\x6d')
            f.write(b'\x00\x00\x02\x00\x69\x73\x6f\x6d\x69\x73\x6f\x32')
        print(f"  [Video Placeholder] Placeholder file created at: {out_video_path}")


def generate_video_from_text(
    text: str,
    output_filename: str,
    output_dir: Path,
    avatar_path: Optional[Path] = None,
    audio_dir: Optional[Path] = None
) -> Dict[str, str]:
    """
    Generate a video from text using TTS and avatar synthesis.
    
    Args:
        text: The text to be spoken
        output_filename: Name for the output video file (without extension)
        output_dir: Directory to save the output video
        avatar_path: Path to avatar image (optional)
        audio_dir: Directory to save intermediate audio files (optional)
        
    Returns:
        Dictionary with status and file paths
    """
    # Create directories if they don't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if audio_dir:
        audio_dir.mkdir(parents=True, exist_ok=True)
    else:
        audio_dir = output_dir / 'temp_audio'
        audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique ID for this job
    job_id = str(uuid.uuid4())[:8]
    
    # Define paths
    audio_path = audio_dir / f"{output_filename}_{job_id}.wav"
    video_path = output_dir / f"{output_filename}.mp4"
    
    try:
        # Step 1: Text to Speech
        print(f"\n[Step 1/2] Converting text to speech...")
        text_to_speech_placeholder(text, audio_path)
        
        # Step 2: Generate talking avatar video
        print(f"[Step 2/2] Generating avatar video...")
        
        # Use provided avatar or default
        if avatar_path and avatar_path.exists():
            avatar = avatar_path
        else:
            # Try to find default avatar
            from django.conf import settings
            default_avatar = Path(settings.BASE_DIR) / 'avatar' / 'avatar.png'
            avatar = default_avatar if default_avatar.exists() else None
        
        generate_placeholder_video(
            avatar if avatar else Path('placeholder.png'),
            audio_path,
            video_path
        )
        
        return {
            'status': 'success',
            'video_path': str(video_path),
            'audio_path': str(audio_path),
            'text': text
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'text': text
        }


def batch_generate_videos(entries: list, output_dir: Path, avatar_path: Optional[Path] = None) -> list:
    """
    Generate videos for multiple text entries.
    
    Args:
        entries: List of dictionaries with 'text' and 'filename' keys
        output_dir: Directory to save output videos
        avatar_path: Optional path to avatar image
        
    Returns:
        List of result dictionaries for each video
    """
    results = []
    total = len(entries)
    
    print(f"\n{'='*60}")
    print(f"Starting batch video generation for {total} entries")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    for idx, entry in enumerate(entries, start=1):
        print(f"\n--- Processing entry {idx}/{total} ---")
        print(f"Text: {entry['text'][:100]}...")
        
        result = generate_video_from_text(
            text=entry['text'],
            output_filename=entry['filename'],
            output_dir=output_dir,
            avatar_path=Path(entry['avatar']) if entry.get('avatar') else avatar_path
        )
        
        result['row_number'] = entry.get('row_number', idx)
        result['filename'] = entry['filename']
        results.append(result)
        
        if result['status'] == 'success':
            print(f"✓ Successfully generated: {result['video_path']}")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("Batch Generation Complete!")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\nSummary:")
    print(f"  Total: {total}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    
    if failed > 0:
        print(f"\nFailed entries:")
        for r in results:
            if r['status'] == 'error':
                print(f"  - Row {r['row_number']}: {r.get('error', 'Unknown error')}")
    
    return results
