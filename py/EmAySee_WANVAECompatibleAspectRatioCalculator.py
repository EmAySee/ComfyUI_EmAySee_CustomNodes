import torch

class EmAySee_VAECompatibleAspectRatioCalculator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "output_height": ("INT", {
                    "default": 512,
                    "min": 1,
                    "step": 64,
                    "values": [512, 576, 640, 704, 768, 832, 896, 960, 1024]
                }),
            }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("output_width", "output_height",)
    CATEGORY = "EmAySee/Utils"
    FUNCTION = "EmAySee_calculate_dimensions"

    def EmAySee_calculate_dimensions(self, image, output_height):
        # We'll use the first image in the batch to determine dimensions.
        batch_size, original_height, original_width, channels = image.shape
        
        # Calculate the ideal width based on the original aspect ratio.
        ratio = original_width / original_height
        
        # Calculate the new width based on the desired height and aspect ratio.
        # This new width must be a multiple of 64 to be VAE-compatible.
        vae_stride = 64
        calculated_width = output_height * ratio
        
        # Round the width to the nearest multiple of the VAE stride.
        output_width = int(round(calculated_width / vae_stride) * vae_stride)
        
        return (output_width, output_height,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_VAECompatibleAspectRatioCalculator": EmAySee_VAECompatibleAspectRatioCalculator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_VAECompatibleAspectRatioCalculator": "EmAySee VAE-Compatible Aspect Ratio Calculator"
}
