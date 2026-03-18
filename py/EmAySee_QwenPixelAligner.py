import torch
import torch.nn.functional as F

class EmAySee_QwenPixelAligner:
    @classmethod
    def INPUT_TYPES(s):
        # Generate the list of resolutions from 784 to 2240 in steps of 112
        resolutions = [str(x) for x in range(784, 2241, 112)]
        
        return {
            "required": {
                "image": ("IMAGE",),
                "longest_edge": (resolutions, {"default": "1232"}),
                "alignment": (["112", "56", "224"], {"default": "112"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "STRING")
    RETURN_NAMES = ("IMAGE", "width", "height", "resolution_text")
    FUNCTION = "align_and_resize"
    CATEGORY = "EmAySee/Image"

    def align_and_resize(self, image, longest_edge, alignment):
        align_val = int(alignment)
        target_edge = int(longest_edge)
        B, H, W, C = image.shape
        
        # Calculate aspect ratio and new dimensions
        current_longest = max(H, W)
        
        # Scale factor to match the longest edge target
        scale_factor = target_edge / current_longest
        
        target_h = H * scale_factor
        target_w = W * scale_factor
        
        # Snap dimensions to the nearest alignment multiple
        new_height = int(round(target_h / align_val) * align_val)
        new_width = int(round(target_w / align_val) * align_val)
        
        # Ensure dimensions are at least one alignment block
        new_height = max(align_val, new_height)
        new_width = max(align_val, new_width)
        
        # Permute image to [B, C, H, W] for interpolation
        img_permuted = image.permute(0, 3, 1, 2)
        
        # Resize using bicubic interpolation
        resized_img = F.interpolate(img_permuted, size=(new_height, new_width), mode="bicubic", align_corners=False)
        
        # Permute back to [B, H, W, C]
        final_image = resized_img.permute(0, 2, 3, 1)
        
        # Create resolution string
        res_text = f"{new_width}x{new_height}"
        
        return (final_image, new_width, new_height, res_text)

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenPixelAligner": EmAySee_QwenPixelAligner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenPixelAligner": "EmAySee Qwen Pixel Aligner"
}