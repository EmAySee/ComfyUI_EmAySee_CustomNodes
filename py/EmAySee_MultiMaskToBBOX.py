import torch

class EmAySee_MultiMaskToBBOX:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask_1": ("MASK",),
            },
            "optional": {
                "mask_2": ("MASK",),
                "mask_3": ("MASK",),
                "mask_4": ("MASK",),
                "mask_5": ("MASK",),
                "mask_6": ("MASK",),
                "mask_7": ("MASK",),
                "mask_8": ("MASK",),
                "mask_9": ("MASK",),
                "mask_10": ("MASK",),
            }
        }

    RETURN_TYPES = ("BBOX", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("bbox", "x", "y", "width", "height")
    FUNCTION = "extract_bbox"
    CATEGORY = "EmAySee/Masking"

    def extract_bbox(self, mask_1, **kwargs):
        masks = [mask_1]
        for i in range(2, 11):
            m = kwargs.get(f"mask_{i}")
            if m is not None:
                masks.append(m)
        
        all_nonzero = []
        for mask in masks:
            if mask.dim() == 2:
                mask = mask.unsqueeze(0)
            
            nonzero = torch.nonzero(mask)
            if nonzero.size(0) > 0:
                all_nonzero.append(nonzero)
        
        if not all_nonzero:
            return ([0, 0, 0, 0], 0, 0, 0, 0)
            
        combined_nonzero = torch.cat(all_nonzero, dim=0)
        
        y_min = torch.min(combined_nonzero[:, 1]).item()
        y_max = torch.max(combined_nonzero[:, 1]).item()
        x_min = torch.min(combined_nonzero[:, 2]).item()
        x_max = torch.max(combined_nonzero[:, 2]).item()
        
        width = (x_max - x_min) + 1
        height = (y_max - y_min) + 1
        
        return ([x_min, y_min, width, height], int(x_min), int(y_min), int(width), int(height))

NODE_CLASS_MAPPINGS = {
    "EmAySee_MultiMaskToBBOX": EmAySee_MultiMaskToBBOX
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MultiMaskToBBOX": "EmAySee_Multi Mask to BBOX"
}