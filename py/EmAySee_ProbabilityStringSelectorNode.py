import comfy.sd
import torch
import numpy as np
import random

class EmAySee_ProbabilityStringSelectorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "string_input_1": ("STRING", {"default": "Option 1 - Less Likely"}),
                    "string_input_2": ("STRING", {"default": "Option 2 - More Likely"}),
                    "probability_option_1": ("FLOAT", {
                        "default": 0.1,  # Default probability of 10% for option 1
                        "min": 0.0,      # Minimum probability is 0%
                        "max": 1.0,      # Maximum probability is 100%
                        "step": 0.01,     # Probability step of 1%
                        "label": "Probability of Option 1 (0.0-1.0)"
                    }),
                 },
                }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("PROBABILISTIC_SELECTED_STRING",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "EmAySee_function"

    def EmAySee_function(self, string_input_1, string_input_2, probability_option_1):
        # Generate a random float between 0.0 and 1.0
        random_value = random.random()

        if random_value < probability_option_1:
            return (string_input_1,)  # Select string_input_1 if random_value is less than the probability
        else:
            return (string_input_2,)  # Otherwise, select string_input_2

NODE_CLASS_MAPPINGS = {
    "EmAySee_ProbabilityStringSelectorNode": EmAySee_ProbabilityStringSelectorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ProbabilityStringSelectorNode": "EmAySee Probability String Selector"
}