import torch
import torch.nn.functional as F

class EmAySee_QwenRatioLock:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "resize_absolute"
    CATEGORY = "EmAySee"

    def resize_absolute(self, image):
        _, oh, ow, _ = image.shape
        
        if ow >= oh:
            new_w = ow
            new_h = int(ow * (2904 / 4000))
        else:
            new_h = oh
            new_w = int(oh * (2904 / 4000))
            
        if oh == new_h and ow == new_w:
            return (image,)
            
        samples = image.permute(0, 3, 1, 2)
        out = F.interpolate(samples, size=(new_h, new_w), mode="bilinear", align_corners=False)
        result = out.permute(0, 2, 3, 1)

        return (result,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_QwenRatioLock": EmAySee_QwenRatioLock
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_QwenRatioLock": "EmAySee_ Qwen Ratio Lock"
}