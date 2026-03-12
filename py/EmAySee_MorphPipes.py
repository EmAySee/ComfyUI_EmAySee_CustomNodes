class EmAySee_MorphPipeIn:
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

    RETURN_TYPES = ("MORPH_PIPE",)
    RETURN_NAMES = ("morph_pipe",)
    FUNCTION = "bundle"
    CATEGORY = "EmAySee/Morph"

    def bundle(self, **kwargs):
        return (kwargs,)

class EmAySee_MorphPipeOut:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "morph_pipe": ("MORPH_PIPE",),
            }
        }

    RETURN_TYPES = ("FLOAT",) * 20
    RETURN_NAMES = (
        "Breast Size", "Breast Sag", "Areola Size", "Puffies",
        "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
        "Thigh Spacing", "Body Type", "Pregnant", "PHP",
        "Extra 01", "Extra 02", "Extra 03", "Extra 04", "Extra 05",
        "Extra 06", "Extra 07", "Extra 08"
    )
    FUNCTION = "expand"
    CATEGORY = "EmAySee/Morph"

    def expand(self, morph_pipe):
        labels = [
            "Breast Size", "Breast Sag", "Areola Size", "Puffies",
            "Belly Fat", "Waist Size", "Butt Size", "Thigh Size",
            "Thigh Spacing", "Body Type", "Pregnant", "PHP",
            "Extra 01", "Extra 02", "Extra 03", "Extra 04", "Extra 05",
            "Extra 06", "Extra 07", "Extra 08"
        ]
        
        results = [morph_pipe.get(label, 0.0) for label in labels]
        return tuple(results)

NODE_CLASS_MAPPINGS = {
    "EmAySee_MorphPipeIn": EmAySee_MorphPipeIn,
    "EmAySee_MorphPipeOut": EmAySee_MorphPipeOut
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MorphPipeIn": "EmAySee Morph Pipe In",
    "EmAySee_MorphPipeOut": "EmAySee Morph Pipe Out"
}