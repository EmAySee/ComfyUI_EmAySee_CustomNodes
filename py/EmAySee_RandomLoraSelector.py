import random
import folder_paths
import comfy.utils
import comfy.sd

class EmAySee_RandomLoraLoader:
    @classmethod
    def INPUT_TYPES(s):
        lora_list = ["None"] + folder_paths.get_filename_list("loras")
        
        inputs = {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
        
        # Dynamically create 10 LoRA slots with activation toggles
        for i in range(1, 11):
            inputs["required"][f"lora_name_{i}"] = (lora_list,)
            inputs["required"][f"lora_active_{i}"] = ("BOOLEAN", {"default": True})

        return inputs

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "INT")
    RETURN_NAMES = ("model", "clip", "selected_lora_name", "selected_lora_index")
    FUNCTION = "load_random_lora"
    CATEGORY = "EmAySee"

    def load_random_lora(self, model, clip, strength_model, strength_clip, seed, **kwargs):
        lora_options = []
        # Collect all active LoRAs from the inputs
        for i in range(1, 11):
            lora_name = kwargs.get(f"lora_name_{i}")
            is_active = kwargs.get(f"lora_active_{i}")
            if lora_name and lora_name != "None" and is_active:
                lora_options.append({"name": lora_name, "index": i})
        
        selected_lora_name = "None"
        selected_lora_index = 0
        
        # If no valid loras are active or strength is 0, pass through the original model/clip
        if not lora_options or (strength_model == 0 and strength_clip == 0):
            return (model, clip, selected_lora_name, selected_lora_index)

        # Use the provided seed for reproducibility
        random.seed(seed)
        selected_lora = random.choice(lora_options)
        selected_lora_name = selected_lora["name"]
        selected_lora_index = selected_lora["index"]

        # --- LoRA Loading Logic (adapted from the default LoraLoader) ---
        lora_path = folder_paths.get_full_path("loras", selected_lora_name)
        lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        
        return (model_lora, clip_lora, selected_lora_name, selected_lora_index)

NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomLoraLoader": EmAySee_RandomLoraLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomLoraLoader": "Random LoRA Loader (EmAySee)"
}
