import torch
import random
import nodes

class EmAySee_RandomOrientationLatent:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 8}),
                "height": ("INT", {"default": 768, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 8}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                "random_orientation": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("LATENT", "INT", "INT")
    RETURN_NAMES = ("latent", "width", "height")
    FUNCTION = "generate"
    CATEGORY = "EmAySee/Latent"

    def generate(self, width, height, batch_size, random_orientation, seed):
        final_w = width
        final_h = height
        
        if random_orientation:
            rng = random.Random(seed)
            if rng.randint(0, 1) == 1:
                final_w = height
                final_h = width
        
        latent = torch.zeros([batch_size, 4, final_h // 8, final_w // 8])
        
        return ({"samples": latent}, final_w, final_h)

NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomOrientationLatent": EmAySee_RandomOrientationLatent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomOrientationLatent": "EmAySee Random Orientation Latent"
}