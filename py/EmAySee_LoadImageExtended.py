import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

class EmAySee_LoadImageExtended:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = folder_paths.get_filename_list("input")
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True})
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT", "INT", "STRING")
    RETURN_NAMES = ("image", "mask", "width", "height", "filename")
    FUNCTION = "load"
    CATEGORY = "EmAySee/Image"

    def load(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        
        image_rgb = img.convert("RGB")
        image_np = np.array(image_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]
        
        if 'A' in img.getbands():
            mask = np.array(img.getchannel('A')).astype(np.float32) / 255.0
            mask_tensor = 1.0 - torch.from_numpy(mask)[None,]
        else:
            mask_tensor = torch.zeros((1, img.height, img.width), dtype=torch.float32)
            
        return (image_tensor, mask_tensor, img.width, img.height, os.path.basename(image_path))

NODE_CLASS_MAPPINGS = {
    "EmAySee_LoadImageExtended": EmAySee_LoadImageExtended
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoadImageExtended": "EmAySee Load Image Extended"
}