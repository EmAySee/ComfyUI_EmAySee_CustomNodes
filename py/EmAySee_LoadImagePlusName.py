import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

class EmAySee_LoadImagePlusName:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required": {"image": (sorted(files), {"image_upload": True})}}

    CATEGORY = "EmAySee"
    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filename_stem")
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image_out = i.convert("RGB")
        image_out = np.array(image_out).astype(np.float32) / 255.0
        image_out = torch.from_numpy(image_out)[None,]
        
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1.0 - mask
            mask = torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            
        filename_stem = os.path.splitext(os.path.basename(image))[0]
        
        return (image_out, mask.unsqueeze(0), filename_stem)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LoadImagePlusName": EmAySee_LoadImagePlusName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoadImagePlusName": "EmAySee Load Image + Name"
}