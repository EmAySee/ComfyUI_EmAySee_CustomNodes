import os
import folder_paths

class EmAySee_SaveTextToFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_to_save": ("STRING", {"multiline": True}),
                "filename": ("STRING", {"default": "output_text"}),
                "subfolder": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee/Utils"

    def save_text(self, text_to_save, filename, subfolder):
        if os.path.isabs(filename):
            full_path_input = filename
        elif subfolder.startswith("/") or (len(subfolder) > 1 and subfolder[1] == ":"):
            full_path_input = os.path.join(subfolder, filename)
        else:
            output_dir = folder_paths.get_output_directory()
            full_path_input = os.path.join(output_dir, subfolder, filename)

        save_dir = os.path.dirname(full_path_input)
        base_name = os.path.basename(full_path_input)

        os.makedirs(save_dir, exist_ok=True)

        if base_name.lower().endswith(".txt"):
            base_name = base_name[:-4]

        safe_filename = "".join(c for c in base_name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
        if not safe_filename:
            safe_filename = "output_text"

        file_path = os.path.join(save_dir, f"{safe_filename}.txt")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_to_save)
            print(f"[EmAySee] Successfully saved text to: {file_path}")
        except Exception as e:
            print(f"[EmAySee] CRITICAL Error saving text to {file_path}: {e}")

        return ()

NODE_CLASS_MAPPINGS = {
    "EmAySee_SaveTextToFile": EmAySee_SaveTextToFile
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SaveTextToFile": "EmAySee Save Text to File"
}