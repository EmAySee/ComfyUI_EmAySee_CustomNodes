import requests
import json
import re

class EmAySee_SubmitToOobaboogaAPIWithKeyThinker:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "api_url": ("STRING", {"default": "http://10.0.0.71:5000/v1/chat/completions"}),
                "api_key": ("STRING", {"default": "supersecretkey"}),
                "max_tokens": ("INT", {"default": 500, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.1, "max": 2.0, "step": 0.05}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "You are a helpful assistant.", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("clean_text", "thinking_content")
    FUNCTION = "submit_request"
    CATEGORY = "EmAySee/API"

    def submit_request(self, text, api_url, api_key, max_tokens, temperature, top_p, seed, system_prompt="You are a helpful assistant."):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Construct the payload for OpenAI-compatible API
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "seed": seed,
            "mode": "instruct", # Helpful for some Ooba configs
            "stream": False
        }

        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            
            result_json = response.json()
            
            # Extract content from OpenAI format
            if "choices" in result_json and len(result_json["choices"]) > 0:
                raw_content = result_json["choices"][0]["message"]["content"]
            else:
                raw_content = ""
                print(f"EmAySee_SubmitToOobaboogaAPIWithKeyThinker: No content in response: {result_json}")

            # --- Logic to separate <think> content from clean text ---
            
            # 1. Extract thinking content
            think_match = re.search(r'<think>(.*?)</think>', raw_content, flags=re.DOTALL)
            thinking_content = think_match.group(1).strip() if think_match else ""

            # 2. Remove thinking tags to get clean text
            clean_text = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()

            return (clean_text, thinking_content)

        except Exception as e:
            print(f"EmAySee_SubmitToOobaboogaAPIWithKeyThinker Error: {e}")
            return (f"Error: {str(e)}", "")

NODE_CLASS_MAPPINGS = {
    "EmAySee_SubmitToOobaboogaAPIWithKeyThinker": EmAySee_SubmitToOobaboogaAPIWithKeyThinker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SubmitToOobaboogaAPIWithKeyThinker": "EmAySee Submit To Oobabooga API With Key With THinkParse"
}