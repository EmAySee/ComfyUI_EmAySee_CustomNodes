import torch
import torch.nn.functional as F

class EmAySee_ConditionalResize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "trigger_threshold": ("INT", {"default": 1024, "min": 0, "max": 16384, "step": 8}),
                "target_resolution": ("INT", {"default": 1024, "min": 0, "max": 16384, "step": 8}),
                "method": (["nearest-exact", "bilinear", "area", "bicubic", "lanczos"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "resize_if_needed"
    CATEGORY = "EmAySee/Image"

    def resize_if_needed(self, image, trigger_threshold, target_resolution, method):
        _, h, w, _ = image.shape
        longest_side = max(h, w)

        if longest_side >= trigger_threshold:
            return (image,)

        scale = target_resolution / longest_side
        new_h = int(h * scale)
        new_w = int(w * scale)

        samples = image.movedim(-1, 1)
        
        if method == "lanczos":
             s = samples.clone()
             # Lanczos kernel implementation usually requires custom handling or specific libraries in standard Torch.
             # Using bicubic as a fallback for standard torch interpolate if lanczos isn't explicitly defined in context,
             # but standard ComfyUI `common_upscale` handles this. 
             # To keep this dependency-free and simple torch:
             # We will use bicubic for lanczos slot here or implement standard resize.
             # Actually, simpler to map standard torch modes. 
             # Let's use bicubic for 'lanczos' to avoid external dependencies, 
             # or simple bicubic with antialias=True if supported.
             mode = "bicubic"
        else:
            mode = method

        if method == "nearest-exact":
            mode = "nearest"

        s = F.interpolate(samples, size=(new_h, new_w), mode=mode, align_corners=False if mode not in ["nearest", "area"] else None)
        s = s.movedim(1, -1)
        
        return (s,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_ConditionalResize": EmAySee_ConditionalResize
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ConditionalResize": "EmAySee Conditional Resize"
}