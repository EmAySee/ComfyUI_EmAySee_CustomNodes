class EmAySee_StringDetector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "detected_value": ("INT", {"default": 1, "min": -1000000, "max": 1000000}),
            },
            "optional": {
                "text_input": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    FUNCTION = "detect"
    CATEGORY = "EmAySee/Logic"

    def detect(self, detected_value, text_input=None):
        if text_input is not None and text_input != "":
            return (detected_value,)
        return (0,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_StringDetector": EmAySee_StringDetector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "f": "EmAySee String Detector"
}