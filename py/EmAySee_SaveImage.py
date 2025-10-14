import os
import time
from PIL import Image, PngImagePlugin
import numpy as np
import folder_paths
import json


class EmAySee_SaveImage:
    """
    A custom ComfyUI node to save images with advanced filename customization.
    """

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "subfolder": ("STRING", {"default": ""}),
                "name_postfix": ("STRING", {"default": "image_"}),
                "timestamp_format": (["none", "YYYYMMDDHHMMSS"], {"default": "YYYYMMDDHHMMSS"}),  # Removed .f option
                "name_prefix": ("STRING", {"default": ""}),
                "separator": ("STRING", {"default": "_"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee/Image"

    def save_images(self, images, subfolder="", name_postfix="image_", timestamp_format="YYYYMMDDHHMMSS", name_prefix="", separator="_", prompt=None, extra_pnginfo=None):
        full_output_folder = os.path.join(self.output_dir, subfolder) if subfolder else self.output_dir

        if not os.path.exists(full_output_folder):
            os.makedirs(full_output_folder)

        results = list()
        filepaths = list()

        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            # --- Filename Construction ---
            filename_parts = []

            # Add name prefix (if provided)
            if name_prefix:
                filename_parts.append(name_prefix)

            # Add timestamp (if selected)
            if timestamp_format != "none":
                if timestamp_format == "YYYYMMDDHHMMSS":
                    timestamp = time.strftime("%Y%m%d%H%M%S")  # Keep only YYYYMMDDHHMMSS
                # No else needed, as the only other option is "none"
                filename_parts.append(timestamp)

            # Add the base filename postfix
            filename_parts.append(name_postfix)

            # Join the parts with the separator
            file_name = separator.join(filename_parts)
            file = f"{file_name}"  # comfyui counter
            file_path = os.path.join(full_output_folder, f"{file}.png")

            filepaths.append(file_path)

            # --- Metadata Handling ---
            if extra_pnginfo is not None:
                pnginfo = PngImagePlugin.PngInfo()
                for k, v in extra_pnginfo.items():
                    if isinstance(v, dict):
                        v = json.dumps(v)
                    elif not isinstance(v, str):
                        v = str(v)
                    pnginfo.add_text(k, v)
            else:
                pnginfo = None

            img.save(file_path, pnginfo=pnginfo)

            results.append({
                "filename": f"{file}.png",
                "subfolder": subfolder,
                "type": self.type
            })

        return (filepaths, {"ui": { "images": results }})


NODE_CLASS_MAPPINGS = {
    "EmAySee_SaveImage": EmAySee_SaveImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SaveImage": "Save Image (EmAySee)"
}