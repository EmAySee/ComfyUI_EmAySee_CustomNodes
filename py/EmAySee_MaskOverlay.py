import torch
import torch.nn.functional as F

class EmAySee_MaskOverlay:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "opacity": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_overlay"
    CATEGORY = "EmAySee/Image"

    def apply_overlay(self, image, mask, opacity):
        b, h, w, c = image.shape
        
        if mask.dim() == 2:
            mask = mask.unsqueeze(0)
            
        mask_b, mask_h, mask_w = mask.shape
        
        if mask_h != h or mask_w != w:
            mask = mask.unsqueeze(1)
            mask = F.interpolate(mask, size=(h, w), mode="bilinear", align_corners=False)
            mask = mask.squeeze(1)
            
        if mask_b != b:
            if mask_b == 1:
                mask = mask.repeat(b, 1, 1)
            elif b == 1:
                image = image.repeat(mask_b, 1, 1, 1)
            else:
                min_b = min(b, mask_b)
                image = image[:min_b]
                mask = mask[:min_b]

        alpha = (mask * opacity).unsqueeze(-1)
        
        red_color = torch.zeros_like(image)
        red_color[..., 0] = 1.0
        
        if c == 4:
            alpha_adjusted = alpha.clone()
            alpha_adjusted[..., 3] = 0.0
            result = image * (1.0 - alpha_adjusted) + red_color * alpha_adjusted
        else:
            result = image * (1.0 - alpha) + red_color * alpha
            
        return (result,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MaskOverlay": EmAySee_MaskOverlay
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MaskOverlay": "EmAySee Mask Overlay"
}