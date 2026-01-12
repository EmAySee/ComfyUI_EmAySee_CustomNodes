import torch

class EmAySee_QwenPixelAligner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "alignment": (["112", "56", "224"], {"default": "112"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("IMAGE", "width", "height")
    FUNCTION = "align_and_crop"
    CATEGORY = "EmAySee_Nodes/Image/Alignment"

    def align_and_crop(self, image, alignment):
        align_val = int(alignment)
        B, H, W, C = image.shape
        
        new_width = (W // align_val) * align_val
        new_height = (H // align_val) * align_val
        
        width_offset = (W - new_width) // 2
        height_offset = (H - new_height) // 2
        
        cropped_image = image[:, height_offset:height_offset + new_height, width_offset:width_offset + new_width, :]
        
        return (cropped_image, new_width, new_height)

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenPixelAligner": EmAySee_QwenPixelAligner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenPixelAligner": "EmAySee_ Qwen Pixel Aligner"
}