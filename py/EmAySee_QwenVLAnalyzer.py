import os
import torch
import base64
import re
import gc
import importlib
import sys
from PIL import Image
from io import BytesIO
import numpy as np
from transformers import AutoProcessor, AutoModelForVision2Seq, BitsAndBytesConfig
from huggingface_hub import snapshot_download, hf_hub_download
import comfy.model_management

class EmAySee_QwenVLAnalyzer:
    def __init__(self):
        self.model = None
        self.processor = None
        self.current_model_path = ""
        self.backend = ""
        self.current_quant = ""

    @classmethod
    def INPUT_TYPES(s):
        base_path = "/ai/datasets/ComfyUI/models/LLM"
        
        folders = [""]
        if os.path.exists(base_path):
            folders += sorted([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])
        
        gguf_files = [""]
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith(".gguf"):
                        rel_path = os.path.relpath(os.path.join(root, file), base_path)
                        gguf_files.append(rel_path)
        
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "Describe this image in detail."}),
                "model_folder": (folders, {"default": ""}),
                "repo_id": ("STRING", {"default": ""}),
                "backend": (["transformers", "gguf"], {"default": "transformers"}),
                "precision": (["fp16", "bf16", "int8", "int4"], {"default": "bf16"}),
                "max_new_tokens": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.01}),
                "device": (["cuda", "cpu"], {"default": "cuda"}),
                "unload_comfy_models": ("BOOLEAN", {"default": True}),
                "dev_mode": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "gguf_model_file": (gguf_files, {"default": ""}),
                "gguf_mmproj_file": (gguf_files, {"default": ""}),
                "base_path_override": ("STRING", {"default": "/ai/datasets/ComfyUI/models/LLM"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("answer", "thinking")
    FUNCTION = "analyze"
    CATEGORY = "EmAySee/LLM"

    def analyze(self, image, prompt, model_folder, repo_id, backend, precision, max_new_tokens, temperature, device, unload_comfy_models, dev_mode, gguf_model_file="", gguf_mmproj_file="", base_path_override="/ai/datasets/ComfyUI/models/LLM"):
        if dev_mode:
            importlib.reload(sys.modules[__name__])
            reloaded_module = sys.modules[__name__]
            reloaded_class = getattr(reloaded_module, self.__class__.__name__)
            
            new_instance = reloaded_class()
            new_instance.model = self.model
            new_instance.processor = self.processor
            new_instance.current_model_path = self.current_model_path
            new_instance.backend = self.backend
            new_instance.current_quant = self.current_quant
            
            return new_instance.real_analyze(image, prompt, model_folder, repo_id, backend, precision, max_new_tokens, temperature, device, unload_comfy_models, gguf_model_file, gguf_mmproj_file, base_path_override)
        
        return self.real_analyze(image, prompt, model_folder, repo_id, backend, precision, max_new_tokens, temperature, device, unload_comfy_models, gguf_model_file, gguf_mmproj_file, base_path_override)

    def real_analyze(self, image, prompt, model_folder, repo_id, backend, precision, max_new_tokens, temperature, device, unload_comfy_models, gguf_model_file, gguf_mmproj_file, base_path_override):
        base_path = base_path_override if base_path_override.strip() else "/ai/datasets/ComfyUI/models/LLM"
        
        if unload_comfy_models:
            comfy.model_management.unload_all_models()
            comfy.model_management.soft_empty_cache()
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        repo_id_clean = repo_id.strip()
        if repo_id_clean:
            local_dir = os.path.join(base_path, repo_id_clean.replace("/", "--"))
            if not os.path.exists(local_dir):
                if backend == "transformers":
                    snapshot_download(repo_id=repo_id_clean, local_dir=local_dir, local_dir_use_symlinks=False)
                elif backend == "gguf":
                    os.makedirs(local_dir, exist_ok=True)
        elif model_folder.strip():
            local_dir = os.path.join(base_path, model_folder.strip())
        else:
            return ("Error: Please select a model_folder or provide a repo_id.", "")

        full_content = ""

        try:
            if backend == "transformers":
                if self.current_model_path != local_dir or self.backend != "transformers" or self.current_quant != precision or self.model is None:
                    if self.model is not None:
                        if hasattr(self.model, "to"):
                            self.model.to("cpu")
                        del self.model
                        del self.processor
                        self.model = None
                        self.processor = None
                        gc.collect()
                        torch.cuda.empty_cache()

                    bnb_config = None
                    dtype = torch.float16 if precision == "fp16" else torch.bfloat16
                    
                    if precision == "int4":
                        bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=dtype, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True)
                    elif precision == "int8":
                        bnb_config = BitsAndBytesConfig(load_in_8bit=True)

                    self.processor = AutoProcessor.from_pretrained(local_dir, trust_remote_code=True)
                    dev_map = "auto" if bnb_config is not None else device
                    
                    self.model = AutoModelForVision2Seq.from_pretrained(
                        local_dir,
                        quantization_config=bnb_config,
                        device_map=dev_map,
                        torch_dtype=dtype,
                        trust_remote_code=True,
                        low_cpu_mem_usage=True,
                        attn_implementation="sdpa"
                    ).eval()
                    self.current_model_path = local_dir
                    self.backend = "transformers"
                    self.current_quant = precision

                i = 255. * image[0].cpu().numpy()
                pil_image = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                messages = [{"role": "user", "content": [{"type": "image", "image": pil_image}, {"type": "text", "text": prompt}]}]
                text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                
                image_inputs, video_inputs = None, None
                try:
                    from qwen_vl_utils import process_vision_info
                    image_inputs, video_inputs = process_vision_info(messages)
                except ImportError:
                    image_inputs = [pil_image]

                inputs = self.processor(text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt").to(device)
                
                if bnb_config is None and hasattr(self.model, "device") and self.model.device.type != "cuda":
                    self.model.to(device)

                generated_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens, temperature=temperature, do_sample=True if temperature > 0 else False)
                generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
                output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)
                full_content = output_text[0]

            elif backend == "gguf":
                from llama_cpp import Llama
                import llama_cpp.llama_chat_format as chat_format

                Qwen2VLChatHandler = getattr(chat_format, "Qwen2VLChatHandler", None)
                if Qwen2VLChatHandler is None:
                    for attr in dir(chat_format):
                        if "Qwen" in attr and "VL" in attr and "Handler" in attr:
                            Qwen2VLChatHandler = getattr(chat_format, attr)
                            break
                
                if Qwen2VLChatHandler is None:
                    return ("Error: Qwen2VLChatHandler not found.", "")

                model_path = os.path.join(base_path, gguf_model_file)
                mmproj_path = os.path.join(base_path, gguf_mmproj_file)

                if not os.path.exists(model_path):
                    if repo_id_clean and gguf_model_file:
                        target_dir = os.path.join(base_path, repo_id_clean.replace("/", "--"))
                        os.makedirs(target_dir, exist_ok=True)
                        hf_hub_download(repo_id=repo_id_clean, filename=os.path.basename(gguf_model_file), local_dir=target_dir)
                        model_path = os.path.join(target_dir, os.path.basename(gguf_model_file))
                    else:
                        return (f"Error: GGUF model file not found at {model_path}", "")
                
                if not os.path.exists(mmproj_path):
                    if repo_id_clean and gguf_mmproj_file:
                        target_dir = os.path.join(base_path, repo_id_clean.replace("/", "--"))
                        os.makedirs(target_dir, exist_ok=True)
                        hf_hub_download(repo_id=repo_id_clean, filename=os.path.basename(gguf_mmproj_file), local_dir=target_dir)
                        mmproj_path = os.path.join(target_dir, os.path.basename(gguf_mmproj_file))
                    else:
                        return (f"Error: GGUF mmproj file not found at {mmproj_path}", "")

                if self.current_model_path != model_path or self.backend != "gguf" or self.model is None:
                    chat_handler = Qwen2VLChatHandler(clip_model_path=mmproj_path)
                    self.model = Llama(
                        model_path=model_path,
                        chat_handler=chat_handler,
                        n_ctx=2048,
                        n_gpu_layers=-1 if device == "cuda" else 0,
                        logits_all=True
                    )
                    self.current_model_path = model_path
                    self.backend = "gguf"

                i = 255. * image[0].cpu().numpy()
                pil_image = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                buffered = BytesIO()
                pil_image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                data_url = f"data:image/jpeg;base64,{base64_image}"

                response = self.model.create_chat_completion(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": data_url}}
                            ]
                        }
                    ],
                    max_tokens=max_new_tokens,
                    temperature=temperature
                )
                full_content = response["choices"][0]["message"]["content"]

            think_pattern = r'<(?:think|thought)>(.*?)</(?:think|thought)>'
            think_match = re.search(think_pattern, full_content, flags=re.DOTALL | re.IGNORECASE)
            
            if think_match:
                thinking = think_match.group(1).strip()
                answer = re.sub(think_pattern, '', full_content, flags=re.DOTALL | re.IGNORECASE).strip()
            else:
                if "<think>" in full_content.lower():
                    start_idx = full_content.lower().find("<think>") + 7
                    thinking = full_content[start_idx:].strip()
                    answer = "[REASONING DID NOT FINISH]"
                else:
                    thinking = ""
                    answer = full_content.strip()

            return (answer, thinking)

        except Exception as e:
            return (f"Error: {str(e)}", "")

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenVLAnalyzer": EmAySee_QwenVLAnalyzer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenVLAnalyzer": "EmAySee QwenVL Analyzer"
}