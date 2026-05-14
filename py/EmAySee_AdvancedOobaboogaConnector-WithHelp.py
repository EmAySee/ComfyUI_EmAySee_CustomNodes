import requests
import json
import re

class EmAySee_AdvancedOobaboogaConnector_WithHelp:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_url": ("STRING", {
                    "default": "http://10.0.0.71:5000/v1/chat/completions",
                    "tooltip": "API Endpoint URL: The network address where your LLM server is listening. This routes your prompt to the backend generation engine."
                }),
                "api_key": ("STRING", {
                    "default": "supersecretkey",
                    "tooltip": "API Key: The authorization token required to access the backend server. Prevents unauthorized execution if your API is exposed."
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Enter prompt here",
                    "tooltip": "Prompt: The main user input or instruction. This is the direct context or question the LLM will respond to."
                }),
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "You are a helpful assistant.",
                    "tooltip": "System Prompt: The foundational instructions given to the LLM before your main prompt. It defines the AI's persona, rules, memory, and behavioral constraints."
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0xffffffffffffffff,
                    "control_after_generate": True,
                    "tooltip": "Seed: The initialization number for the random number generator. Using the same seed with identical settings guarantees the exact same text output. -1 generates a random seed each time."
                }),
                "max_tokens": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 32768,
                    "tooltip": "Max Tokens: The absolute maximum number of words or sub-words the model is allowed to generate in a single response. Acts as a hard stop to prevent runaway generation."
                }),
                "temperature": ("FLOAT", {
                    "default": 0.78,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Temperature: Modifies token probabilities. >1.0 flattens the distribution, increasing randomness and creativity. <1.0 sharpens the distribution, making the model strictly pick highly probable, deterministic words. 0.0 is entirely greedy."
                }),
                "top_p": ("FLOAT", {
                    "default": 0.95,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Top-P (Nucleus Sampling): Sorts tokens by probability and keeps adding them to a pool until their combined probability hits this limit. 0.95 discards the bottom 5% of unlikely tokens, cutting off the 'long tail' of gibberish."
                }),
                "min_p": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Min-P: Sets a dynamic probability threshold relative to the most likely token. A value of 0.05 means any token with less than 5% of the top token's probability is instantly discarded. Excellent for maintaining coherence."
                }),
                "top_k": ("INT", {
                    "default": 20,
                    "min": 0,
                    "max": 200,
                    "tooltip": "Top-K: A hard, absolute limit on the number of token choices considered. 20 means the model will only ever choose from the 20 most likely next words, stripping away all other possibilities."
                }),
                "repetition_penalty": ("FLOAT", {
                    "default": 1.0,
                    "min": 1.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Repetition Penalty: Divides the probability of tokens that have already appeared in the output by this value. >1.0 reduces looping. Setting it too high will cause the model to artificially avoid common grammar like 'the' or 'and'."
                }),
                "reasoning_effort": (["low", "medium", "high"], {
                    "default": "medium",
                    "tooltip": "Reasoning Effort: For advanced models supporting internal chain-of-thought. Dictates how much hidden compute time and context length the model dedicates to thinking before it begins outputting the final answer."
                }),
                "auto_continue": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Auto-Continue: If the model stops generating solely because it hit your 'Max Tokens' limit, enabling this will automatically append the generated text and ask the server to continue writing."
                }),
                "max_continues": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "tooltip": "Max Continues: The safety trigger for Auto-Continue. Prevents an infinite API loop by strictly capping how many consecutive times the node is allowed to ask the model to keep generating."
                }),
                "stop_on_error": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Stop on Error: If True, backend API errors (like timeouts or out-of-memory) will crash the ComfyUI workflow. If False, the node will output the error text and allow the workflow to proceed."
                }),
            },
            "optional": {
                "best_of": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "tooltip": "Best Of: Generates this number of full completions entirely on the server side, evaluates them, and only returns the single completion with the highest overall token probability score. Extremely compute-heavy."
                }),
                "echo": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Echo: Forces the server to prepend your exact input prompt to the beginning of the generated output text."
                }),
                "frequency_penalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Frequency Penalty: Subtracts from a token's logit score based on exactly how many times it has ALREADY appeared in the text. Directly punishes repetitive vocabulary."
                }),
                "presence_penalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Presence Penalty: Applies a flat, one-time penalty to a token if it has appeared AT ALL in the generated text. Highly encourages the model to transition to new topics."
                }),
                "n": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "tooltip": "N: Instructs the API to generate multiple independent completions for a single prompt simultaneously. ComfyUI will only process the first choice with this specific node setup."
                }),
                "suffix": ("STRING", {
                    "default": "",
                    "tooltip": "Suffix: Text that the model expects to come immediately after its generation. Used heavily in fill-in-the-middle (FIM) coding tasks."
                }),
                "user": ("STRING", {
                    "default": "",
                    "tooltip": "User: A unique string identifying the end-user for backend logging or rate-limiting purposes."
                }),
                "preset": ("STRING", {
                    "default": "",
                    "tooltip": "Preset: The exact string name of a generation YAML preset saved in your Oobabooga text-generation-webui server. Overrides node parameters if defined."
                }),
                "dynatemp_low": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Dynamic Temperature Low: The minimum temperature floor. When the model is highly confident in its next token, temperature shifts toward this value to ensure logical consistency."
                }),
                "dynatemp_high": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Dynamic Temperature High: The maximum temperature ceiling. When the model is uncertain, temperature shifts toward this value to encourage creative exploration out of the uncertainty."
                }),
                "dynatemp_exponent": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "tooltip": "Dynamic Temperature Exponent: Controls the mathematical curve between dynatemp_low and dynatemp_high. Modifies how aggressively the temperature swings based on model confidence."
                }),
                "smoothing_factor": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "tooltip": "Smoothing Factor (Quadratic Sampling): Flattens extremely sharp spikes in the probability distribution. Makes the model slightly more likely to pick the 2nd or 3rd best token rather than constantly locking onto the absolute highest."
                }),
                "smoothing_curve": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "tooltip": "Smoothing Curve: Adjusts the shape of the mathematical curve applied by the Smoothing Factor."
                }),
                "typical_p": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Typical-P: Sorts tokens based on how close their probability is to the expected entropy (typicality) of the text, rather than pure likelihood. 1.0 disables it."
                }),
                "xtc_threshold": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "XTC Threshold: Exclude Top Choices threshold. Any token with a probability higher than this value becomes eligible to be completely removed from consideration."
                }),
                "xtc_probability": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "XTC Probability: The random chance (0.0 to 1.0) that the tokens exceeding the XTC Threshold will actually be deleted. Forces the model into extreme lateral thinking by stripping the most obvious answers."
                }),
                "epsilon_cutoff": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Epsilon Cutoff: A hard probability floor. Any token with a raw probability below this exact decimal value is instantly discarded. A flat alternative to min_p."
                }),
                "eta_cutoff": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Eta Cutoff: A dynamic entropy-based cutoff. Similar to epsilon, but the threshold scales based on the overall uncertainty of the current token distribution."
                }),
                "tfs": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Tail Free Sampling (TFS): Looks at the mathematical second derivative of the probability curve to find the exact point where probabilities drop off a cliff, and cuts the 'tail' off there."
                }),
                "top_a": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Top-A: Squares the probability of the most likely token and multiplies it by this Top-A value to create a dynamic floor. Tokens below this dynamic floor are discarded."
                }),
                "top_n_sigma": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "tooltip": "Top N Sigma: Retains only the tokens whose probabilities fall within this many standard deviations from the mean probability of the distribution."
                }),
                "dry_multiplier": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "DRY Multiplier (Don't Repeat Yourself): The master switch for the DRY algorithm. Applies an exponentially growing penalty to repeating sequences of text. 0.0 disables."
                }),
                "dry_allowed_length": ("INT", {
                    "default": 2,
                    "min": 0,
                    "max": 20,
                    "tooltip": "DRY Allowed Length: How many tokens can perfectly match a previous sequence before the DRY exponential penalty triggers and forces the model to change course."
                }),
                "dry_base": ("FLOAT", {
                    "default": 1.75,
                    "min": 1.0,
                    "max": 5.0,
                    "step": 0.01,
                    "tooltip": "DRY Base: The base mathematical value for the DRY exponential curve. Higher values make the penalty scale violently faster as a sequence repeats."
                }),
                "encoder_repetition_penalty": ("FLOAT", {
                    "default": 1.0,
                    "min": 1.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Encoder Repetition Penalty: Applies specifically to the encoder phase of seq2seq models. Irrelevant for most standard decoder-only LLMs."
                }),
                "no_repeat_ngram_size": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 20,
                    "tooltip": "No Repeat N-Gram Size: An absolute rule. If set to 3, the model is physically incapable of ever generating the same sequence of 3 tokens twice in the entire output."
                }),
                "repetition_penalty_range": ("INT", {
                    "default": 1024,
                    "min": 0,
                    "max": 8192,
                    "tooltip": "Repetition Penalty Range: How far back in the context (in tokens) the model looks when calculating standard repetition penalties. Should generally match your expected output length."
                }),
                "penalty_alpha": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "tooltip": "Penalty Alpha (Contrastive Search): Balances token probability with a penalty based on similarity to recent context. 0.0 disables. Forces diverse phrasing."
                }),
                "guidance_scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 20.0,
                    "step": 0.1,
                    "tooltip": "Guidance Scale: Classifier-Free Guidance (CFG) for LLMs. Pushes the output toward the prompt and heavily away from the Negative Prompt. >1.0 activates CFG."
                }),
                "mirostat_mode": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2,
                    "tooltip": "Mirostat Mode: 0 = Off, 1 = V1, 2 = V2. Completely overrides Temperature and Top-P to automatically lock the text generation at a constant level of target 'surprise' (entropy)."
                }),
                "mirostat_tau": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.0,
                    "max": 20.0,
                    "step": 0.1,
                    "tooltip": "Mirostat Tau: The target entropy level for Mirostat. Higher values result in more surprising/creative text; lower values result in highly predictable text."
                }),
                "mirostat_eta": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Mirostat Eta: The learning rate. Controls how quickly the Mirostat algorithm reacts and corrects the temperature when the text strays from the target Tau entropy."
                }),
                "prompt_lookup_num_tokens": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 20,
                    "tooltip": "Prompt Lookup Tokens: Speculative decoding trick. The model scans the prompt for sequences matching its current generation and attempts to copy them wholesale to speed up generation."
                }),
                "max_tokens_second": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 32768,
                    "tooltip": "Max Tokens Second: A fallback/secondary token limit used by specific backend routing configurations."
                }),
                "do_sample": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Do Sample: If True, uses all your configured samplers (temp, top_p, etc). If False, executes 'Greedy Decoding', bypassing all math to strictly pick the #1 top token every single time."
                }),
                "dynamic_temperature": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Dynamic Temperature Enable: Master switch to turn on the dynatemp_low, dynatemp_high, and exponent scaling logic."
                }),
                "temperature_last": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Temperature Last: Shifts the Temperature calculation to the absolute end of the sampling pipeline, applying it after Top-K, Top-P, and min_p have made their cuts."
                }),
                "auto_max_new_tokens": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Auto Max New Tokens: Ignores your 'max_tokens' integer and automatically sets the generation limit to perfectly fill the absolute maximum remaining space in the model's context window."
                }),
                "ban_eos_token": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Ban EOS Token: Physically forbids the model from outputting the 'End Of Stream' token. Forces the model to keep generating text until it hits the max_tokens wall."
                }),
                "add_bos_token": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Add BOS Token: Automatically prepends the invisible 'Beginning Of Stream' token to your prompt. Most models require this to structure their context correctly."
                }),
                "enable_thinking": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable Thinking: Allows models programmed with explicit reasoning phases (like DeepSeek R1) to output their internal thought process tags (<think>)."
                }),
                "skip_special_tokens": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Skip Special Tokens: Strips backend formatting tokens (like <|endoftext|> or <|user|>) from the final returned string to keep the text clean."
                }),
                "static_cache": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Static Cache: Locks the Key-Value (KV) cache allocation in VRAM. Can improve continuous generation speed on some backends at the cost of rigid memory reservation."
                }),
                "truncation_length": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 131072,
                    "tooltip": "Truncation Length: If your combined prompt and history exceeds this number, the backend will forcibly slice off the oldest text to fit. 0 uses the model's innate maximum."
                }),
                "custom_token_bans": ("STRING", {
                    "default": "",
                    "tooltip": "Custom Token Bans: Comma-separated list of raw Token IDs (numbers, not words) that the model is strictly forbidden from ever generating."
                }),
                "negative_prompt": ("STRING", {
                    "default": "",
                    "tooltip": "Negative Prompt: Text describing exactly what you do NOT want. Only functions if Guidance Scale (CFG) is set higher than 1.0."
                }),
                "dry_sequence_breakers": ("STRING", {
                    "default": '"\\n", ":", "\\"", "*"',
                    "tooltip": "DRY Sequence Breakers: Specific characters or strings that immediately reset the DRY exponential repetition penalty back to zero when generated."
                }),
                "grammar_string": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Grammar String: A complex GBNF formatted string that forces the model to strictly adhere to a specific output format, such as a rigid JSON schema."
                }),
                "sampler_priority": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Sampler Priority: Comma-separated list defining the exact execution order of the math samplers (e.g., 'temperature, top_p, top_k'). Modifying this drastically changes generation logic."
                }),
                "stop_sequences": ("STRING", {
                    "default": "",
                    "tooltip": "Stop Sequences: Comma-separated words or symbols. If the model generates any of these exact sequences, it will instantly stop generating and return the text up to that point."
                }),
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
    "EmAySee_AdvancedOobaboogaConnector_WithHelp": EmAySee_AdvancedOobaboogaConnector_WithHelp
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_AdvancedOobaboogaConnector_WithHelp": "EmAySee Advanced Oobabooga Connector With Help"
}