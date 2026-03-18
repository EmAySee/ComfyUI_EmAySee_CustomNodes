import folder_paths
import comfy.sd
import comfy.utils

class EmAySee_LoraNameSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_name": (folder_paths.get_filename_list("loras"), ),
            }
        }
    
    RETURN_TYPES = ("LORA_OBJECT",) 
    RETURN_NAMES = ("lora_object",)
    FUNCTION = "load_lora_data"
    CATEGORY = "EmAySee/Loaders"

    def load_lora_data(self, lora_name):
        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = None
        if lora_path is None:
            print(f"Lora not found: {lora_name}")
            return (None,)
        else:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
        return (lora,)

class EmAySee_LoraProcessor:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_selector": ("INT", {"default": 1, "min": 1, "max": 9}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            },
            "optional": {}
        }
        
        for i in range(1, 10):
            inputs["optional"][f"lora_object_{i}"] = ("LORA_OBJECT",)
            
        return inputs

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "apply_selected_lora"
    CATEGORY = "EmAySee/Loaders"

    def apply_selected_lora(self, model, clip, lora_selector, strength_model, strength_clip, **kwargs):
        selected_key = f"lora_object_{lora_selector}"
        lora_object = kwargs.get(selected_key, None)

        if strength_model == 0 and strength_clip == 0:
            return (model, clip)
        
        if lora_object is None:
            return (model, clip)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora_object, strength_model, strength_clip)
        return (model_lora, clip_lora)

class EmAySee_NineChoiceSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "selector": ("INT", {"default": 1, "min": 1, "max": 9}),
                "label_1": ("STRING", {"multiline": False, "default": "Option 1"}),
                "label_2": ("STRING", {"multiline": False, "default": "Option 2"}),
                "label_3": ("STRING", {"multiline": False, "default": "Option 3"}),
                "label_4": ("STRING", {"multiline": False, "default": "Option 4"}),
                "label_5": ("STRING", {"multiline": False, "default": "Option 5"}),
                "label_6": ("STRING", {"multiline": False, "default": "Option 6"}),
                "label_7": ("STRING", {"multiline": False, "default": "Option 7"}),
                "label_8": ("STRING", {"multiline": False, "default": "Option 8"}),
                "label_9": ("STRING", {"multiline": False, "default": "Option 9"}),
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("selected_int", "selected_label")
    FUNCTION = "get_choice"
    CATEGORY = "EmAySee/Utils"

    def get_choice(self, selector, label_1, label_2, label_3, label_4, label_5, label_6, label_7, label_8, label_9):
        labels = [label_1, label_2, label_3, label_4, label_5, label_6, label_7, label_8, label_9]
        idx = max(1, min(9, selector)) - 1
        return (selector, labels[idx])

class EmAySee_LoraStacker20:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
            },
            "optional": {}
        }
        
        #  Create inputs for 20 Loras with individual strength controls
        for i in range(1, 21):
            inputs["optional"][f"lora_{i}"] = ("LORA_OBJECT",)
            inputs["required"][f"strength_model_{i}"] = ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01})
            inputs["required"][f"strength_clip_{i}"] = ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01})
            
        return inputs

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "apply_stack"
    CATEGORY = "EmAySee/Loaders"

    def apply_stack(self, model, clip, **kwargs):
        current_model = model
        current_clip = clip

        #  Iterate through all 20 possible slots
        for i in range(1, 21):
            lora_obj = kwargs.get(f"lora_{i}", None)
            str_model = kwargs.get(f"strength_model_{i}", 1.0)
            str_clip = kwargs.get(f"strength_clip_{i}", 1.0)

            #  Only apply if a Lora Object is connected to the slot
            if lora_obj is not None:
                 if str_model == 0 and str_clip == 0:
                     continue
                 current_model, current_clip = comfy.sd.load_lora_for_models(current_model, current_clip, lora_obj, str_model, str_clip)
        
        return (current_model, current_clip)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LoraNameSelector": EmAySee_LoraNameSelector,
    "EmAySee_LoraProcessor": EmAySee_LoraProcessor,
    "EmAySee_NineChoiceSelector": EmAySee_NineChoiceSelector,
    "EmAySee_LoraStacker20": EmAySee_LoraStacker20
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoraNameSelector": "EmAySee Lora Selector (Object)",
    "EmAySee_LoraProcessor": "EmAySee Lora Processor (9-Input Switch)",
    "EmAySee_NineChoiceSelector": "EmAySee Nine Choice Selector",
    "EmAySee_LoraStacker20": "EmAySee Lora Stacker (20 Sequential)"
}