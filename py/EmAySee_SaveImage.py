import os
import json
import torch
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args
import folder_paths

class EmAySee_SaveImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "save_metadata": ("BOOLEAN", {"default": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee_Nodes/Image"

    def save_images(self, images, filename_prefix="ComfyUI", save_metadata=True, prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        
        is_absolute = os.path.isabs(filename_prefix) or ".." in filename_prefix or "/" in filename_prefix or "\\" in filename_prefix
        
        if is_absolute:
            full_output_folder = os.path.dirname(filename_prefix)
            if not os.path.exists(full_output_folder):
                os.makedirs(full_output_folder, exist_ok=True)
            filename = os.path.basename(filename_prefix)
            subfolder = ""
            
            # Simple manual counter for absolute paths
            files = os.listdir(full_output_folder)
            existing_counters = []
            for f in files:
                if f.startswith(filename) and "_" in f:
                    parts = f.split("_")
                    for p in parts:
                        if p.isdigit():
                            existing_counters.append(int(p))
            counter = max(existing_counters) + 1 if existing_counters else 1
        else:
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])

        results = list()
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if save_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for r in extra_pnginfo:
                        metadata.add_text(r, json.dumps(extra_pnginfo[r]))

            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return {"ui": {"images": results}}

NODE_CLASS_MAPPINGS = {
    "EmAySee_SaveImage": EmAySee_SaveImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SaveImage": "EmAySee Save Image"
}