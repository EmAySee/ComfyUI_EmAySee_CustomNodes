import torch

class EmAySee_TwentyFloatToTextV2:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        labels = [
            "Breast Size", "Breast Sag", "Areola Size", "Puffies",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Spacing", "Body Type", "Pregnant", "PHP",
            "Extra 01", "Extra 02", "Extra 03", "Extra 04", "Extra 05",
            "Extra 06", "Extra 07", "Extra 08"
        ]
        
        inputs = {"required": {}}
        for label in labels:
            inputs["required"][label] = ("FLOAT", {"default": 0.0, "min": -2.0, "max": 3.0, "step": 0.01})
            
        return inputs

    RETURN_TYPES = ("STRING",) + ("STRING",) * 20 + ("FLOAT",) * 20
    RETURN_NAMES = ("combined_text",) + (
        "T_Breast Size", "T_Breast Sag", "T_Areola Size", "T_Puffies",
        "T_Belly Fat", "T_Waist Size", "T_Butt Size", "T_Thigh Size",
        "T_Thigh Spacing", "T_Body Type", "T_Pregnant", "T_PHP",
        "T_Extra 01", "T_Extra 02", "T_Extra 03", "T_Extra 04", "T_Extra 05",
        "T_Extra 06", "T_Extra 07", "T_Extra 08",
        "F_Breast Size", "F_Breast Sag", "F_Areola Size", "F_Puffies",
        "F_Belly Fat", "F_Waist Size", "F_Butt Size", "F_Thigh Size",
        "F_Thigh Spacing", "F_Body Type", "F_Pregnant", "F_PHP",
        "F_Extra 01", "F_Extra 02", "F_Extra 03", "F_Extra 04", "F_Extra 05",
        "F_Extra 06", "F_Extra 07", "F_Extra 08"
    )
    FUNCTION = "convert"
    CATEGORY = "EmAySee/Text"

    def convert(self, **kwargs):
        labels = [
            "Breast Size", "Breast Sag", "Areola Size", "Puffies",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Spacing", "Body Type", "Pregnant", "PHP",
            "Extra 01", "Extra 02", "Extra 03", "Extra 04", "Extra 05",
            "Extra 06", "Extra 07", "Extra 08"
        ]
        
        combined_list = []
        individual_texts = []
        float_outputs = []
        
        for label in labels:
            value = kwargs.get(label, 0.0)
            float_outputs.append(value)
            
            if value != 0.0:
                formatted = f"{label}: {value:.2f}"
                combined_list.append(formatted)
                individual_texts.append(formatted)
            else:
                individual_texts.append("")
                
        return ("\n".join(combined_list),) + tuple(individual_texts) + tuple(float_outputs)

NODE_CLASS_MAPPINGS = {
    "EmAySee_TwentyFloatToTextV2": EmAySee_TwentyFloatToTextV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TwentyFloatToTextV2": "EmAySee Twenty Float To Text V2"
}