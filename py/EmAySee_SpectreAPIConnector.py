import base64
from io import BytesIO
from PIL import Image
import torch
import numpy as np
import requests
import json

class EmAySee_SpectreAPIConnector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "spectre_url": ("STRING", {"default": "http://10.0.0.71:11434/v1/chat/completions"}),
                "model_name": ("STRING", {"default": "qwen3-vl"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "Analyze this image and generate a detailed image generation prompt. Output only the prompt."}),
                "user_prompt": ("STRING", {"multiline": True, "default": ""}),
                "max_tokens": ("INT", {"default": 2048, "min": 16, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 2.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "thinking")
    FUNCTION = "generate"
    CATEGORY = "EmAySee"

    def _tensor_to_base64(self, image_tensor):
        img0 = image_tensor[0].detach().cpu().float().clamp(0, 1)
        arr = (img0.numpy() * 255.0).round().astype(np.uint8)
        pil_img = Image.fromarray(arr, mode="RGB")
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def generate(self, image, spectre_url, model_name, system_prompt, user_prompt, max_tokens, temperature):
        b64_image = self._tensor_to_base64(image)
        data_url = f"data:image/jpeg;base64,{b64_image}"

        text_instruction = system_prompt.strip()
        if user_prompt and user_prompt.strip():
            text_instruction = f"{text_instruction}\nAdditional requirements:\n{user_prompt.strip()}"

        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_instruction},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(spectre_url, headers=headers, data=json.dumps(payload), timeout=600)
            response.raise_for_status()
            response_data = response.json()
            
            output_text = response_data["choices"][0]["message"]["content"]
            
            thinking = ""
            prompt = output_text

            think_end_tag = "</think>"
            if think_end_tag in output_text:
                parts = output_text.split(think_end_tag, 1)
                thinking = parts[0].replace("<think>", "").strip()
                prompt = parts[1].strip()

            return (prompt, thinking)
            
        except requests.exceptions.RequestException as e:
            return (f"API Connection Error: {str(e)}", "")
        except KeyError as e:
            return (f"Unexpected API Response format: {str(e)}", "")

NODE_CLASS_MAPPINGS = {
    "EmAySee_SpectreAPIConnector": EmAySee_SpectreAPIConnector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SpectreAPIConnector": "EmAySee_Spectre API Connector"
}