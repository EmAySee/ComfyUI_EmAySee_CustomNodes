class EmAySee_FloatToText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "min": -3.0, "max": 3.0, "step": 0.05}),
                "prefix": ("STRING", {"default": "", "multiline": False}),
                "suffix": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING", "FLOAT")
    RETURN_NAMES = ("text", "float")
    FUNCTION = "convert"
    CATEGORY = "EmAySee/Text"

    def convert(self, value, prefix, suffix):
        return (f"({prefix}:{value}{suffix})", value)

NODE_CLASS_MAPPINGS = {
    "EmAySee_FloatToText": EmAySee_FloatToText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_FloatToText": "EmAySee Float To Text"
}