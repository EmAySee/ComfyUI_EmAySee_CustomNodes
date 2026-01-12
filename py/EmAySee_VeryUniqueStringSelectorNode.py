import comfy.sd
import torch
import numpy as np

class EmAySee_StringSelectorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "string_input_1": ("STRING", {"default": "Input String 1"}),
                    "string_input_2": ("STRING", {"default": "Input String 2"}),
                    "select_input": (["string_input_1", "string_input_2"], {"default": "string_input_1", "label": "Select Input"})
                 },
                }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("SELECTED_STRING",)
    CATEGORY = "EmAySee_Utils" # Or a category you prefer

    FUNCTION = "EmAySee_function"  # <-- IMPORTANT: Back to string for FUNCTION

    def EmAySee_function(self, string_input_1, string_input_2, select_input): # Ensure defined AFTER FUNCTION is set
        if select_input == "string_input_1":
            return (string_input_1,)
        elif select_input == "string_input_2":
            return (string_input_2,)
        else:
            return ("",) # Should not happen, but default to empty string

NODE_CLASS_MAPPINGS = {
    "EmAySee_VeryUniqueStringSelectorNode": EmAySee_StringSelectorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_VeryUniqueStringSelectorNode": "EmAySee REALLY Unique String Selector"
}