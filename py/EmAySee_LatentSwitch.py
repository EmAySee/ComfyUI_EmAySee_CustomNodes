import torch

class EmAySee_LatentSwitch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "top_latent": ("LATENT",),
            },
            "optional": {
                "bottom_latent": ("LATENT",)
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("selected_latent",)
    CATEGORY = "EmAySee/Utils"
    FUNCTION = "EmAySee_select_latent"

    def EmAySee_select_latent(self, top_latent, bottom_latent=None):
        if bottom_latent is not None:
            return (bottom_latent,)
        else:
            return (top_latent,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LatentSwitch": EmAySee_LatentSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LatentSwitch": "EmAySee Latent Switch"
}
