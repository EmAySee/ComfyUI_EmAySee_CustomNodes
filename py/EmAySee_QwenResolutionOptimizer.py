import torch
import torch.nn.functional as F

class EmAySee_QwenResolutionOptimizer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "scale_multiplier": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 4.0, "step": 0.1}),
                "method": (["crop", "stretch"], {"default": "crop"}),
                "upscale_method": (["bicubic", "nearest-exact", "bilinear", "area"], {"default": "bicubic"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "STRING")
    RETURN_NAMES = ("IMAGE", "width", "height", "aspect_ratio_name")
    FUNCTION = "optimize"
    CATEGORY = "EmAySee_Nodes/Image/Alignment"

    def optimize(self, image, scale_multiplier, method, upscale_method):
        B, H, W, C = image.shape
        input_aspect = W / H
        
        targets = [
            (1.0, 1008, 1008, "1:1 Square"),
            (1.25, 1120, 896, "4:3 Landscape"),
            (1.375, 1232, 896, "3:2 Classic"),
            (1.714, 1344, 784, "16:9 Widescreen"),
            (0.8, 896, 1120, "3:4 Portrait"),
            (0.727, 896, 1232, "2:3 Classic Portrait"),
            (0.583, 784, 1344, "9:16 Vertical")
        ]
        
        best_match = min(targets, key=lambda x: abs(x[0] - input_aspect))
        base_w, base_h, ratio_name = best_match[1], best_match[2], best_match[3]

        target_w = int(round((base_w * scale_multiplier) / 112) * 112)
        target_h = int(round((base_h * scale_multiplier) / 112) * 112)
        
        if target_w == 0: target_w = 112
        if target_h == 0: target_h = 112

        samples = image.movedim(-1, 1)

        if method == "crop":
            target_aspect = base_w / base_h
            if input_aspect > target_aspect:
                new_w = int(H * target_aspect)
                offset = (W - new_w) // 2
                samples = samples[:, :, :, offset:offset + new_w]
            else:
                new_h = int(W / target_aspect)
                offset = (H - new_h) // 2
                samples = samples[:, :, offset:offset + new_h, :]
        
        samples = F.interpolate(samples, size=(target_h, target_w), mode=upscale_method)
        samples = samples.movedim(1, -1)
        
        final_info = f"{ratio_name} @ {scale_multiplier}x ({target_w}x{target_h})"
        
        return (samples, target_w, target_h, final_info)

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenResolutionOptimizer": EmAySee_QwenResolutionOptimizer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenResolutionOptimizer": "EmAySee_ Qwen Resolution Optimizer"
}