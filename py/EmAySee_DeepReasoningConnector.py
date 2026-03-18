import requests
import json
import re
import time

class EmAySee_DeepReasoningConnector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "Enter prompt here"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a helpful assistant."}),
                "api_url": ("STRING", {"default": "http://10.0.0.71:5000/v1/chat/completions"}),
                "api_key": ("STRING", {"default": "supersecretkey"}),
                "model_name": ("STRING", {"default": "default"}),
                "max_tokens_per_call": ("INT", {"default": 4096, "min": 1, "max": 8192, "step": 64}),
                "truncation_length": ("INT", {"default": 32768, "min": 0, "max": 131072, "step": 512}),
                "temperature": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 2.0, "step": 0.05}),
                "top_p": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01}),
                "min_p": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "min": 0, "max": 200}),
                "repetition_penalty": ("FLOAT", {"default": 1.15, "min": 1.0, "max": 2.0, "step": 0.01}),
                "repetition_penalty_range": ("INT", {"default": 2048, "min": 0, "max": 8192, "step": 64}),
                "reasoning_effort": (["low", "medium", "high"], {"default": "low"}),
                "xtc_threshold": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01}),
                "xtc_probability": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "dry_multiplier": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.1}),
                "dry_base": ("FLOAT", {"default": 1.75, "min": 1.0, "max": 5.0, "step": 0.05}),
                "dry_allowed_length": ("INT", {"default": 1, "min": 0, "max": 20}),
                "auto_continue": ("BOOLEAN", {"default": True}),
                "max_continues": ("INT", {"default": 3, "min": 1, "max": 10}),
                "stop_on_error": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("answer", "thinking", "full_raw")
    FUNCTION = "execute_request"
    CATEGORY = "EmAySee/LLM"

    def execute_request(self, prompt, system_prompt, api_url, api_key, model_name, 
                        max_tokens_per_call, truncation_length, temperature, top_p, min_p, top_k,
                        repetition_penalty, repetition_penalty_range, reasoning_effort, 
                        xtc_threshold, xtc_probability, dry_multiplier, dry_base, 
                        dry_allowed_length, auto_continue, max_continues, stop_on_error):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        full_content = ""
        current_continue = 0
        
        while current_continue <= max_continues:
            payload = {
                "model": model_name,
                "messages": messages,
                "max_tokens": max_tokens_per_call,
                "truncation_length": truncation_length,
                "temperature": temperature,
                "top_p": top_p,
                "min_p": min_p,
                "top_k": top_k,
                "repetition_penalty": repetition_penalty,
                "repetition_penalty_range": repetition_penalty_range,
                "xtc_threshold": xtc_threshold,
                "xtc_probability": xtc_probability,
                "dry_multiplier": dry_multiplier,
                "dry_base": dry_base,
                "dry_allowed_length": dry_allowed_length,
                "enable_thinking": True,
                "reasoning_effort": reasoning_effort,
                "do_sample": True,
                "add_bos_token": False,
                "skip_special_tokens": True,
                "stream": False
            }

            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=600)
                
                if response.status_code != 200:
                    error_detail = response.text
                    print(f"!!! EmAySee Deep Reasoning Error [{response.status_code}] !!!")
                    print(f"Backend Response: {error_detail}")
                    if stop_on_error:
                        raise Exception(f"Backend Error {response.status_code}: {error_detail}")
                    return (f"Error {response.status_code}", "", error_detail)

                result_json = response.json()
                
                if "choices" in result_json and len(result_json["choices"]) > 0:
                    choice = result_json["choices"][0]
                    content = choice["message"]["content"]
                    finish_reason = choice.get("finish_reason", "")
                    
                    full_content += content
                    
                    usage = result_json.get("usage", {})
                    print(f"[EmAySee LLM] Chunk {current_continue + 1} | Context: {usage.get('total_tokens', '??')}/{truncation_length} | Finish: {finish_reason}")
                    
                    if not auto_continue or (finish_reason != "length" and finish_reason != "maxlen"):
                        break
                    
                    messages.append({"role": "assistant", "content": content})
                    current_continue += 1
                else:
                    if stop_on_error: raise Exception("No content in response")
                    return ("No content", "", str(result_json))

            except Exception as e:
                if stop_on_error: raise e
                return (f"Error: {str(e)}", "", "ERROR")

        #  Parsing results
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

        return (answer, thinking, full_content)

NODE_CLASS_MAPPINGS = {
    "EmAySee_DeepReasoningConnector": EmAySee_DeepReasoningConnector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_DeepReasoningConnector": "EmAySee Deep Reasoning Connector"
}