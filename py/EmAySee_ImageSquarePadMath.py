import torch

class EmAySee_ImageSquarePadMath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("left", "top", "right", "bottom", "width", "height")
    FUNCTION = "calculate_padding"
    CATEGORY = "Image/Padding"

    def calculate_padding(self, image):
        # image tensor is [B, H, W, C]
        _, h, w, _ = image.shape
        
        left = 0
        top = 0
        right = 0
        bottom = 0
        
        if w > h:
            # Landscape: Pad top and bottom
            diff = w - h
            top = diff // 2
            bottom = diff - top  # Handles odd numbers
        elif h > w:
            # Portrait: Pad left and right
            diff = h - w
            left = diff // 2
            right = diff - left # Handles odd numbers
            
        return (left, top, right, bottom, w, h)

NODE_CLASS_MAPPINGS = {
    "EmAySee_ImageSquarePadMath": EmAySee_ImageSquarePadMath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ImageSquarePadMath": "Image Square Padding Math"
}