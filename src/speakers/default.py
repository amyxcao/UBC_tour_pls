from ..interfaces import Speaker

import openai  # Changed from requests
import sounddevice as sd  # Added for playback
import numpy as np  # Added for PCM data handling
import os
from typing_extensions import Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class DefaultSpeaker(Speaker):
    """A speaker that uses Azure OpenAI TTS API to convert text to speech and plays it"""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config if config else {})  # Ensure config is a dict
        # Default configuration for Azure TTS API
        self.api_key = self.config.get("api_key", os.getenv("AZURE_OPENAI_API_KEY"))
        # Endpoint should be the base URL, not the full path with query params
        self.azure_endpoint = self.config.get(
            "azure_endpoint",
            "https://openai-ai-museum.openai.azure.com",  # Base endpoint
        )
        self.api_version = self.config.get("api_version", "2025-03-01-preview")
        self.tts_deployment_name = self.config.get(
            "tts_deployment_name", "tts"
        )  # This is the model/deployment
        self.voice = self.config.get("voice", "alloy")
        self.output_format = self.config.get(
            "output_format", "pcm"
        )  # Default to pcm for direct playback
        self.samplerate = self.config.get("samplerate", 24000)  # Default for pcm

        # Validate API key
        if not self.api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY not set. Provide it in config or environment variable."
            )
        if not self.azure_endpoint:
            raise ValueError(
                "Azure endpoint not set. Provide it in config or environment variable."
            )

        self.client = openai.AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.api_version,
        )

    def process(self, text: str) -> None:
        """Convert text to speech using Azure TTS API and play it in real-time"""
        if not text:
            print("Speaker received empty text, nothing to play.")
            return

        try:
            response = self.client.audio.speech.create(
                model=self.tts_deployment_name,
                voice=self.voice,
                input=text,
                response_format=self.output_format,
            )

            channels = 1  # PCM from OpenAI is typically mono

            print(f"Speaker: Starting audio playback (format: {self.output_format})...")

            if self.output_format == "pcm":

                def pcm_audio_stream_generator():
                    for chunk in response.iter_bytes(chunk_size=1024):
                        yield np.frombuffer(chunk, dtype=np.int16)

                with sd.OutputStream(
                    samplerate=self.samplerate, channels=channels, dtype="int16"
                ) as stream:
                    for audio_chunk in pcm_audio_stream_generator():
                        if len(audio_chunk) > 0:
                            stream.write(audio_chunk)
                print("Speaker: PCM audio playback finished.")
            else:
                # For other formats, save to file as direct playback is more complex here
                output_filename = f"speaker_output_audio.{self.output_format}"
                print(
                    f"Speaker: Received {self.output_format} format. Saving to {output_filename}..."
                )
                with open(output_filename, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=4096):
                        f.write(chunk)
                print(
                    f"Speaker: Audio saved to {output_filename}. Manual playback required for this format."
                )

        except openai.APIError as e:
            print(f"Speaker: Azure OpenAI API Error: {e}")
        except Exception as e:
            print(f"Speaker: An unexpected error occurred during TTS processing: {e}")
