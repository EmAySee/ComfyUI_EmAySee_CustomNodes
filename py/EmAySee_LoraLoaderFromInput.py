import folder_paths
import comfy.sd
import torch

class EmAySee_LoraLoaderFromInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                # This input will connect to the output of the EmAySee Lora Name Selector
                "lora_filename": ("LORA",), 
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP",)
    CATEGORY = "EmAySee/Loaders"
    FUNCTION = "EmAySee_load_lora"

    def EmAySee_load_lora(self, model, clip, lora_filename, strength_model, strength_clip):
        
        # 1. Find the full path of the Lora file using the filename from input
        lora_path = folder_paths.get_full_path("loras", lora_filename)
        
        # 2. Check if the file exists before proceeding
        if lora_path is None:
            # We print an error but return the original model/clip to prevent the workflow from crashing
            print(f"[EmAySee_LoraLoaderFromInput] Lora file not found: {lora_filename}. Skipping Lora application.")
            return (model, clip) 

        # 3. Load and apply the Lora using ComfyUI's standard utility function
        model_lora, clip_lora = comfy.sd.load_lora(model, clip, lora_path, strength_model, strength_clip)
        
        return (model_lora, clip_lora)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LoraLoaderFromInput": EmAySee_LoraLoaderFromInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoraLoaderFromInput": "EmAySee Lora Loader From Input"
}