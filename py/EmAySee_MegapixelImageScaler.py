import torch
import torch.nn.functional as F

class EmAySee_MegapixelImageScaler:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_megapixels": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 64.0, "step": 0.1}),
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 64}),
                "method": (["nearest-exact", "bilinear", "area", "bicubic", "lanczos"], {"default": "bicubic"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "FLOAT")
    RETURN_NAMES = ("IMAGE", "width", "height", "actual_mp")
    FUNCTION = "resize_to_mp"
    CATEGORY = "EmAySee/Image"

    def resize_to_mp(self, image, target_megapixels, multiple_of, method):
        _, old_h, old_w, _ = image.shape
        
        aspect_ratio = old_w / old_h
        target_pixels = target_megapixels * 1_000_000
        
        new_h = (target_pixels / aspect_ratio)**0.5
        new_w = new_h * aspect_ratio
        
        final_w = int(round(new_w / multiple_of) * multiple_of)
        final_h = int(round(new_h / multiple_of) * multiple_of)
        
        img = image.permute(0, 3, 1, 2)
        
        if method == "lanczos":
            rescaled_image = F.interpolate(img, size=(final_h, final_w), mode="bicubic", align_corners=False)
        else:
            rescaled_image = F.interpolate(img, size=(final_h, final_w), mode=method, align_corners=False if method != "nearest-exact" else None)
        
        rescaled_image = rescaled_image.permute(0, 2, 3, 1)
        actual_mp = (final_w * final_h) / 1_000_000
        
        return (rescaled_image, final_w, final_h, actual_mp)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MegapixelImageScaler": EmAySee_MegapixelImageScaler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MegapixelImageScaler": "EmAySee Megapixel Image Resizer"
}