import torch
import torch.nn.functional as F
import math

class EmAySee_ImageGetSize:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_size"
    CATEGORY = "EmAySee"

    def get_size(self, image):
        _, height, width, _ = image.shape
        return (width, height)

class EmAySee_MathExpression:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "expression": ("STRING", {"multiline": True, "default": "max(w, h)"}),
                "w": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 1}),
                "h": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "evaluate"
    CATEGORY = "EmAySee"


    def evaluate(self, expression, w, h):
        safe_env = {
            'w': w,
            'h': h,
            'max': max,
            'min': min,
            'abs': abs,
            'pow': pow,
            'round': round,
            'math': math
        }
        result = 0
        try:
            result = eval(expression, {"__builtins__": {}}, safe_env)
        except Exception as e:
            print(f"EmAySee_MathExpression Error: {e}")
        return (int(result),)

class EmAySee_PadImageForOutpainting:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
                "top": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
                "right": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
                "bottom": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "pad"
    CATEGORY = "EmAySee"

    def pad(self, image, left, top, right, bottom):
        B, H, W, C = image.shape
        image_padded = image.permute(0, 3, 1, 2)
        image_padded = F.pad(image_padded, (left, right, top, bottom), "constant", 0)
        image_padded = image_padded.permute(0, 2, 3, 1)

        new_H, new_W = image_padded.shape[1], image_padded.shape[2]
        mask = torch.ones((new_H, new_W), dtype=torch.float32, device=image.device)
        mask[top:top+H, left:left+W] = 0

        return (image_padded, mask.unsqueeze(0))

NODE_CLASS_MAPPINGS = {
    "EmAySee_ImageGetSize": EmAySee_ImageGetSize,
    "EmAySee_MathExpression": EmAySee_MathExpression,
    "EmAySee_PadImageForOutpainting": EmAySee_PadImageForOutpainting,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ImageGetSize": "Image Get Size (EmAySee)",
    "EmAySee_MathExpression": "Math Expression (EmAySee)",
    "EmAySee_PadImageForOutpainting": "Pad Image For Outpainting (EmAySee)",
}
