import torch
import numpy as np
from PIL import Image
import io
from google import genai
from google.genai import types

class EmAySee_GeminiImageGen:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "prompt": ("STRING", {"multiline": True}),
                "model": (["gemini-2.0-flash-exp", "gemini-2.5-flash-image", "imagen-3.0-generate-001", "imagen-3.0-fast-generate-001"],),
                "aspect_ratio": (["1:1", "16:9", "9:16", "4:3", "3:4"],),
                "number_of_images": ("INT", {"default": 1, "min": 1, "max": 4}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_image"
    CATEGORY = "EmAySee"

    def generate_image(self, api_key, prompt, model, aspect_ratio, number_of_images):
        client = genai.Client(api_key=api_key)
        
        try:
            if number_of_images > 4:
                number_of_images = 4

            response = client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio,
                    safety_filter_level="BLOCK_ONLY_HIGH",
                    person_generation="ALLOW_ADULT",
                )
            )

            output_images = []
            if response.generated_images:
                for img_entry in response.generated_images:
                    image_bytes = img_entry.image.image_bytes
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    image_np = np.array(image).astype(np.float32) / 255.0
                    image_tensor = torch.from_numpy(image_np)
                    output_images.append(image_tensor)

            if not output_images:
                print("No images returned by Gemini.")
                return (torch.zeros((1, 512, 512, 3), dtype=torch.float32),)

            if len(output_images) > 1:
                final_tensor = torch.stack(output_images)
            else:
                final_tensor = output_images[0].unsqueeze(0)

            return (final_tensor,)

        except Exception as e:
            print(f"Gemini API Error: {e}")
            empty = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return (empty,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_GeminiImageGen": EmAySee_GeminiImageGen
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_GeminiImageGen": "EmAySee Gemini Image Gen"
}