import math

class EmAySee_DynamicRangeSlider:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "min_val": ("FLOAT", {"default": -1.0, "step": 0.1}),
                "max_val": ("FLOAT", {"default": 2.0, "step": 0.1}),
                "step_val": ("FLOAT", {"default": 0.25, "min": 0.001, "step": 0.001}),
                "value_percent": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }
    
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "get_value"
    CATEGORY = "EmAySee/Utils"

    def get_value(self, min_val, max_val, step_val, value_percent):
        if min_val > max_val:
            min_val, max_val = max_val, min_val

        raw_value = min_val + (value_percent * (max_val - min_val))

        quantized_value = raw_value
        if step_val > 0:
            quantized_value = round(raw_value / step_val) * step_val
        
        final_value = max(min_val, min(max_val, quantized_value))

        return (final_value,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_DynamicRangeSlider": EmAySee_DynamicRangeSlider
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_DynamicRangeSlider": "EmAySee Dynamic Range Slider"
}