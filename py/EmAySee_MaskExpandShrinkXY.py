import torch
import torch.nn.functional as F

class EmAySee_MaskExpandShrinkXY:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "expand_x": ("INT", {"default": 0, "min": -1024, "max": 1024, "step": 1}),
                "expand_y": ("INT", {"default": 0, "min": -1024, "max": 1024, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "modify_mask"
    CATEGORY = "EmAySee/Mask"

    def modify_mask(self, mask, expand_x, expand_y):
        if expand_x == 0 and expand_y == 0:
            return (mask,)

        if mask.dim() == 2:
            mask = mask.unsqueeze(0)

        m = mask.unsqueeze(1)

        if expand_x > 0:
            kernel_x = expand_x * 2 + 1
            m = F.max_pool2d(m, kernel_size=(1, kernel_x), stride=(1, 1), padding=(0, expand_x))
        elif expand_x < 0:
            shrink_x = abs(expand_x)
            kernel_x = shrink_x * 2 + 1
            m = 1.0 - F.max_pool2d(1.0 - m, kernel_size=(1, kernel_x), stride=(1, 1), padding=(0, shrink_x))

        if expand_y > 0:
            kernel_y = expand_y * 2 + 1
            m = F.max_pool2d(m, kernel_size=(kernel_y, 1), stride=(1, 1), padding=(expand_y, 0))
        elif expand_y < 0:
            shrink_y = abs(expand_y)
            kernel_y = shrink_y * 2 + 1
            m = 1.0 - F.max_pool2d(1.0 - m, kernel_size=(kernel_y, 1), stride=(1, 1), padding=(shrink_y, 0))

        m = m.squeeze(1)

        return (m,)

class EmAySee_MaskCenterHoleXY:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "hole_width": ("INT", {"default": 25, "min": 0, "max": 8192, "step": 1}),
                "hole_height": ("INT", {"default": 150, "min": 0, "max": 8192, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "punch_hole"
    CATEGORY = "EmAySee/Mask"

    def punch_hole(self, mask, hole_width, hole_height):
        if hole_width <= 0 and hole_height <= 0:
            return (mask,)

        if mask.dim() == 2:
            mask = mask.unsqueeze(0)

        res_mask = mask.clone()
        B, H, W = res_mask.shape

        for b in range(B):
            m = res_mask[b]
            y_idx, x_idx = torch.where(m > 0.5)
            
            if len(y_idx) == 0:
                continue

            min_y, max_y = y_idx.min().item(), y_idx.max().item()
            min_x, max_x = x_idx.min().item(), x_idx.max().item()

            cy = (min_y + max_y) // 2
            cx = (min_x + max_x) // 2

            x1 = max(0, cx - hole_width // 2)
            x2 = min(W, x1 + hole_width)
            
            y1 = max(0, cy - hole_height // 2)
            y2 = min(H, y1 + hole_height)

            res_mask[b, y1:y2, x1:x2] = 0.0

        return (res_mask,)

class EmAySee_MaskUniversalXY:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "expand_x": ("INT", {"default": 0, "min": -1024, "max": 1024, "step": 1}),
                "expand_y": ("INT", {"default": 0, "min": -1024, "max": 1024, "step": 1}),
                "hole_width": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 1}),
                "hole_height": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "process"
    CATEGORY = "EmAySee/Mask"

    def process(self, mask, expand_x, expand_y, hole_width, hole_height):
        if mask.dim() == 2:
            mask = mask.unsqueeze(0)
        
        m = mask.unsqueeze(1)
        
        if expand_x > 0:
            k = expand_x * 2 + 1
            m = F.max_pool2d(m, kernel_size=(1, k), stride=(1, 1), padding=(0, expand_x))
        elif expand_x < 0:
            s = abs(expand_x)
            k = s * 2 + 1
            m = 1.0 - F.max_pool2d(1.0 - m, kernel_size=(1, k), stride=(1, 1), padding=(0, s))

        if expand_y > 0:
            k = expand_y * 2 + 1
            m = F.max_pool2d(m, kernel_size=(k, 1), stride=(1, 1), padding=(expand_y, 0))
        elif expand_y < 0:
            s = abs(expand_y)
            k = s * 2 + 1
            m = 1.0 - F.max_pool2d(1.0 - m, kernel_size=(k, 1), stride=(1, 1), padding=(s, 0))
            
        res_mask = m.squeeze(1).clone()
        
        if hole_width <= 0 and hole_height <= 0:
            return (res_mask,)

        B, H, W = res_mask.shape

        for b in range(B):
            single_m = res_mask[b]
            y_idx, x_idx = torch.where(single_m > 0.5)
            
            if len(y_idx) == 0:
                continue

            min_y, max_y = y_idx.min().item(), y_idx.max().item()
            min_x, max_x = x_idx.min().item(), x_idx.max().item()

            cy = (min_y + max_y) // 2
            cx = (min_x + max_x) // 2

            x1 = max(0, cx - hole_width // 2)
            x2 = min(W, x1 + hole_width)
            
            y1 = max(0, cy - hole_height // 2)
            y2 = min(H, y1 + hole_height)

            res_mask[b, y1:y2, x1:x2] = 0.0

        return (res_mask,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MaskExpandShrinkXY": EmAySee_MaskExpandShrinkXY,
    "EmAySee_MaskCenterHoleXY": EmAySee_MaskCenterHoleXY,
    "EmAySee_MaskUniversalXY": EmAySee_MaskUniversalXY
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MaskExpandShrinkXY": "EmAySee Mask Expand Shrink XY",
    "EmAySee_MaskCenterHoleXY": "EmAySee Mask Center Hole XY",
    "EmAySee_MaskUniversalXY": "EmAySee Mask Universal XY"
}