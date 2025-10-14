import comfy.sd
import torch
import numpy as np
import random

class EmAySee_DynamicStringSelectorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "string_input_1": ("STRING", {"default": "Initial Input"}), # Added initial input
            "select_index": ("INT", {"default": 1, "min": 1, "max": 1, "step": 1, "display": "slider", "label": "Select Input"}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
        }, "optional": {}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("SELECTED_STRING",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "EmAySee_function"

    @classmethod
    def IS_CHANGED(s, *args):
        return float("nan") # Never cache, so the node updates every time

    @classmethod
    def VALIDATE_INPUTS(s, select_index, seed, **kwargs):
        max_index = len(kwargs)
        if select_index > max_index or select_index < 1:
            return f"Select index must be between 1 and {max_index}"
        return True

    def EmAySee_function(self, select_index, seed, **kwargs):
        if not kwargs:
            return ("",)  # No inputs connected
        random.seed(seed) #seed the random generator
        return (list(kwargs.values())[select_index - 1],)

    @classmethod
    def UPDATE_INPUT_TYPES(cls, config):
        input_types = {"required": {
            "select_index": ("INT", {"default": 1, "min": 1, "max": 1, "step": 1, "display": "slider", "label": "Select Input"}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
        }, "optional": {}}
        if config is not None:
            max_index = len(config)
            if max_index > 0:
                input_types["required"]["select_index"][1]["max"] = max_index
            for i in range(1, max_index+1):
                input_types["optional"][f"string_input_{i}"] = ("STRING",)

        else:
           input_types["required"]["string_input_1"] = ("STRING", {"default": "Initial Input"})

        return input_types

NODE_CLASS_MAPPINGS = {
    "EmAySee_DynamicStringSelectorNode": EmAySee_DynamicStringSelectorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_DynamicStringSelectorNode": "EmAySee Dynamic String Selector Seeded V2"
}