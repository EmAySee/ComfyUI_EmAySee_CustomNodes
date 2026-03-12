import torch
import torch.nn.functional as F

class EmAySee_MaskUnion:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {},
            "optional": {}
        }
        for i in range(1, 15):
            inputs["optional"][f"mask_{i}"] = ("MASK",)
        return inputs

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "combine"
    CATEGORY = "EmAySee/Mask"

    def combine(self, **kwargs):
        masks = [v for k, v in kwargs.items() if v is not None]
        
        if not masks:
            return (torch.zeros((1, 64, 64), dtype=torch.float32),)

        target_h = max(m.shape[-2] for m in masks)
        target_w = max(m.shape[-1] for m in masks)
        
        res = torch.zeros((1, target_h, target_w), dtype=torch.float32)

        for m in masks:
            if m.dim() == 2:
                m = m.unsqueeze(0)
            
            if m.shape[-2] != target_h or m.shape[-1] != target_w:
                m_temp = m.unsqueeze(0) if m.dim() == 3 else m
                m = F.interpolate(m_temp, size=(target_h, target_w), mode="bilinear").squeeze(0)
            
            res = torch.max(res, m)
            
        return (res,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MaskUnion": EmAySee_MaskUnion
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MaskUnion": "EmAySee Mask Union"
}