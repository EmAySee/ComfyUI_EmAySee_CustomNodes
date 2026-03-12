import os

class EmAySee_GlobalStringReader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "O:/custom_nodes/storage"}),
                "file_name": ("STRING", {"default": "iteration_state"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "read_string"
    CATEGORY = "EmAySee/Logic"

    def read_string(self, path, file_name):
        full_path = os.path.join(path, f"{file_name}.txt")
        
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            
        if not os.path.exists(full_path):
            return ("",)
            
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        return (content,)

class EmAySee_GlobalStringUpdater:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {"forceInput": True}),
                "path": ("STRING", {"default": "O:/custom_nodes/storage"}),
                "file_name": ("STRING", {"default": "iteration_state"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("passthrough",)
    FUNCTION = "update_string"
    CATEGORY = "EmAySee/Logic"

    def update_string(self, input_text, path, file_name):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            
        state_path = os.path.join(path, f"{file_name}.txt")
        story_path = os.path.join(path, f"{file_name}-story.txt")
        
        with open(state_path, "w", encoding="utf-8") as f:
            f.write(input_text)
            
        with open(story_path, "a", encoding="utf-8") as f:
            f.write(input_text + "\n\n")
            
        return (input_text,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_GlobalStringReader": EmAySee_GlobalStringReader,
    "EmAySee_GlobalStringUpdater": EmAySee_GlobalStringUpdater
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_GlobalStringReader": "EmAySee Global String Reader",
    "EmAySee_GlobalStringUpdater": "EmAySee Global String Updater"
}