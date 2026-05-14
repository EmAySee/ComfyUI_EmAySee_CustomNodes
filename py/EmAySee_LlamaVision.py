import torch
import base64
import json
import urllib.request
import urllib.error
import time
import numpy as np
from PIL import Image
from io import BytesIO

class EmAySee_LlamaVision:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": ("STRING", {"default": "qwen2-vl"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a specialized image captioning assistant for AI training datasets."}),
                "prompt": ("STRING", {"multiline": True, "default": "Describe this image in detail."}),
                "server_url": ("STRING", {"default": "http://10.0.0.71:11434"}),
                "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 2.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "analyze_image"
    CATEGORY = "EmAySee/LLM"

    def analyze_image(self, image, model, system_prompt, prompt, server_url, max_tokens, temperature):
        i = 255. * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        url = f"{server_url.rstrip('/')}/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        
        retries = 5
        delay = 1
        last_error = ""

        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return (res_data["choices"][0]["message"]["content"],)
            except Exception as e:
                last_error = str(e)
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                continue
        
        return (f"Error connecting to Ollama on SPECTRE: {last_error}",)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LlamaVision": EmAySee_LlamaVision
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LlamaVision": "EmAySee Llama Vision"
}