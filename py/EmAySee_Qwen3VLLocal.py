import gc
import torch
import numpy as np
import psutil
from PIL import Image

try:
    from transformers import AutoProcessor, Qwen3VLForConditionalGeneration, Qwen2_5_VLForConditionalGeneration, AutoModelForImageTextToText
except ImportError:
    AutoProcessor = None
    Qwen3VLForConditionalGeneration = None
    Qwen2_5_VLForConditionalGeneration = None
    AutoModelForImageTextToText = None

class EmAySee_QwenVLLocal:
    _MODEL = None
    _PROCESSOR = None
    _CURRENT_PATH = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_path": ("STRING", {"default": "/ai/datasets/ComfyUI/models/LLM/DavidAU/gemma-3-4b-it-vl-Heretic-SuperBrain7x-Uncensored"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "Analyze this image and generate a detailed image generation prompt. Output only the prompt."}),
                "user_prompt": ("STRING", {"multiline": True, "default": ""}),
                "max_tokens": ("INT", {"default": 2048, "min": 16, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 2.0, "step": 0.05}),
                "max_memory_percent": ("FLOAT", {"default": 0.95, "min": 0.10, "max": 1.00, "step": 0.01}),
                "unload_after": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "thinking")
    FUNCTION = "generate"
    CATEGORY = "EmAySee"

    def _tensor_to_pil(self, image_tensor):
        img0 = image_tensor[0].detach().cpu().float().clamp(0, 1)
        arr = (img0.numpy() * 255.0).round().astype(np.uint8)
        return Image.fromarray(arr, mode="RGB")

    def load_model(self, model_path, max_memory_percent):
        if EmAySee_QwenVLLocal._MODEL is not None and EmAySee_QwenVLLocal._CURRENT_PATH == model_path:
            return EmAySee_QwenVLLocal._MODEL, EmAySee_QwenVLLocal._PROCESSOR

        if AutoProcessor is None:
            raise RuntimeError("transformers library is missing or out of date.")

        EmAySee_QwenVLLocal._PROCESSOR = AutoProcessor.from_pretrained(model_path)
        
        path_lower = model_path.lower()
        if "gemma" in path_lower:
            model_class = AutoModelForImageTextToText
        elif "qwen2.5" in path_lower or "qwen2-5" in path_lower or "qwen2_5" in path_lower:
            model_class = Qwen2_5_VLForConditionalGeneration
        elif "qwen" in path_lower:
            model_class = Qwen3VLForConditionalGeneration
        else:
            model_class = AutoModelForImageTextToText

        if model_class is None:
            raise RuntimeError("Required model architecture not found in transformers. Please update transformers.")

        max_mem = {}
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                max_mem[i] = int(torch.cuda.get_device_properties(i).total_memory * max_memory_percent)
        max_mem["cpu"] = int(psutil.virtual_memory().total * max_memory_percent)

        EmAySee_QwenVLLocal._MODEL = model_class.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            max_memory=max_mem
        )
        EmAySee_QwenVLLocal._MODEL.eval()
        EmAySee_QwenVLLocal._CURRENT_PATH = model_path
        
        return EmAySee_QwenVLLocal._MODEL, EmAySee_QwenVLLocal._PROCESSOR

    def unload_model(self):
        EmAySee_QwenVLLocal._MODEL = None
        EmAySee_QwenVLLocal._PROCESSOR = None
        EmAySee_QwenVLLocal._CURRENT_PATH = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

    def generate(self, image, model_path, system_prompt, user_prompt, max_tokens, temperature, max_memory_percent, unload_after):
        pil_image = self._tensor_to_pil(image)
        model, processor = self.load_model(model_path, max_memory_percent)

        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt.strip()}]},
            {"role": "user", "content": [
                {"type": "image", "image": pil_image},
                {"type": "text", "text": user_prompt.strip()}
            ]}
        ]

        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )

        inputs = inputs.to(model.device)

        gen_kwargs = {"max_new_tokens": int(max_tokens)}
        if temperature > 0:
            gen_kwargs.update({"do_sample": True, "temperature": float(temperature), "top_p": 0.9})
        else:
            gen_kwargs.update({"do_sample": False})

        with torch.inference_mode():
            output_ids = model.generate(**inputs, **gen_kwargs)

        trimmed_ids = [out_id[len(in_id):] for in_id, out_id in zip(inputs.input_ids, output_ids)]
        output_text = processor.batch_decode(trimmed_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

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
    "EmAySee_QwenVLLocal": EmAySee_QwenVLLocal
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenVLLocal": "EmAySee_Vision LLM Local Generator"
}