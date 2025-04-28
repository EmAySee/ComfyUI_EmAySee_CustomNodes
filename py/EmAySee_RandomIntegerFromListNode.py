import comfy.sd
import torch
import numpy as np
import random

class EmAySee_RandomIntegerFromListNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "integer_list_str": ("STRING", {"multiline": False, "default": "1, 5, 10, 25"}),
                 },
                }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("RANDOM_INTEGER",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "get_random_integer"

    def get_random_integer(self, integer_list_str):
        integer_strings = integer_list_str.strip().split(',')
        valid_integers = []
        for s in integer_strings:
            try:
                integer_value = int(s.strip())
                valid_integers.append(integer_value)
            except ValueError:
                print(f"EmAySee Random Integer From List: Ignoring invalid integer string: '{s.strip()}'")

        if valid_integers:
            selected_integer = random.choice(valid_integers)
            return (selected_integer,)
        else:
            print("EmAySee Random Integer From List: No valid integers found in input string. Returning 0.")
            return (0,) # Or you could return (None,) if you prefer None when no valid integers

NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomIntegerFromListNode": EmAySee_RandomIntegerFromListNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomIntegerFromListNode": "EmAySee Random Integer From List"
}