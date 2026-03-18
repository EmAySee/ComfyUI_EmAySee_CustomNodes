import torch

class EmAySee_LoraSelector:
    """
    A universal Lora control node that provides file selection and strength controls
    as internal widgets (no inputs) and outputs the values for downstream loaders.
    """
    @classmethod
    def INPUT_TYPES(s):
        #  Define the controls as part of the INPUT_TYPES but specify that they should 
        #  be rendered as internal widgets (input_is_widget=True)
        return {
            "required": {
                #  This input is used solely for the internal widget rendering.
                "lora_name": ("LORA", {"default": "NONE", "input_is_widget": True, "widget_name": "lora_name_select"}), 
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, "input_is_widget": True, "widget_name": "strength_model_select"}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, "input_is_widget": True, "widget_name": "strength_clip_select"}),
            },
            "optional": {},
        }

    #  The output now includes the filename and the two strength values as separate outputs
    RETURN_TYPES = ("LORA", "FLOAT", "FLOAT",) 
    RETURN_NAMES = ("lora_filename", "strength_model", "strength_clip",)
    CATEGORY = "EmAySee/Loaders"
    FUNCTION = "EmAySee_select_lora"

    def EmAySee_select_lora(self, lora_name, strength_model, strength_clip):
        #  The node receives values from its internal widgets and passes them out.
        return (lora_name, strength_model, strength_clip,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_LoraSelector": EmAySee_LoraSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoraSelector": "EmAySee Lora Name Selector"
}
