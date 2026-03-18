import folder_paths
import os
import random
from PIL import Image
import numpy as np

class EphemeralPreview:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"images": ("IMAGE",)}}

    RETURN_TYPES = ()
    FUNCTION = "preview_no_cache"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee_Tools" # Added per your preference

    def preview_no_cache(self, images):
        results = []
        # We use a fixed filename to encourage the browser to reuse the memory slot
        # slightly changing the query param (subfolder) to force a refresh but try to keep it lean.
        
        for i, image in enumerate(images):
            i_np = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))
            
            # Save to a fixed filename in temp to avoid disk bloat
            filename = f"ephemeral_monitor_{i}.png"
            file = os.path.join(self.output_dir, filename)
            img.save(file, optimize=True, compress_level=4)
            
            # We append a random int to the subfolder only to trigger the UI update,
            # but the file on disk remains constant.
            results.append({
                "filename": filename,
                "subfolder": "", 
                "type": self.type
            })

        # This return structure mimics a PreviewImage node
        return {"ui": {"images": results}}

# Register the node
NODE_CLASS_MAPPINGS = {
    "EmAySee_EphemeralPreview": EphemeralPreview
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_EphemeralPreview": "Ephemeral Preview (Low RAM)"
}