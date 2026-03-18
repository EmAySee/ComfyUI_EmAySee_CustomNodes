import os
import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

class EmAySee_VisualMachine_SaveImageAndText_V2:
    def __init__(self):
        self.output_dir = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "SPECTRE"}),
                "history_text": ("STRING", {"forceInput": True}),
                "current_prompt": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee_Automation/Image"

    def save_images(self, images, filename_prefix, history_text, current_prompt):
        from nodes import get_comfy_root
        
        full_output_folder = os.path.join(get_comfy_root(), self.output_dir)
        if not os.path.exists(full_output_folder):
            os.makedirs(full_output_folder, mode=0o777, exist_ok=True)

        results = list()
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            #  1. Handle Naming
            #  Uses the prefix as the base name; extension replacement happens here
            file_base = f"{filename_prefix}"
            image_file = f"{file_base}.png"
            log_file = f"{file_base}.txt"
            
            image_path = os.path.join(full_output_folder, image_file)
            log_path = os.path.join(full_output_folder, log_file)

            #  2. Save the Image
            img.save(image_path, pnginfo=None, compress_level=4)

            #  3. Save the Companion Text File
            entry = (
                f"--- SPECTRE V2 METADATA ---\n"
                f"FILENAME: {image_file}\n"
                f"METADATA_FILE: {log_file}\n"
                f"PROMPT: {current_prompt}\n"
                f"STATE HISTORY:\n{history_text}\n"
                f"----------------------------"
            )
            
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(entry)

        return {"ui": {"images": [{"filename": image_file, "subfolder": "", "type": "output"}]}}

NODE_CLASS_MAPPINGS = {"EmAySee_VisualMachine_SaveImageAndText_V2": EmAySee_VisualMachine_SaveImageAndText_V2}
NODE_DISPLAY_NAME_MAPPINGS = {"EmAySee_VisualMachine_SaveImageAndText_V2": "EmAySee VisualMachine Save Image And Text V2"}