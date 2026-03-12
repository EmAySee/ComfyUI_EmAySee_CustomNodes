import base64
from io import BytesIO
from PIL import Image
import torch
import gc
import numpy as np

try:
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Llava15ChatHandler
except ImportError:
    Llama = None
    Llava15ChatHandler = None

class EmAySee_GGUFVisionLocal:
    _MODEL = None
    _CHAT_HANDLER = None
    _CURRENT_MODEL_PATH = None
    _CURRENT_MMPROJ_PATH = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "gguf_model_path": ("STRING", {"default": "/ai/models-2/models/LLM/qwen3-vl-4b.gguf"}),
                "mmproj_path": ("STRING", {"default": "/ai/models-2/models/LLM/mmproj-qwen3-vl-4b.gguf"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "Analyze this image and generate a detailed image generation prompt. Output only the prompt."}),
                "user_prompt": ("STRING", {"multiline": True, "default": ""}),
                "max_tokens": ("INT", {"default": 2048, "min": 16, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 2.0, "step": 0.05}),
                "n_gpu_layers": ("INT", {"default": -1, "min": -1, "max": 128}),
                "unload_after": ("BOOLEAN", {"default": True}),
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
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{img_str}"

    def load_model(self, model_path, mmproj_path, n_gpu_layers):
        if EmAySee_GGUFVisionLocal._MODEL is not None and \
           EmAySee_GGUFVisionLocal._CURRENT_MODEL_PATH == model_path and \
           EmAySee_GGUFVisionLocal._CURRENT_MMPROJ_PATH == mmproj_path:
            return EmAySee_GGUFVisionLocal._MODEL

        if Llama is None:
            raise RuntimeError("llama_cpp is not installed. Please compile llama-cpp-python with CUDA support.")

        chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
        
        llm = Llama(
            model_path=model_path,
            chat_handler=chat_handler,
            n_ctx=4096, 
            n_gpu_layers=n_gpu_layers,
            verbose=False
        )

        EmAySee_GGUFVisionLocal._CHAT_HANDLER = chat_handler
        EmAySee_GGUFVisionLocal._MODEL = llm
        EmAySee_GGUFVisionLocal._CURRENT_MODEL_PATH = model_path
        EmAySee_GGUFVisionLocal._CURRENT_MMPROJ_PATH = mmproj_path

        return EmAySee_GGUFVisionLocal._MODEL

    def unload_model(self):
        if EmAySee_GGUFVisionLocal._MODEL is not None:
            del EmAySee_GGUFVisionLocal._MODEL
            del EmAySee_GGUFVisionLocal._CHAT_HANDLER
            EmAySee_GGUFVisionLocal._MODEL = None
            EmAySee_GGUFVisionLocal._CHAT_HANDLER = None
            EmAySee_GGUFVisionLocal._CURRENT_MODEL_PATH = None
            EmAySee_GGUFVisionLocal._CURRENT_MMPROJ_PATH = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    def generate(self, image, gguf_model_path, mmproj_path, system_prompt, user_prompt, max_tokens, temperature, n_gpu_layers, unload_after):
        b64_image = self._tensor_to_base64(image)
        llm = self.load_model(gguf_model_path, mmproj_path, n_gpu_layers)

        if system_prompt.strip() == "":
            text_instruction = "Convert the image into a rich image-generation prompt."
        else:
            text_instruction = system_prompt.strip()
        
        if user_prompt and user_prompt.strip():
            text_instruction = f"{text_instruction}\nAdditional requirements:\n{user_prompt.strip()}"

        response = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": b64_image}},
                        {"type": "text", "text": text_instruction}
                    ]
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        output_text = response["choices"][0]["message"]["content"]
        
        thinking = ""
        prompt = output_text

        think_end_tag = "</think>"
        if think_end_tag in output_text:
            parts = output_text.split(think_end_tag, 1)
            thinking = parts[0].replace("<think>", "").strip()
            prompt = parts[1].strip()

        if unload_after:
            self.unload_model()

        return (prompt, thinking)

NODE_CLASS_MAPPINGS = {
    "EmAySee_GGUFVisionLocal": EmAySee_GGUFVisionLocal
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_GGUFVisionLocal": "EmAySee_GGUF Vision Local Generator"
}