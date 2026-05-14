import torch
import torch.nn.functional as F
import math

class EmAySee_QwenResolutionOptimizer_V2NS:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_megapixels": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 16.0, "step": 0.1}),
                "min_megapixels": ("FLOAT", {"default": 0.1, "min": 0.05, "max": 1.0, "step": 0.05}),
                "max_megapixels": ("FLOAT", {"default": 1.5, "min": 0.5, "max": 32.0, "step": 0.1}),
                "multiple_of": ("INT", {"default": 112, "min": 1, "max": 512, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT", "FLOAT", "FLOAT", "STRING")
    RETURN_NAMES = ("IMAGE", "width", "height", "total_pixels", "actual_mp", "recommended_mp", "resolution_text")
    FUNCTION = "optimize"
    CATEGORY = "EmAySee/Image"

    def optimize(self, image, target_megapixels, min_megapixels, max_megapixels, multiple_of):
        batch, h_orig, w_orig, channels = image.shape
        aspect_ratio = w_orig / h_orig
        
        target_pixels = target_megapixels * 1000000
        min_pixels = min_megapixels * 1000000
        max_pixels = max_megapixels * 1000000
        
        clamped_target = max(min_pixels, min(max_pixels, target_pixels))
        
        opt_h = math.sqrt(clamped_target / aspect_ratio)
        opt_w = opt_h * aspect_ratio
        
        width = int(round(opt_w / multiple_of) * multiple_of)
        height = int(round(opt_h / multiple_of) * multiple_of)
        
        width = max(multiple_of, width)
        height = max(multiple_of, height)
        
        current_pixels = width * height
        if current_pixels > max_pixels:
            if width > height:
                width = int(math.floor(width / multiple_of) * multiple_of)
                if width * height > max_pixels:
                     height = int(math.floor(height / multiple_of) * multiple_of)
            else:
                height = int(math.floor(height / multiple_of) * multiple_of)
                if width * height > max_pixels:
                    width = int(math.floor(width / multiple_of) * multiple_of)

        target_ar = width / height
        
        if aspect_ratio > target_ar:
            crop_w = int(h_orig * target_ar)
            crop_h = h_orig
            start_x = (w_orig - crop_w) // 2
            start_y = 0
        else:
            crop_w = w_orig
            crop_h = int(w_orig / target_ar)
            start_x = 0
            start_y = (h_orig - crop_h) // 2
            
        cropped_image = image[:, start_y:start_y+crop_h, start_x:start_x+crop_w, :]
        
        img_permuted = cropped_image.permute(0, 3, 1, 2)
        resized_img = F.interpolate(img_permuted, size=(height, width), mode="bicubic", align_corners=False)
        final_image = resized_img.permute(0, 2, 3, 1)

        actual_pixels = width * height
        actual_mp = actual_pixels / 1000000.0
        rec_mp = clamped_target / 1000000.0
        res_text = f"{width}x{height}"
        
        return (final_image, width, height, actual_pixels, actual_mp, rec_mp, res_text)

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenResolutionOptimizer_V2NS": EmAySee_QwenResolutionOptimizer_V2NS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenResolutionOptimizer_V2NS": "EmAySee Qwen Resolution Optimizer V2NS"
}