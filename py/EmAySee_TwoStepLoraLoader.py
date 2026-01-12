import comfy.utils
import comfy.sd
import folder_paths

lora_names = ["None"] + folder_paths.get_filename_list("loras")

class EmAySee_LoraNameSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_name": (lora_names,),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("lora_name",)
    FUNCTION = "get_name"
    CATEGORY = "EmAySee/Loaders"

    def get_name(self, lora_name):
        return (lora_name,)

class EmAySee_LoraApplier:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_name": ("STRING", {"default": "None", "multiline": False}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "apply_lora"
    CATEGORY = "EmAySee/Loaders"

    def apply_lora(self, model, clip, lora_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0 or lora_name is None or lora_name == "None":
            return (model, clip)

        lora_path = folder_paths.get_full_path("loras", lora_name)
        
        if not lora_path:
            print(f"EmAySee LoRA Applier: Warning, LoRA not found: {lora_name}")
            return (model, clip)

        lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        
        return (model_lora, clip_lora)


NODE_CLASS_MAPPINGS = {
    "EmAySee_LoraNameSelector": EmAySee_LoraNameSelector,
    "EmAySee_LoraApplier": EmAySee_LoraApplier,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoraNameSelector": "EmAySee LoRA Name Selector",
    "EmAySee_LoraApplier": "EmAySee LoRA Applier",
}