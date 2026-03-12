import requests
import json
import re

class EmAySee_AdvancedOobaboogaConnector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_url": ("STRING", {"default": "http://10.0.0.71:5000/v1/chat/completions"}),
                "api_key": ("STRING", {"default": "supersecretkey"}),
                "prompt": ("STRING", {"multiline": True, "default": "Enter prompt here"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a helpful assistant."}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff, "control_after_generate": True}),
                "max_tokens": ("INT", {"default": 512, "min": 1, "max": 32768}),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "top_p": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "min_p": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 0, "min": 0, "max": 200}),
                "repetition_penalty": ("FLOAT", {"default": 1.0, "min": 1.0, "max": 2.0, "step": 0.01}),
                "reasoning_effort": (["low", "medium", "high"], {"default": "medium"}),
                "auto_continue": ("BOOLEAN", {"default": False}),
                "max_continues": ("INT", {"default": 3, "min": 1, "max": 10}),
                "stop_on_error": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "best_of": ("INT", {"default": 1, "min": 1, "max": 10}),
                "echo": ("BOOLEAN", {"default": False}),
                "frequency_penalty": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "presence_penalty": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "n": ("INT", {"default": 1, "min": 1, "max": 10}),
                "suffix": ("STRING", {"default": ""}),
                "user": ("STRING", {"default": ""}),
                "preset": ("STRING", {"default": ""}),
                "dynatemp_low": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "dynatemp_high": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "dynatemp_exponent": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "smoothing_factor": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "smoothing_curve": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "typical_p": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "xtc_threshold": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01}),
                "xtc_probability": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "epsilon_cutoff": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "eta_cutoff": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "tfs": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_a": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_n_sigma": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "dry_multiplier": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "dry_allowed_length": ("INT", {"default": 2, "min": 0, "max": 20}),
                "dry_base": ("FLOAT", {"default": 1.75, "min": 1.0, "max": 5.0, "step": 0.01}),
                "encoder_repetition_penalty": ("FLOAT", {"default": 1.0, "min": 1.0, "max": 2.0, "step": 0.01}),
                "no_repeat_ngram_size": ("INT", {"default": 0, "min": 0, "max": 20}),
                "repetition_penalty_range": ("INT", {"default": 1024, "min": 0, "max": 8192}),
                "penalty_alpha": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "guidance_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "mirostat_mode": ("INT", {"default": 0, "min": 0, "max": 2}),
                "mirostat_tau": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "mirostat_eta": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01}),
                "prompt_lookup_num_tokens": ("INT", {"default": 0, "min": 0, "max": 20}),
                "max_tokens_second": ("INT", {"default": 0, "min": 0, "max": 32768}),
                "do_sample": ("BOOLEAN", {"default": True}),
                "dynamic_temperature": ("BOOLEAN", {"default": False}),
                "temperature_last": ("BOOLEAN", {"default": False}),
                "auto_max_new_tokens": ("BOOLEAN", {"default": False}),
                "ban_eos_token": ("BOOLEAN", {"default": False}),
                "add_bos_token": ("BOOLEAN", {"default": True}),
                "enable_thinking": ("BOOLEAN", {"default": True}),
                "skip_special_tokens": ("BOOLEAN", {"default": True}),
                "static_cache": ("BOOLEAN", {"default": False}),
                "truncation_length": ("INT", {"default": 0, "min": 0, "max": 131072}),
                "custom_token_bans": ("STRING", {"default": ""}),
                "negative_prompt": ("STRING", {"default": ""}),
                "dry_sequence_breakers": ("STRING", {"default": '"\\n", ":", "\\"", "*"'}),
                "grammar_string": ("STRING", {"multiline": True, "default": ""}),
                "sampler_priority": ("STRING", {"multiline": True, "default": ""}),
                "stop_sequences": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("answer", "thinking", "full_raw")
    FUNCTION = "execute_request"
    CATEGORY = "EmAySee/LLM"

    def execute_request(self, api_url, api_key, prompt, system_prompt, seed, max_tokens, 
                        temperature, top_p, min_p, top_k, repetition_penalty, 
                        reasoning_effort, auto_continue, max_continues, stop_on_error, **kwargs):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        schema_defaults = {
            "best_of": 1, "echo": False, "frequency_penalty": 0.0, "presence_penalty": 0.0,
            "n": 1, "suffix": "", "user": "", "preset": "", "dynatemp_low": 1.0,
            "dynatemp_high": 1.0, "dynatemp_exponent": 1.0, "smoothing_factor": 0.0,
            "smoothing_curve": 1.0, "typical_p": 1.0, "xtc_threshold": 0.1,
            "xtc_probability": 0.0, "epsilon_cutoff": 0.0, "eta_cutoff": 0.0,
            "tfs": 1.0, "top_a": 0.0, "top_n_sigma": 0.0, "dry_multiplier": 0.0,
            "dry_allowed_length": 2, "dry_base": 1.75, "encoder_repetition_penalty": 1.0,
            "no_repeat_ngram_size": 0, "repetition_penalty_range": 1024, "penalty_alpha": 0.0,
            "guidance_scale": 1.0, "mirostat_mode": 0, "mirostat_tau": 5.0, "mirostat_eta": 0.1,
            "prompt_lookup_num_tokens": 0, "max_tokens_second": 0, "do_sample": True,
            "dynamic_temperature": False, "temperature_last": False, "auto_max_new_tokens": False,
            "ban_eos_token": False, "add_bos_token": True, "enable_thinking": True,
            "skip_special_tokens": True, "static_cache": False, "truncation_length": 0,
            "custom_token_bans": "", "negative_prompt": "", "grammar_string": "",
            "dry_sequence_breakers": '"\\n", ":", "\\"", "*"', "sampler_priority": "",
            "stop_sequences": ""
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        full_content = ""
        current_continue = 0
        last_json_response = {}

        while current_continue <= max_continues:
            payload = {
                "messages": messages,
                "seed": seed,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "min_p": min_p,
                "top_k": top_k,
                "repetition_penalty": repetition_penalty,
                "reasoning_effort": reasoning_effort,
                "stream": False
            }

            for key, default_val in schema_defaults.items():
                current_val = kwargs.get(key, default_val)
                if current_val != default_val:
                    if key == "sampler_priority" and current_val.strip():
                        payload[key] = [s.strip() for s in current_val.split(",") if s.strip()]
                    elif key == "stop_sequences" and current_val.strip():
                        payload["stop"] = [s.strip() for s in current_val.split(",") if s.strip()]
                    else:
                        payload[key] = current_val

            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=600)
                if response.status_code != 200:
                    if stop_on_error:
                        raise Exception(f"Backend Error {response.status_code}: {response.text}")
                    return (f"Error {response.status_code}", "", response.text)

                result_json = response.json()
                last_json_response = result_json
                
                if "choices" in result_json and len(result_json["choices"]) > 0:
                    choice = result_json["choices"][0]
                    content = choice["message"]["content"]
                    finish_reason = choice.get("finish_reason", "")
                    
                    full_content += content
                    
                    if not auto_continue or (finish_reason != "length" and finish_reason != "maxlen"):
                        break
                    
                    messages.append({"role": "assistant", "content": content})
                    current_continue += 1
                else:
                    if stop_on_error:
                        raise Exception("No content in response")
                    return ("No content in response", "", str(result_json))

            except Exception as e:
                if stop_on_error:
                    raise e
                return (f"Connection Error: {str(e)}", "", "ERROR")

        think_pattern = r'<(?:think|thought)>(.*?)</(?:think|thought)>'
        think_match = re.search(think_pattern, full_content, flags=re.DOTALL | re.IGNORECASE)
        
        if think_match:
            thinking = think_match.group(1).strip()
            answer = re.sub(think_pattern, '', full_content, flags=re.DOTALL | re.IGNORECASE).strip()
        else:
            if "<think>" in full_content.lower():
                start_idx = full_content.lower().find("<think>") + 7
                thinking = full_content[start_idx:].strip()
                answer = "[REASONING TRUNCATED]"
            else:
                thinking = ""
                answer = full_content.strip()

        return (answer, thinking, json.dumps(last_json_response, indent=2))

NODE_CLASS_MAPPINGS = {
    "EmAySee_AdvancedOobaboogaConnector": EmAySee_AdvancedOobaboogaConnector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_AdvancedOobaboogaConnector": "EmAySee Advanced Oobabooga Connector"
}