import re

class EmAySee_LLMOutputCleaner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clean_text",)
    FUNCTION = "clean_text"
    CATEGORY = "EmAySee/Utils"

    def clean_text(self, text):
        # 1. Remove <think>...</think> blocks (DeepSeek/Reasoning models)
        # flags=re.DOTALL ensures the dot matches newlines inside the think block
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # 2. Remove common "Here is the thinking process:" preambles if they exist
        # (Optional, but helps with some chatty models)
        # cleaned = re.sub(r'(?i)here[\'s\s]+the\s+thinking.*?:', '', cleaned)

        # 3. Clean up extra whitespace left behind
        cleaned = cleaned.strip()
        
        return (cleaned,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LLMOutputCleaner": EmAySee_LLMOutputCleaner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LLMOutputCleaner": "EmAySee LLM Output Cleaner"
}