import asyncio
import io
import math
import struct
import wave
from dataclasses import dataclass

from openai import OpenAI

from shared.config.settings import Settings


@dataclass
class SpeechService:
    settings: Settings
    provider_name: str = "mock"

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        if self.provider_name == "openai" and self.settings.openai_api_key:
            return await asyncio.to_thread(self._transcribe_sync, audio_bytes, filename)
        return f"Mock transcript: received {len(audio_bytes)} bytes of audio."

    async def speak(self, text: str) -> bytes:
        if self.provider_name == "openai" and self.settings.openai_api_key:
            return await asyncio.to_thread(self._speak_sync, text)
        return self._mock_wav(text)

    def _transcribe_sync(self, audio_bytes: bytes, filename: str) -> str:
        client = OpenAI(api_key=self.settings.openai_api_key)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = filename
        transcript = client.audio.transcriptions.create(
            model=self.settings.openai_stt_model,
            file=audio_file,
        )
        return (getattr(transcript, "text", "") or "").strip()

    def _speak_sync(self, text: str) -> bytes:
        client = OpenAI(api_key=self.settings.openai_api_key)
        with client.audio.speech.with_streaming_response.create(
            model=self.settings.openai_tts_model,
            voice=self.settings.openai_tts_voice,
            input=text,
        ) as response:
            return response.read()

    def _mock_wav(self, text: str) -> bytes:
        duration_seconds = max(1.0, min(4.0, len(text) / 60.0))
        sample_rate = 16000
        amplitude = 16000
        frequency = 440.0
        frames = bytearray()
        total_samples = int(duration_seconds * sample_rate)
        for i in range(total_samples):
            value = int(amplitude * math.sin(2.0 * math.pi * frequency * (i / sample_rate)))
            frames.extend(struct.pack("<h", value))
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(bytes(frames))
        return buffer.getvalue()
