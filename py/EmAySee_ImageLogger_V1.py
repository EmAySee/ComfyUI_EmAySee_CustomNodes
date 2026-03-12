import os

class EmAySee_ImageLogger:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "log_directory": ("STRING", {"default": "user/default/emaysee_logs"}),
                "log_filename": ("STRING", {"default": "production_log.txt"}),
                "history_text": ("STRING", {"forceInput": True}),
                "current_prompt": ("STRING", {"forceInput": True}),
                "generated_name": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log_entry",)
    FUNCTION = "log_data"
    CATEGORY = "EmAySee_Automation/Logging"
    OUTPUT_NODE = True

    def log_data(self, log_directory, log_filename, history_text, current_prompt, generated_name):
        from nodes import get_comfy_root
        
        abs_dir = os.path.join(get_comfy_root(), log_directory)
        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir, mode=0o777, exist_ok=True)
            
        file_path = os.path.join(abs_dir, log_filename)
        
        entry = f"--- NEW ENTRY ---\nFILE: {generated_name}\nPROMPT: {current_prompt}\nSTATE HISTORY:\n{history_text}\n\n"
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
            
        return (entry,)

NODE_CLASS_MAPPINGS = {"EmAySee_ImageLogger": EmAySee_ImageLogger}
NODE_DISPLAY_NAME_MAPPINGS = {"EmAySee_ImageLogger": "EmAySee Image Logger V1"}