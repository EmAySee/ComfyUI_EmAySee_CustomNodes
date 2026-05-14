import torch
import torch.nn.functional as F

class EmAySee_MaskSkinnier:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "shrink_percentage": ("FLOAT", {"default": 33.0, "min": 0.0, "max": 100.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "shrink_mask_content"
    CATEGORY = "EmAySee_/Mask"

    def shrink_mask_content(self, mask, shrink_percentage):
        if len(mask.shape) == 2:
            mask = mask.unsqueeze(0)
        
        B, H, W = mask.shape
        out_masks = []
        strength = shrink_percentage / 100.0

        for i in range(B):
            m = mask[i]
            coords = torch.nonzero(m > 0.0)
            
            if coords.shape[0] == 0:
                out_masks.append(m)
                continue

            y_min, x_min = coords.min(dim=0).values
            y_max, x_max = coords.max(dim=0).values
            
            mh = (y_max - y_min + 1).item()
            mw = (x_max - x_min + 1).item()
            
            mask_content = m[y_min:y_max+1, x_min:x_max+1].unsqueeze(0).unsqueeze(0)
            
            new_mask = torch.zeros((H, W), device=mask.device)
            
            if mw > mh:
                new_mh = max(1, int(mh * (1.0 - strength)))
                shrunk_content = F.interpolate(mask_content, size=(new_mh, mw), mode='bilinear', align_corners=False).squeeze()
                y_offset = y_min + (mh - new_mh) // 2
                new_mask[y_offset:y_offset+new_mh, x_min:x_max+1] = shrunk_content
            else:
                new_mw = max(1, int(mw * (1.0 - strength)))
                shrunk_content = F.interpolate(mask_content, size=(mh, new_mw), mode='bilinear', align_corners=False).squeeze()
                x_offset = x_min + (mw - new_mw) // 2
                new_mask[y_min:y_max+1, x_offset:x_offset+new_mw] = shrunk_content
                
            out_masks.append(new_mask)

        return (torch.stack(out_masks),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MaskSkinnier": EmAySee_MaskSkinnier
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MaskSkinnier": "EmAySee_ Mask Skinnier"
}