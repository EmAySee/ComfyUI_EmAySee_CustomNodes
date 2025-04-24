import comfy.sd
import torch
import numpy as np
import random

class EmAySee_RandomIntegerFromTogglesNode_PremadeLabels:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "node_description": ("STRING", {"multiline": True, "default": "Select options below to choose from randomly."}),
                    "option_1": ("TOGGLE", {"default": False, "label": "Option 1: Label for Option 1"}), # Example labels
                    "option_2": ("BOOLEAN", {"default": False, "label": "Option 2: Label for Option 2"}),
                    "option_3": ("BOOLEAN", {"default": False, "label": "Option 3: Label for Option 3"}),
                    "option_4": ("BOOLEAN", {"default": False, "label": "Option 4: Label for Option 4"}),
                    "option_5": ("BOOLEAN", {"default": False, "label": "Option 5: Label for Option 5"}),
                    "option_6": ("BOOLEAN", {"default": False, "label": "Option 6: Label for Option 6"}),
                    "option_7": ("BOOLEAN", {"default": False, "label": "Option 7: Label for Option 7"}),
                    "option_8": ("BOOLEAN", {"default": False, "label": "Option 8: Label for Option 8"}),
                    "option_9": ("BOOLEAN", {"default": False, "label": "Option 9: Label for Option 9"}),
                    "option_10": ("BOOLEAN", {"default": False, "label": "Option 10: Label for Option 10"}),
                    "option_11": ("BOOLEAN", {"default": False, "label": "Option 11: Label for Option 11"}),
                    "option_12": ("BOOLEAN", {"default": False, "label": "Option 12: Label for Option 12"}),
                    "option_13": ("BOOLEAN", {"default": False, "label": "Option 13: Label for Option 13"}),
                    "option_14": ("BOOLEAN", {"default": False, "label": "Option 14: Label for Option 14"}),
                    "option_15": ("BOOLEAN", {"default": False, "label": "Option 15: Label for Option 15"}),
                    "option_16": ("BOOLEAN", {"default": False, "label": "Option 16: Label for Option 16"}),
                    "option_17": ("BOOLEAN", {"default": False, "label": "Option 17: Label for Option 17"}),
                    "option_18": ("BOOLEAN", {"default": False, "label": "Option 18: Label for Option 18"}),
                    "option_19": ("BOOLEAN", {"default": False, "label": "Option 19: Label for Option 19"}),
                    "option_20": ("BOOLEAN", {"default": False, "label": "Option 20: Label for Option 20"}),
                }}

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("RANDOM_TOGGLE_INTEGER",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "get_random_integer_from_toggles"

    def get_random_integer_from_toggles(self, node_description, **kwargs): # Only node_description and kwargs now
        selected_integers = []
        for i in range(1, 21):
            toggle_name = f"option_{i}" # Toggle input names are now option_1, option_2,...
            if kwargs.get(toggle_name, False):
                selected_integers.append(i)

        if selected_integers:
            selected_integer = random.choice(selected_integers)
            return (selected_integer,)
        else:
            print("EmAySee Random Integer From Toggles (Premade Labels): No toggles selected. Returning 0.")
            return (0,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomIntegerFromTogglesNode_PremadeLabels": EmAySee_RandomIntegerFromTogglesNode_PremadeLabels
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomIntegerFromTogglesNode_PremadeLabels": "EmAySee Random Integer From Toggles (Premade Labels)"
}