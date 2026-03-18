import comfy.sd
import torch
import numpy as np

class EmAySee_ToggleIntNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "toggle_input": ("BOOLEAN", {"default": False, "label": "Toggle (On/Off)"}),
                    "int_if_on": ("INT", {"default": 1, "label": "Integer if ON"}),
                    "int_if_off": ("INT", {"default": 0, "label": "Integer if OFF"}),
                 },
                }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("TOGGLE_INT_OUTPUT",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "toggle_to_integer"

    def toggle_to_integer(self, toggle_input, int_if_on, int_if_off):
        if toggle_input: # If toggle_input is True (toggle is ON)
            return (int_if_on,)
        else: # If toggle_input is False (toggle is OFF)
            return (int_if_off,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_ToggleIntNode": EmAySee_ToggleIntNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ToggleIntNode": "EmAySee Toggle to Integer"
}