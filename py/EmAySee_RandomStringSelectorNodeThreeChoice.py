import comfy.sd
import torch
import numpy as np
import random  # Import the random module

class EmAySee_RandomStringSelectorNodeThreeChoice:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "string_input_1": ("STRING", {"default": "Input String 1"}),
                    "string_input_2": ("STRING", {"default": "Input String 2"}),
                    "string_input_3": ("STRING", {"default": "Input String 3"}),
                 },
                }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("RANDOM_SELECTED_STRING",)
    CATEGORY = "EmAySee_Utils" # Or a category you prefer

    FUNCTION = "EmAySee_function"

    def EmAySee_function(self, string_input_1, string_input_2, string_input_3):
        # Generate a random number (0 , 1 , 2 )
        random_choice = random.randint(0, 2)

        if random_choice == 0:
            return (string_input_1,)  # Return the first input if random_choice is 0
        if random_choice == 1:
            return (string_input_2,)  # Return the first input if random_choice is 1
        else:
            return (string_input_3,)  # Return the first input if random_choice is 2


NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomStringSelectorNodeThreeChoice": EmAySee_RandomStringSelectorNodeThreeChoice
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomStringSelectorNodeThreeChoice": "EmAySee Random String SelectorThreeChoice"
}