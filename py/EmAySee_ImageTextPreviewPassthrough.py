import os
import numpy as np
from PIL import Image
import folder_paths
import random
import string

class EmAySee_ImageTextPreviewPassthrough:
    def __init__(self):
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"forceInput": True, "multiline": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "text")
    FUNCTION = "preview"
    OUTPUT_NODE = True
    CATEGORY = "EmAySee/Utils"

    def preview(self, image, text):
        output_dir = folder_paths.get_temp_directory()
        filename_prefix = "EmAySee_Preview" + self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, output_dir, image[0].shape[1], image[0].shape[0])

        results = list()
        for img_tensor in image:
            i = 255. * img_tensor.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), compress_level=4)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return {"ui": {"images": results, "text": [text]}, "result": (image, text)}

NODE_CLASS_MAPPINGS = {
    "EmAySee_ImageTextPreviewPassthrough": EmAySee_ImageTextPreviewPassthrough
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ImageTextPreviewPassthrough": "EmAySee Image Text Preview Passthrough"
}