import torch
import torch.nn.functional as F

class EmAySee_MaskExpandXY:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "expand_x": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 1}),
                "expand_y": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "expand_mask"
    CATEGORY = "EmAySee/Mask"

    def expand_mask(self, mask, expand_x, expand_y):
        if expand_x == 0 and expand_y == 0:
            return (mask,)

        if mask.dim() == 2:
            mask = mask.unsqueeze(0)

        m = mask.unsqueeze(1)

        kernel_y = expand_y * 2 + 1
        kernel_x = expand_x * 2 + 1

        m = F.max_pool2d(m, kernel_size=(kernel_y, kernel_x), stride=(1, 1), padding=(expand_y, expand_x))

        m = m.squeeze(1)

        return (m,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MaskExpandXY": EmAySee_MaskExpandXY
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MaskExpandXY": "EmAySee Mask Expand XY"
}