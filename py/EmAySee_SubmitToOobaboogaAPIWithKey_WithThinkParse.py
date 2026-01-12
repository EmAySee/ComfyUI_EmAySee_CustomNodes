import requests
import json
import re

class EmAySee_SubmitToOobaboogaAPIWithKey_WithThinkParse:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "api_url": ("STRING", {"default": "http://10.0.0.71:5000/v1/chat/completions"}),
                "api_key": ("STRING", {"default": "supersecretkey"}),
                "model_name": ("STRING", {"default": "default"}), 
                "max_tokens": ("INT", {"default": 500, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.1, "max": 2.0, "step": 0.05}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "min": 0, "max": 200}),
                "min_p": ("FLOAT", {"default": 0.05, "min": 0.0, "max": 1.0, "step": 0.01}),
                "repetition_penalty": ("FLOAT", {"default": 1.15, "min": 1.0, "max": 2.0, "step": 0.01}),
                "frequency_penalty": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "presence_penalty": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.05}),
                "dry_multiplier": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2.0, "step": 0.1}), 
                "dry_base": ("FLOAT", {"default": 1.75, "min": 1.0, "max": 5.0, "step": 0.05}), 
                "dry_allowed_length": ("INT", {"default": 2, "min": 0, "max": 20}), 
                "enable_thinking": ("BOOLEAN", {"default": True}),
                # New Parameter: reasoning_effort
                "reasoning_effort": (["low", "medium", "high"], {"default": "medium"}),
                "guidance_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "You are a helpful assistant.", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "stop": ("STRING", {"default": "", "multiline": False, "placeholder": "comma, separated, stop, strings"}),
                "instruction_template": ("STRING", {"default": "", "placeholder": "e.g. Qwen, Alpaca, ChatML"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("clean_text", "thinking_content")
    FUNCTION = "submit_request"
    CATEGORY = "EmAySee/API"

    def submit_request(self, text, api_url, api_key, model_name, max_tokens, temperature, top_p, top_k, min_p, repetition_penalty, frequency_penalty, presence_penalty, dry_multiplier, dry_base, dry_allowed_length, enable_thinking, reasoning_effort, guidance_scale, seed, system_prompt="You are a helpful assistant.", negative_prompt="", stop="", instruction_template=""):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        stop_list = [s.strip() for s in stop.split(",")] if stop and stop.strip() else []

        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "min_p": min_p,
            "repetition_penalty": repetition_penalty,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "dry_multiplier": dry_multiplier,
            "dry_base": dry_base,
            "dry_allowed_length": dry_allowed_length,
            "enable_thinking": enable_thinking,
            "reasoning_effort": reasoning_effort, # Added here
            "guidance_scale": guidance_scale,
            "negative_prompt": negative_prompt,
            "instruction_template": instruction_template,
            "seed": seed,
            "mode": "instruct", 
            "stream": False
        }

        if stop_list:
            data["stop"] = stop_list

        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            
            result_json = response.json()
            
            if "choices" in result_json and len(result_json["choices"]) > 0:
                raw_content = result_json["choices"][0]["message"]["content"]
            else:
                raw_content = ""
                print(f"EmAySee_SubmitToOobaboogaAPIWithKey: No content in response: {result_json}")

            # 1. Extract thinking content
            think_match = re.search(r'<think>(.*?)</think>', raw_content, flags=re.DOTALL)
            thinking_content = think_match.group(1).strip() if think_match else ""

            # 2. Remove thinking tags to get clean text
            clean_text = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()

            return (clean_text, thinking_content)

        except Exception as e:
            print(f"EmAySee_SubmitToOobaboogaAPIWithKey Error: {e}")
            return (f"Error: {str(e)}", "")

NODE_CLASS_MAPPINGS = {
    "EmAySee_SubmitToOobaboogaAPIWithKey_WithThinkParse": EmAySee_SubmitToOobaboogaAPIWithKey_WithThinkParse
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SubmitToOobaboogaAPIWithKey_WithThinkParse": "EmAySee Submit To Oobabooga API With Key With Think Parse"
}