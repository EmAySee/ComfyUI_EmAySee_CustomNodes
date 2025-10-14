import comfy.sd
import torch
import numpy as np

class EmAySee_IntegerStringSelectorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "string_input_1": ("STRING", {"default": "Input String 1"}),
                    "string_input_2": ("STRING", {"default": "Input String 2"}),
                    "string_input_3": ("STRING", {"default": "Input String 3"}),
                    "string_input_4": ("STRING", {"default": "Input String 4"}),
                    "select_index": ("INT", {
                        "default": 1,
                        "min": 1,
                        "max": 4,
                        "step": 1,
                        "display": "slider", # Or "number"
                        "label": "Select Input (1-4)"
                    }),
                 },
                }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("SELECTED_STRING",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "EmAySee_function"

    def EmAySee_function(self, string_input_1, string_input_2, string_input_3, string_input_4, select_index):
        if select_index == 1:
            return (string_input_1,)
        elif select_index == 2:
            return (string_input_2,)
        elif select_index == 3:
            return (string_input_3,)
        elif select_index == 4:
            return (string_input_4,)
        else:
            return ("",) # Should not happen given input constraints, but as a failsafe


NODE_CLASS_MAPPINGS = { # Moved to after the class definition
    "EmAySee_IntegerStringSelectorNode": EmAySee_IntegerStringSelectorNode
}

NODE_DISPLAY_NAME_MAPPINGS = { # Moved to after the class definition
    "EmAySee_IntegerStringSelectorNode": "EmAySee Integer String Selector"
}