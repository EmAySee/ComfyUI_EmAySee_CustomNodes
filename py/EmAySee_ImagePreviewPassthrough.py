import folder_paths
import numpy as np
from PIL import Image
import os
import time

class EmAySee_ImagePreviewPassthrough:
    def __init__(self):
        #  Get the temp directory from ComfyUI
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "preview_and_passthrough"
    CATEGORY = "EmAySee/Utils"

    def preview_and_passthrough(self, image):
        #  1. --- Prepare images for preview ---
        #  This logic is adapted from ComfyUI's PreviewImage node
        
        #  Convert tensor to PIL images
        images = []
        for i in range(image.shape[0]):
            img_tensor = image[i]
            img = (img_tensor * 255.0).cpu().numpy().astype(np.uint8)
            images.append(Image.fromarray(img))
        
        #  Save images to temp folder and get filenames
        preview_images = []
        for img in images:
            #  Generate a unique filename based on current time
            filename = f"emaysee_preview_{time.time_ns()}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            #  Save the image
            img.save(filepath, format='PNG', compress_level=4) #  Use low compression for speed
            
            #  Add to preview list for the UI
            preview_images.append({
                "filename": filename,
                "subfolder": "", #  We are using the temp folder directly
                "type": self.type
            })

        #  2. --- Return results ---
        #  This dictionary structure tells ComfyUI what to display in the UI
        #  and what to pass to the output port.
        return {
            "ui": { "images": preview_images }, #  This triggers the inline preview
            "result": (image,)                 #  This is the passthrough output
        }

NODE_CLASS_MAPPINGS = {
    "EmAySee_ImagePreviewPassthrough": EmAySee_ImagePreviewPassthrough
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ImagePreviewPassthrough": "EmAySee Image Preview Passthrough"
}
