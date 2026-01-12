class EmAySee_DimensionSwapper:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 8}),
                "height": ("INT", {"default": 512, "min": 1, "max": 4096, "step": 8}),
                "swap_dimensions": (["No Swap", "Swap"],)
            }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("WIDTH", "HEIGHT",)
    FUNCTION = "swap_dims"
    CATEGORY = "EmAySee/Dimensions"

    def swap_dims(self, width, height, swap_dimensions):
        if swap_dimensions == "Swap":
            return (height, width,)
        else:
            return (width, height,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_DimensionSwapper": EmAySee_DimensionSwapper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_DimensionSwapper": "EmAySee Dimension Swapper"
}
