import uuid
from pathlib import Path

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import GenerateVideoSerializer

# ===== TTS MODEL LOAD (example: Coqui TTS) =====
# Uncomment when TTS library is installed:
# from TTS.api import TTS
# TTS_MODEL_NAME = "tts_models/en/ljspeech/tacotron2-DDC"
# tts_model = TTS(TTS_MODEL_NAME)

# Avatar image (single static avatar)
AVATAR_PATH = Path(settings.BASE_DIR) / 'avatar' / 'avatar.png'
AVATAR_PATH.parent.mkdir(parents=True, exist_ok=True)

# Directories for generated outputs
AUDIO_DIR = Path(settings.MEDIA_ROOT) / 'audio'
VIDEO_DIR = Path(settings.MEDIA_ROOT) / 'video'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def text_to_speech(text: str, out_wav_path: Path):
    """
    Local TTS: text > WAV file
    Uses Coqui TTS offline model
    """
    # Uncomment when TTS library is installed:
    # tts_model.tts_to_file(text=text, file_path=str(out_wav_path))
    
    # For now, just raise an error so you remember to implement it:
    raise NotImplementedError("TTS not configured. Install TTS library and uncomment the code above.")


def generate_talking_avatar(avatar_img: Path, audio_path: Path, out_video_path: Path):
    """
    Use your local talking-head / lip-sync model (e.g. Wav2Lip, SadTalker)
    to create a video at out_video_path

    Here I'll put pseudocode – you'll replace with your real inference call
    """

    # PSEUDOCODE EXAMPLE WITH WAV2LIP-LIKE FUNCTION:
    #
    # from wav2lip_inference import make_talking_video
    # make_talking_video(
    #     face_image=str(avatar_img),
    #     audio=str(audio_path),
    #     outfile=str(out_video_path),
    # )
    #
    # For now, just raise an error so you remember to implement it:
    raise NotImplementedError("Plug your Wav2Lip/SadTalker inference here")


class GenerateVideoView(APIView):
    """
    POST /api/generatevideo/
    Body: { "text": "Hello world" }
    Response: { "video_url": "/media/video/<id>.mp4" }
    """

    def post(self, request, *args, **kwargs):
        serializer = GenerateVideoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text'].strip()
        if not text:
            return Response(
                {"detail": "Text cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job_id = str(uuid.uuid4())

        audio_path = AUDIO_DIR / f"{job_id}.wav"
        video_path = VIDEO_DIR / f"{job_id}.mp4"

        # 1. text > speech
        try:
            text_to_speech(text, audio_path)
        except NotImplementedError as e:
            # dev convenience
            return Response(
                {"detail": f"TTS not implemented: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 2. avatar + audio > talking-head video
        try:
            generate_talking_avatar(AVATAR_PATH, audio_path, video_path)
        except NotImplementedError as e:
            # dev convenience
            return Response(
                {"detail": f"Video generation not implemented: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        video_url = f"{settings.MEDIA_URL}video/{job_id}.mp4"
        return Response({"video_url": video_url}, status=status.HTTP_200_OK)
