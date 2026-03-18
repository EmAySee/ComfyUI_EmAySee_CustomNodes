import torch

class EmAySee_CalculateAspectRatio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "output_height": ("INT", {"default": 512, "min": 1, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("output_width", "output_height",)
    CATEGORY = "EmAySee/Utils"
    FUNCTION = "EmAySee_calculate_dimensions"

    def EmAySee_calculate_dimensions(self, image, output_height):
        batch_size, original_height, original_width, channels = image.shape
        
        # Calculate the new width based on the aspect ratio
        ratio = original_width / original_height
        output_width = int(output_height * ratio)
        
        return (output_width, output_height,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_CalculateAspectRatio": EmAySee_CalculateAspectRatio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_CalculateAspectRatio": "EmAySee Aspect Ratio Calculator"
}


