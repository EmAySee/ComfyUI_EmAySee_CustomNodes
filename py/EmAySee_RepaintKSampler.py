from comfy.samplers import KSampler as ComfyUISampler
import torch

class EmAySee_RepaintKSampler:
    """
    A KSampler node designed for repainting using an image mask.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "mask": ("MASK",),
                "sampler_name": (ComfyUISampler.SAMPLERS, {"default": "euler_ancestral"}),
                "scheduler": (ComfyUISampler.SCHEDULERS, {"default": "normal"}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 1000.0}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0}),
            },
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    TITLE = "EmAySee Repaint KSampler"
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "EmAySee_function"

    def EmAySee_function(self, model, positive, negative, latent_image, mask, sampler_name, scheduler, steps, cfg, denoise):
        # Invert the mask because in ComfyUI, white usually means "keep" and black means "change" for inpainting
        inverted_mask = 1.0 - mask.unsqueeze(1)

        # Apply the mask to the latent image
        masked_latent = latent_image["samples"] * inverted_mask

        # Create an empty latent image for the masked area (this will be filled by the sampler)
        initial_noise = torch.randn_like(latent_image["samples"]) * denoise

        # Combine the masked original and the initial noise for the masked area
        # Where the mask is white (1.0), we take the noise; where it's black (0.0), we take the original latent
        combined_latent = masked_latent + initial_noise * mask.unsqueeze(1)

        # Perform the K-sampling with the combined latent as the starting point
        sampler = ComfyUISampler(model)
        samples = sampler.sample(noise=combined_latent,
                                 positive=positive,
                                 negative=negative,
                                 cfg=cfg,
                                 steps=steps,
                                 sampler_name=sampler_name,
                                 scheduler=scheduler,
                                 denoise=denoise)

        return ({"samples": samples},)

NODE_CLASS_MAPPINGS = {
    "EmAySee_RepaintKSampler": EmAySee_RepaintKSampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RepaintKSampler": "EmAySee Repaint KSampler"
}