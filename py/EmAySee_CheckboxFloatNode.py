import comfy.sd
import torch
import numpy as np

class EmAySee_CheckboxFloatNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "checkbox_input": ("BOOLEAN", {"default": False, "label": "Enable (Outputs 1.0)"}),
                 },
                }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("CHECKBOX_VALUE",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "checkbox_to_float"

    def checkbox_to_float(self, checkbox_input):
        if checkbox_input: # If checkbox_input is True (checked)
            return (1.0,)
        else: # If checkbox_input is False (unchecked)
            return (0.0,) # Or you could return (0.0,) if you prefer 0 when unchecked

NODE_CLASS_MAPPINGS = {
    "EmAySee_CheckboxFloatNode": EmAySee_CheckboxFloatNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_CheckboxFloatNode": "EmAySee Checkbox to Float"
}