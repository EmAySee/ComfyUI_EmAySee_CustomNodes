import comfy.sd
import torch
import numpy as np

class EmAySee_RemoveDuplicateCSV:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"csv_string": ("STRING", {"multiline": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("unique_csv_string",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "remove_duplicates"

    def remove_duplicates(self, csv_string):
        try:
            elements = csv_string.split(",")
            unique_elements = []
            seen = set()

            for element in elements:
                stripped_element = element.strip()
                if stripped_element not in seen:
                    unique_elements.append(stripped_element)
                    seen.add(stripped_element)

            unique_string = ", ".join(unique_elements)
            return (unique_string,)

        except Exception as e:
            print(f"Error processing string: {e}")
            return (csv_string,) #return the original string if there is an error.

NODE_CLASS_MAPPINGS = {
    "EmAySee_RemoveDuplicateCSV": EmAySee_RemoveDuplicateCSV
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RemoveDuplicateCSV": "EmAySee Remove Duplicate CSV"
}