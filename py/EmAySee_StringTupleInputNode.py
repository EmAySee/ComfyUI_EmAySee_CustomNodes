import comfy.sd
import torch
import numpy as np

class EmAySee_StringTupleInputNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "string_list": ("STRING", {"multiline": True, "default": "Label 1\nLabel 2\nLabel 3\n...\nLabel 20"}),
                 },
                }

    RETURN_TYPES = ("STRING_TUPLE",)
    RETURN_NAMES = ("STRING_TUPLE_OUTPUT",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "create_string_tuple"

    def create_string_tuple(self, string_list):
        lines = string_list.strip().split('\n') # Split multiline string into lines
        string_tuple = tuple(line.strip() for line in lines) # Create a tuple of strings, stripping whitespace from each line
        return (string_tuple,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_StringTupleInputNode": EmAySee_StringTupleInputNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_StringTupleInputNode": "EmAySee String Tuple Input"
}