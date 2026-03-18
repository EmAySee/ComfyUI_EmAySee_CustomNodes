import os

class EmAySee_ContextWriter_V5:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "/full/path/to/prompt_v2.txt"}),
                "text_to_append": ("STRING", {"forceInput": True}),
                "max_history": ("INT", {"default": 4, "min": 1, "max": 20}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "write_context"
    CATEGORY = "EmAySee_Automation/Context"

    def write_context(self, file_path, text_to_append, max_history):
        #  1. Truncation Guard
        if "[REASONING TRUNCATED]" in text_to_append:
            raise ValueError(f"CRITICAL ERROR: LLM Output was truncated. Workflow halted to prevent history corruption.")

        #  2. Path Validation
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path), mode=0o777, exist_ok=True)

        #  3. Read existing to manage history length
        history = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                history = [block for block in content.split("---") if "STATE:" in block]

        #  4. Append New Entry
        history.append(text_to_append)
        
        #  5. Keep only the last N entries
        history = history[-max_history:]
        
        #  6. Rewrite file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---".join(history))

        return (text_to_append,)

NODE_CLASS_MAPPINGS = {"EmAySee_ContextWriter_V5": EmAySee_ContextWriter_V5}
NODE_DISPLAY_NAME_MAPPINGS = {"EmAySee_ContextWriter_V5": "EmAySee Context Writer V5"}