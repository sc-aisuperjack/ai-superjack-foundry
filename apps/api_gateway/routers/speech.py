from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from apps.api_gateway.dependencies import get_speech_service
from services.speech.service import SpeechService
from shared.contracts.chat import SpeechSynthesisRequest

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    speech_service: SpeechService = Depends(get_speech_service),
) -> dict[str, str]:
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio upload.")
    transcript = await speech_service.transcribe(audio_bytes=audio_bytes, filename=file.filename or "audio.wav")
    return {"transcript": transcript, "provider": speech_service.provider_name}


@router.post("/speak")
async def speak_text(
    payload: SpeechSynthesisRequest,
    speech_service: SpeechService = Depends(get_speech_service),
) -> Response:
    audio_bytes = await speech_service.speak(payload.text)
    media_type = "audio/mpeg" if speech_service.provider_name == "openai" else "audio/wav"
    return Response(content=audio_bytes, media_type=media_type)
