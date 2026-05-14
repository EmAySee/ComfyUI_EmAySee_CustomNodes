import torch

class EmAySee_MaskGuard:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "EmAySee_Nodes"

    def execute(self, mask, width, height):
        if mask is None or mask.numel() == 0:
            return (torch.zeros((1, height, width, 3), dtype=torch.float32),)

        if mask.dim() == 2:
            mask = mask.unsqueeze(0)
        
        try:
            target_mask = mask[0]
            image = target_mask.reshape((-1, 1, target_mask.shape[-2], target_mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
            return (image,)
        except Exception:
            return (torch.zeros((1, height, width, 3), dtype=torch.float32),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MaskGuard": EmAySee_MaskGuard
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MaskGuard": "EmAySee_ Mask Guard to Image"
}