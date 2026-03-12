import re

class EmAySee_TwentyFloatToTextAndFloat:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        labels = [
            "Breasts Size", "Breasts Sag", "Areloas Size", "Puffie",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Spacing", "Body Type", "Pregnant", "Pubic Hair Peek",
            "Option 01", "Option 02", "Option 03", "Option 04", "Option 05",
            "Option 06", "Option 07", "Option 08"
        ]
        
        inputs = {"required": {}}
        for label in labels:
            inputs["required"][label] = ("FLOAT", {"default": 0.0, "min": -2.0, "max": 3.0, "step": 0.01})
            
        return inputs

    RETURN_TYPES = ("STRING",) + ("FLOAT",) * 20
    RETURN_NAMES = ("combined_text",) + (
        "Breasts Size", "Breasts Sag", "Areloas Size", "Puffie",
        "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
        "Thigh Spacing", "Body Type", "Pregnant", "Pubic Hair Peek",
        "Option 01", "Option 02", "Option 03", "Option 04", "Option 05",
        "Option 06", "Option 07", "Option 08"
    )
    FUNCTION = "convert"
    CATEGORY = "EmAySee/Text"

    def convert(self, **kwargs):
        labels = [
            "Breasts Size", "Breasts Sag", "Areloas Size", "Puffie",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Spacing", "Body Type", "Pregnant", "Pubic Hair Peek",
            "Option 01", "Option 02", "Option 03", "Option 04", "Option 05",
            "Option 06", "Option 07", "Option 08"
        ]
        
        combined_list = []
        float_outputs = []
        
        for label in labels:
            value = kwargs.get(label, 0.0)
            float_outputs.append(value)
            if value != 0.0:
                combined_list.append(f"{label}: {value:.2f}")
                
        return ("\n".join(combined_list),) + tuple(float_outputs)

NODE_CLASS_MAPPINGS = {
    "EmAySee_TwentyFloatToTextAndFloat": EmAySee_TwentyFloatToTextAndFloat
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TwentyFloatToTextAndFloat": "EmAySee Twenty Float To Text And Float"
}