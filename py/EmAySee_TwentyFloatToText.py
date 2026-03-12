import re

class EmAySee_TwentyFloatToText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        labels = [
            "Breasts Size", "Breasts Sag", "Areolas Size", "Puffies",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Gap", "Body Type", "Pregnant", "Peeking Pubic Hairs"
        ]
        
        inputs = {"required": {}}
        for label in labels:
            inputs["required"][label] = ("FLOAT", {"default": 0.0, "min": -3.0, "max": 5.0, "step": 0.1})
            
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)
    FUNCTION = "convert"
    CATEGORY = "EmAySee/Text"

    def convert(self, **kwargs):
        labels = [
            "Breasts Size", "Breasts Sag", "Areolas Size", "Puffies",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Gap", "Body Type", "Pregnant", "Peeking Pubic Hairs"
        ]
        
        combined_list = []
        for label in labels:
            value = kwargs.get(label, 0.0)
            if value != 0.0:
                combined_list.append(f"{label}: {value:.2f}")
                
        return ("\n".join(combined_list),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_TwentyFloatToText": EmAySee_TwentyFloatToText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TwentyFloatToText": "EmAySee Twenty Float To Text"
}