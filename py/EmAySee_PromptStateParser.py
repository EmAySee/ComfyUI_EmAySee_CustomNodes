class EmAySee_PromptStateParser:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_input": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "state")
    FUNCTION = "parse"
    CATEGORY = "EmAySee/Text"

    def parse(self, text_input):
        prompt_marker = "PROMPT:"
        state_marker = "STATE:"
        
        p_idx = text_input.find(prompt_marker)
        s_idx = text_input.find(state_marker)
        
        prompt_out = ""
        state_out = ""
        
        if p_idx != -1:
            start = p_idx + len(prompt_marker)
            if s_idx != -1 and s_idx > p_idx:
                prompt_out = text_input[start:s_idx].strip()
            else:
                prompt_out = text_input[start:].strip()
        
        if s_idx != -1:
            start = s_idx + len(state_marker)
            if p_idx != -1 and p_idx > s_idx:
                state_out = text_input[start:p_idx].strip()
            else:
                state_out = text_input[start:].strip()
                
        return (prompt_out, state_out)

NODE_CLASS_MAPPINGS = {
    "EmAySee_PromptStateParser": EmAySee_PromptStateParser
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_PromptStateParser": "EmAySee Prompt State Parser"
}