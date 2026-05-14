import requests
import base64
import torch
import numpy as np
import io
import wave
import json

class EmAySee_ScenemaAudioConnector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True, 
                    "default": "<speak voice=\"Gravelly male voice, fast talking, rough.\" gender=\"male\">\n<action>He completely loses it, shouting</action>\nWhat are you waiting for?!\n</speak>"
                }),
                "api_url": ("STRING", {"default": "http://10.0.0.71:8000/generate"}),
                "seed": ("INT", {"default": 42, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True}),
                "steps": ("INT", {"default": 50, "min": 1, "max": 200}),
                "guidance_scale": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "output_sample_rate": ([24000, 44100, 48000], {"default": 44100}),
            },
            "optional": {
                "reference_audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("AUDIO", "STRING")
    RETURN_NAMES = ("audio", "status")
    FUNCTION = "generate_audio"
    CATEGORY = "EmAySee/Audio"

    def generate_audio(self, prompt, api_url, seed, steps, guidance_scale, output_sample_rate, reference_audio=None):
        payload = {
            "prompt": prompt,
            "seed": seed,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "sample_rate": output_sample_rate,
        }

        if reference_audio is not None:
            waveform = reference_audio["waveform"]
            sr_in = reference_audio["sample_rate"]
            
            waveform_np = waveform.squeeze().cpu().numpy()
            if waveform_np.ndim > 1:
                waveform_np = waveform_np.mean(axis=0)
            
            waveform_int = (waveform_np * 32767).astype(np.int16)
            
            byte_io = io.BytesIO()
            with wave.open(byte_io, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sr_in)
                wav_file.writeframes(waveform_int.tobytes())
            
            audio_b64 = base64.b64encode(byte_io.getvalue()).decode('utf-8')
            payload["reference_audio"] = audio_b64

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url.strip(), json=payload, headers=headers, timeout=300)
            
            if response.status_code != 200:
                return (None, f"Error: {response.status_code} - {response.text}")

            result_json = response.json()
            if "audio" not in result_json:
                return (None, f"JSON missing 'audio' key. Got: {list(result_json.keys())}")

            audio_data = base64.b64decode(result_json["audio"])
            
            byte_io = io.BytesIO(audio_data)
            with wave.open(byte_io, 'rb') as wav_file:
                sr_out = wav_file.getframerate()
                n_channels = wav_file.getnchannels()
                frames = wav_file.readframes(wav_file.getnframes())
                waveform_np = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                
                if n_channels > 1:
                    waveform_np = waveform_np.reshape(-1, n_channels).T
                else:
                    waveform_np = waveform_np.reshape(1, -1)
                
                waveform_tensor = torch.from_numpy(waveform_np).unsqueeze(0)
            
            return ({"waveform": waveform_tensor, "sample_rate": sr_out}, "Success")

        except Exception as e:
            return (None, f"Connection Failed: {str(e)}")

NODE_CLASS_MAPPINGS = {
    "EmAySee_ScenemaAudioConnector": EmAySee_ScenemaAudioConnector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ScenemaAudioConnector": "EmAySee Scenema Audio Connector"
}