import os
import numpy as np
from PIL import Image

class EmAySee_SaveImageExact:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "path": ("STRING", {"default": "/ai/training/"}),
                "filename": ("STRING", {"default": "image.png"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_exact"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee/Image"

    def save_exact(self, images, path, filename):
        os.makedirs(path, exist_ok=True)

        for i, image in enumerate(images):
            img_arr = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(img_arr, 0, 255).astype(np.uint8))
            
            if len(images) > 1:
                name, ext = os.path.splitext(filename)
                current_filename = f"{name}_{i}{ext}"
            else:
                current_filename = filename
                
            full_path = os.path.join(path, current_filename)
            
            try:
                img.save(full_path)
                print(f"[EmAySee] Saved image to: {full_path}")
            except Exception as e:
                print(f"[EmAySee] CRITICAL Error saving image to {full_path}: {e}")

        return ()

NODE_CLASS_MAPPINGS = {
    "EmAySee_SaveImageExact": EmAySee_SaveImageExact
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SaveImageExact": "EmAySee Save Image Exact"
}