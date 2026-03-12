import base64
import json
import re
import os
from io import BytesIO
from typing import Dict, Tuple

import gc
import numpy as np
import torch
from PIL import Image
import requests

try:
    from transformers import AutoProcessor
    from transformers import Qwen2_5_VLForConditionalGeneration
    from transformers import Qwen3VLForConditionalGeneration
except Exception:
    AutoProcessor = None
    Qwen2_5_VLForConditionalGeneration = None
    Qwen3VLForConditionalGeneration = None

def _tensor_image_to_pil(image_tensor: torch.Tensor) -> Image.Image:
    if not isinstance(image_tensor, torch.Tensor):
        raise TypeError("IMAGE input must be a torch.Tensor")
    if image_tensor.ndim != 4 or image_tensor.shape[-1] != 3:
        raise ValueError(f"Expected IMAGE with shape [B,H,W,3], got {tuple(image_tensor.shape)}")
    img0 = image_tensor[0].detach().cpu().float().clamp(0, 1)
    arr = (img0.numpy() * 255.0).round().astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")

def _clean_single_line(text: str) -> str:
    text = text.strip()
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) >= 2 and ((text[0] == '"' and text[-1] == '"') or (text[0] == "'" and text[-1] == "'")):
        text = text[1:-1].strip()
    return text

def _available_devices() -> Tuple[str, ...]:
    devices = []
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            name = torch.cuda.get_device_name(i)
            devices.append(f"cuda:{i} | {name}")
    devices.append("cpu")
    return tuple(devices)

def _parse_device_choice(device_choice: str) -> str:
    return device_choice.split("|", 1)[0].strip()

def _cuda_cleanup(device_index: int | None):
    gc.collect()
    if torch.cuda.is_available():
        if device_index is None:
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        else:
            with torch.cuda.device(device_index):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

def _resolve_model_family(model_id: str) -> str:
    model_lower = model_id.lower()
    if "qwen2.5" in model_lower:
        return "qwen2_5_vl"
    elif "qwen3" in model_lower:
        return "qwen3_vl"
    else:
        raise ValueError(f"Unknown model ID: {model_id}")

class EmAySee_QwenPromptFromImage:
    _MODEL_CACHE: Dict[Tuple[str, str, str, str], object] = {}
    _PROC_CACHE: Dict[str, object] = {}

    @classmethod
    def INPUT_TYPES(cls):
        default_system = (
            "You convert the given image into a rich, image-generation prompt.\n"
            "Return ONLY the final prompt as a single line, no quotes, no extra text.\n"
            "Include: subject, environment, style, lighting, camera/lens, composition, key details.\n"
            "Avoid meta-commentary."
        )

        model_list = (
            "Qwen/Qwen2.5-VL-3B-Instruct",
            "Qwen/Qwen2.5-VL-7B-Instruct",
            "Qwen/Qwen3-VL-2B-Instruct",
            "Qwen/Qwen3-VL-2B-Thinking",
            "Qwen/Qwen3-VL-8B-Instruct",
            "Qwen/Qwen3-VL-8B-Thinking",
            "Qwen/Qwen3-VL-235B-A22B-Instruct",
            "Qwen/Qwen3-VL-235B-A22B-Thinking",
        )

        return {
            "required": {
                "image": ("IMAGE",),
                "backend": (("local", "openai_compatible"),),
                "qwen_model": (model_list,),
                "local_model_path": ("STRING", {"default": ""}),
                "device": (_available_devices(),),
                "quantization": ((
                    "int8_bnb",
                    "int4_bnb",
                    "bf16",
                    "fp16",
                    "fp32_cpu",
                ),),
                "flash_attention": (("off", "on"),),
                "system_prompt": ("STRING", {"multiline": True, "default": default_system}),
                "user_prompt": ("STRING", {"multiline": True, "default": ""}),
                "max_new_tokens": ("INT", {"default": 2048, "min": 16, "max": 8192, "step": 1}),
                "temperature": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 2.0, "step": 0.05}),
                "safe_quants": ([True, False], {"default": True}),
                "unload_model": ([True, False], {"default": True}),
            },
            "optional": {
                "openai_base_url": ("STRING", {"default": "http://127.0.0.1:11434"}),
                "openai_api_key": ("STRING", {"default": ""}),
                "openai_model_override": ("STRING", {"default": ""}),
                "openrouter_providers": ("STRING", {"default": ""}),
                "verbose_output": ([True, False], {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES = ("prompt_text", "thinking_text")
    FUNCTION = "run"
    CATEGORY = "d3cker/Prompt-Generator"

    def _get_processor(self, model_id: str, load_path: str):
        if AutoProcessor is None:
            raise RuntimeError("transformers is missing or too old.")
        if self._PROC_CACHE.get(load_path) is None:
            self._PROC_CACHE[load_path] = AutoProcessor.from_pretrained(load_path)
        return self._PROC_CACHE[load_path]

    def _load_local_model(self, model_id: str, load_path: str, device_choice: str, quantization: str, flash_attention: str, safe_quants: bool):
        model_family = _resolve_model_family(model_id)
        
        if Qwen2_5_VLForConditionalGeneration is None or Qwen3VLForConditionalGeneration is None:
            raise RuntimeError("transformers is missing or too old.")
        
        device = _parse_device_choice(device_choice)

        if safe_quants:
            if device == "cpu" and quantization != "fp32_cpu":
                quantization = "fp32_cpu"
            elif device.lower().startswith("cuda"):
                if model_family == "qwen2_5_vl" and (quantization == "fp16" or quantization == "fp32_cpu"):
                    quantization = "bf16"
                elif model_family == "qwen3_vl" and quantization == "fp32_cpu":
                    quantization = "bf16"

        if quantization == "fp32_cpu":
            dtype = torch.float32
        elif quantization == "bf16":
            dtype = torch.bfloat16
        elif quantization == "fp16":
            dtype = torch.float16
        else:
            dtype = torch.bfloat16 if (device.startswith("cuda") and torch.cuda.is_available()) else torch.float32

        dtype_key = str(dtype).replace("torch.", "")
        cache_key = (load_path, quantization, device, dtype_key)

        kwargs = {
            "torch_dtype": dtype,
            "device_map": "auto" if device.startswith("cuda") else {"": device},
        }

        cached = self._MODEL_CACHE.get(cache_key)
        if cached is not None:
            return cached

        if quantization in ("int8_bnb", "int4_bnb"):
            if not device.startswith("cuda"):
                raise RuntimeError("bitsandbytes requires a CUDA device.")
            try:
                from transformers import BitsAndBytesConfig
                import bitsandbytes
            except Exception as e:
                raise RuntimeError("BitsAndBytes missing.") from e

            if quantization == "int8_bnb":
                qconf = BitsAndBytesConfig(load_in_8bit=True)
            else:
                qconf = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_compute_dtype=dtype,
                )
            kwargs["quantization_config"] = qconf
        
        if flash_attention == "on":
            kwargs["attn_implementation"] = "flash_attention_2"
            
        if model_family == "qwen2_5_vl":
            self._MODEL_CACHE[cache_key] = Qwen2_5_VLForConditionalGeneration.from_pretrained(load_path, **kwargs)
        elif model_family == "qwen3_vl":
            self._MODEL_CACHE[cache_key] = Qwen3VLForConditionalGeneration.from_pretrained(load_path, **kwargs)
        
        self._MODEL_CACHE[cache_key].eval()
        return self._MODEL_CACHE[cache_key]
    
    def _generate_local(
        self,
        image_pil: Image.Image,
        model_id: str,
        load_path: str,
        device_choice: str,
        quantization: str,
        flash_attention: str,
        system_prompt: str,
        user_prompt: str,
        max_new_tokens: int,
        temperature: float,
        safe_quants: bool,
        unload_model: bool,
    ) -> str:
        model = self._load_local_model(model_id, load_path, device_choice, quantization, flash_attention, safe_quants)
        processor = self._get_processor(model_id, load_path)

        if system_prompt.strip() == "":
            text_instruction = "Convert the image into a rich image-generation prompt."
        else:
            text_instruction = system_prompt.strip()
        
        if user_prompt and user_prompt.strip():
            text_instruction = f"{text_instruction}\nAdditional requirements:\n{user_prompt.strip()}"
        
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_prompt.strip()}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_pil},
                    {"type": "text", "text": text_instruction},
                ],
            },
        ]

        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        )

        inputs = inputs.to(model.device)

        gen_kwargs = {
            "max_new_tokens": int(max_new_tokens),
        }
        if temperature and temperature > 0:
            gen_kwargs.update({"do_sample": True, "temperature": float(temperature), "top_p": 0.9})
        else:
            gen_kwargs.update({"do_sample": False})

        with torch.inference_mode():
            out_ids = model.generate(**inputs, **gen_kwargs)

        trimmed = [o[len(i):] for i, o in zip(inputs.input_ids, out_ids)]
        
        out_text = processor.batch_decode(
            trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]

        sep = "</think>"
        idx = out_text.find(sep)
        if idx != -1:
            pstart = idx + len(sep)
            prompt = out_text[pstart:]
            reasoning = out_text[:idx]
        else:
            reasoning = ""
            prompt = out_text

        if unload_model:
            for key in self._MODEL_CACHE:
                self._MODEL_CACHE[key] = None
            for key in self._PROC_CACHE:
                 self._PROC_CACHE[key] = None
            model = None
            processor = None
            inputs = None
            _cuda_cleanup(None)

        return _clean_single_line(prompt), reasoning

    def _generate_openai_compatible(
        self,
        image_pil: Image.Image,
        model_id: str,
        base_url: str,
        api_key: str,
        model_override: str,
        system_prompt: str,
        user_prompt: str,
        max_new_tokens: int,
        temperature: float,
        providers: str = "",
        verbose: bool = True,
    ) -> str:
        buf = BytesIO()
        image_pil.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        data_url = f"data:image/png;base64,{b64}"
        if system_prompt.strip() == "":                                                                         
            text_instruction = "Convert the image into a rich image-generation prompt."
        else:
            text_instruction = system_prompt.strip()
        if user_prompt and user_prompt.strip():
            text_instruction = f"{text_instruction}\nAdditional requirements:\n{user_prompt.strip()}"

        url = base_url.rstrip("/") + "/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        if api_key and api_key.strip():
            headers["Authorization"] = f"Bearer {api_key.strip()}"

        payload = {
            "model": (model_override.strip() if model_override and model_override.strip() else model_id),
            "messages": [
                {"role": "system", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_instruction},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                },
            ],
            "temperature": float(temperature),
            "max_tokens": int(max_new_tokens),
        }

        if providers and providers.strip():
            provider_list = [p.strip() for p in providers.split(",") if p.strip()]
            if provider_list:
                payload["provider"] = {
                    "order": provider_list,
                    "allow_fallbacks": False
                }

        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=600)
        if resp.status_code != 200:
            raise RuntimeError(f"OpenAI-compatible endpoint error {resp.status_code}: {resp.text}")

        data = resp.json()

        if verbose:
            provider = data.get("provider", "unknown")
            model = data.get("model", "unknown")
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            cost = usage.get("cost", 0)
            cached_tokens = usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)

            lines = [
                f"Provider: {provider}",
                f"Model: {model}",
                f"Tokens: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total",
            ]
            if cached_tokens > 0:
                lines.append(f"Cached: {cached_tokens} tokens")
            lines.append(f"Cost: ${cost:.6f}")

            width = max(len(line) for line in lines) + 2
            title = " OpenAI API Response "
            top_border = f"┌{title}{'─' * (width - len(title))}┐"
            bottom_border = f"└{'─' * width}┘"

            print(f"\n{top_border}")
            for line in lines:
                print(f"│ {line.ljust(width - 1)}│")
            print(f"{bottom_border}\n")

        reasoning = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("reasoning")
        )

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content")
        )

        if reasoning == None:
            reasoning = ""
        
        return _clean_single_line(content), reasoning

    def run(
        self,
        image,
        backend,
        qwen_model,
        local_model_path,
        device,
        quantization,
        flash_attention,
        system_prompt,
        user_prompt,
        max_new_tokens,
        temperature,
        safe_quants,
        unload_model,
        openai_base_url="http://127.0.0.1:11434",
        openai_api_key="",
        openai_model_override="",
        openrouter_providers="",
        verbose_output=True,
    ):
        image_pil = _tensor_image_to_pil(image)
        load_path = local_model_path.strip() if local_model_path.strip() else qwen_model

        if backend == "openai_compatible":
            if not openai_api_key or not openai_api_key.strip():
                if "OPENROUTER_API_KEY" in os.environ:
                    openai_api_key = os.environ.get("OPENROUTER_API_KEY", "")
                    if openai_base_url in ("http://127.0.0.1:11434", "") or not openai_base_url.strip():
                        openai_base_url = "https://openrouter.ai/api"
                elif "OPENAI_API_KEY" in os.environ:
                    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
                
            prompt, reasoning = self._generate_openai_compatible(
                image_pil=image_pil,
                model_id=qwen_model,
                base_url=openai_base_url,
                api_key=openai_api_key,
                model_override=openai_model_override,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                providers=openrouter_providers,
                verbose=verbose_output,
            )
        else:
            prompt, reasoning = self._generate_local(
                image_pil=image_pil,
                model_id=qwen_model,
                load_path=load_path,
                device_choice=device,
                quantization=quantization,
                flash_attention=flash_attention,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                safe_quants=safe_quants,
                unload_model=unload_model
            )

        return (prompt,reasoning,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenPromptFromImage": EmAySee_QwenPromptFromImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenPromptFromImage": "EmAySee_Qwen / OpenAI Prompt From Image",
}