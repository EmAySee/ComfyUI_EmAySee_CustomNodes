import comfy.sd
import torch
import numpy as np

class EmAySee_IntegerStringSelectorNodeDynamic:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {"required": {}}
        for i in range(1, 21):
            inputs["required"][f"string_input_{i}"] = ("STRING", {"default": f"Input String {i}"})
        inputs["required"]["select_index"] = ("INT", {
            "default": 1,
            "min": 1,
            "max": 20,
            "step": 1,
            "display": "slider",
            "label": "Select Input (1-20)"
        })
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("SELECTED_STRING",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "EmAySee_function"

    def EmAySee_function(self, select_index, **kwargs):
        return (kwargs[f"string_input_{select_index}"],)

NODE_CLASS_MAPPINGS = {
    "EmAySee_IntegerStringSelectorNodeDynamic": EmAySee_IntegerStringSelectorNodeDynamic
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_IntegerStringSelectorNodeDynamic": "EmAySee Integer String Selector Max-20"
}