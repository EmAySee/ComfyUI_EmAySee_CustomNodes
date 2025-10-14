import requests
import json
import time

class EmAySee_SubmitToOobaboogaAPIWithKey:  # Class name now prefixed with EmAySee_
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "apikey_input": ("STRING", {"default": "Enter your api key here"}),
                "text_input": ("STRING", {"default": "Enter your prompt for text-generation-webui here"}),
                "api_endpoint": ("STRING", {"default": "http://10.0.0.57:5000/v1/completions"}),  # Default oobabooga COMPletions API endpoint - Non-streaming
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.01, "max": 2.0, "step": 0.01}), # Common oobabooga default
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),     # Common oobabooga default
                "top_k": ("INT", {"default": 0, "min": 0, "max": 200}), # 0 means disabled in oobabooga
                "typical_p": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}), # Common oobabooga default
                "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.01}), # Common oobabooga default                
                "max_new_tokens": (
                    ["25", "50", "75", "100", "125", "150", "175", "200", "250", "300", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800"],  # Dropdown options
                    {"default": "200"}  # Default, adjust as needed
                ),
                "seed": ("INT", {"default": -1, "label": "Seed (-1 for random)"}), # Added Seed - common in completions API
                "delay_seconds": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1, "label": "Delay (seconds)"}),
                "show_api_response": ("BOOLEAN", {"default": False, "label": "Show API Response in Console"}),
            },
            "optional": {
                # You can add 'stopping_strings' or other completion-specific parameters here later if needed
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_response",)
    OUTPUT_NODE = True
    FUNCTION = "submitToOobabooga"

    def submitToOobabooga(self, apikey_input, api_endpoint, text_input, temperature, top_p, top_k, typical_p, repetition_penalty, max_new_tokens, seed, delay_seconds, show_api_response, **kwargs): # Removed history_, added seed
        """
        Submits a request to the text-generation-webui (oobabooga) /v1/completions API for non-streaming text generation.
        Waits for the full response before returning.
        """
        payload = {
            "prompt": text_input,
            "max_tokens": int(max_new_tokens), # Use 'max_tokens' for /v1/completions
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "typical_p": typical_p,
            "repetition_penalty": repetition_penalty,
            "seed": seed, # Added seed to payload
            "stream": False # **Ensuring non-streaming: explicitly set stream to False**
            # Add other oobabooga /v1/completions parameters here as needed, consult API docs
        }

        headers = {
                   'Content-Type': 'application/json',
                   'Authorization': f'Bearer {apikey_input}' # <-- ADD THIS LINE
                  }
        try:
            time.sleep(delay_seconds)
            response = requests.post(api_endpoint, json=payload, headers=headers)
            response.raise_for_status()

            try:
                api_response = response.json()
            except json.JSONDecodeError:
                error_message = f"Oobabooga API returned non-JSON. Status: {response.status_code}. Text: {response.text}"
                print(error_message)
                return (error_message,)

            if show_api_response:
                print("Oobabooga API Response Content:")
                print(api_response)

            # Response parsing for /v1/completions endpoint - VERIFY AGAINST DOCS!
            if isinstance(api_response, dict) and 'choices' in api_response and api_response['choices']:
                api_response_text = api_response['choices'][0]['text'] # Expecting text directly under 'choices'-> 0 -> 'text' for /v1/completions
            elif isinstance(api_response, dict) and 'text' in api_response: # Fallback if API just returns text directly
                api_response_text = api_response['text']
            elif isinstance(api_response, str): # Fallback if API returns plain text string
                api_response_text = api_response
            else:
                error_message = f"Unexpected Oobabooga API response format for /v1/completions. JSON: {api_response}"
                print(error_message)
                return (error_message,)

            trimmed_text = api_response_text.strip()
            return (trimmed_text,)

        except requests.exceptions.RequestException as e:
            error_message = f"Oobabooga API Request Error: {e}. Status: {getattr(e.response, 'status_code', 'N/A')}. Content: {getattr(e.response, 'text', 'N/A')}"
            print(error_message)
            return (error_message,)


NODE_CLASS_MAPPINGS = {
    "EmAySee_SubmitToOobaboogaAPIWithKey": EmAySee_SubmitToOobaboogaAPIWithKey  # Class mapping with alias
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SubmitToOobaboogaAPIWithKey": "EmAySee Submit to Oobabooga API Node With API Key" # Display name with alias
}